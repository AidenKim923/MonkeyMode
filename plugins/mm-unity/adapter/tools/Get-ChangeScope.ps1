[CmdletBinding()]
param(
    [string]$Base = 'HEAD',
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Unity.ps1')
$root = Get-RepoRoot

$numstat = @(git -C $root diff $Base --numstat)
$untracked = @(git -C $root ls-files --others --exclude-standard)
$changed = New-Object System.Collections.Generic.List[object]
foreach ($row in $numstat) {
    $p = $row -split "`t"
    if ($p.Count -ge 3) { $changed.Add([pscustomobject]@{ Path = $p[2]; Added = $p[0]; Removed = $p[1]; Kind = 'modified' }) }
}
foreach ($u in $untracked) { $changed.Add([pscustomobject]@{ Path = $u; Added = '?'; Removed = '0'; Kind = 'new' }) }
$vendored = '^(.agents/skills|.claude/skills|_mm|_mm-output)/|.meta$|/(Library|Temp|Logs|UserSettings)/'
$vendoredCount = @($changed | Where-Object { $_.Path -match $vendored }).Count
$changed = New-Object System.Collections.Generic.List[object] (, @($changed | Where-Object { $_.Path -notmatch $vendored }))

$unityRoot = Get-UnityProjectRoot
$asmdefs = @(Get-ChildItem (Join-Path $(if ($unityRoot) { $unityRoot } else { $root }) 'Assets') -Recurse -Filter *.asmdef -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '[\\/](Library|Temp|ThirdParty)[\\/]' })
$guidToName = @{}
$asmInfo = @{}
foreach ($f in $asmdefs) {
    $j = Get-Content $f.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    $refs = if ($j.PSObject.Properties['references']) { @($j.references) } else { @() }
    $asmInfo[$j.name] = [pscustomobject]@{ Dir = $f.DirectoryName; Refs = $refs }
    $meta = "$($f.FullName).meta"
    if (Test-Path $meta) {
        $m = Get-Content $meta | Where-Object { $_ -match '^guid:' } | Select-Object -First 1
        if ($m) { $guidToName[($m -split ':\s*')[1].Trim()] = $j.name }
    }
}
foreach ($k in @($asmInfo.Keys)) {
    $asmInfo[$k].Refs = @($asmInfo[$k].Refs | ForEach-Object { if ($_ -like 'GUID:*') { $guidToName[$_.Substring(5)] } else { $_ } } | Where-Object { $_ })
}

function Find-Assembly([string]$relPath) {
    $full = (Join-Path $root $relPath)
    $best = $null
    foreach ($k in $asmInfo.Keys) {
        $d = $asmInfo[$k].Dir
        if ($full.StartsWith($d + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            if (-not $best -or $d.Length -gt $asmInfo[$best].Dir.Length) { $best = $k }
        }
    }
    return $best
}

$directAssemblies = New-Object System.Collections.Generic.HashSet[string]
$symbols = New-Object System.Collections.Generic.List[object]
foreach ($c in $changed) {
    if ($c.Path -notlike '*.cs' -and $c.Path -notlike '*.asmdef') { continue }
    $asm = Find-Assembly $c.Path
    if ($asm) { [void]$directAssemblies.Add($asm) }
    if ($c.Path -like '*.cs') {
        $file = Join-Path $root $c.Path
        if (Test-Path $file) {
            $text = Get-Content $file -Raw -Encoding UTF8
            foreach ($m in [regex]::Matches($text, '\b(?:class|struct|interface|enum)\s+(\w+)')) {
                $symbols.Add([pscustomobject]@{ Symbol = $m.Groups[1].Value; File = $c.Path })
            }
        }
    }
}

$affected = New-Object System.Collections.Generic.HashSet[string]
$queue = New-Object System.Collections.Generic.Queue[string]
foreach ($a in $directAssemblies) { [void]$affected.Add($a); $queue.Enqueue($a) }
while ($queue.Count -gt 0) {
    $cur = $queue.Dequeue()
    foreach ($k in $asmInfo.Keys) {
        if ($asmInfo[$k].Refs -contains $cur -and $affected.Add($k)) { $queue.Enqueue($k) }
    }
}

$references = New-Object System.Collections.Generic.List[object]
foreach ($s in ($symbols | Sort-Object Symbol -Unique)) {
    $hits = @(git -C $root grep --untracked -l -w -- $s.Symbol -- '*.cs' '*.asmdef' '*.unity' '*.prefab' '*.asset' 2>$null | Where-Object { $_ -ne $s.File })
    if ($hits.Count -gt 0) { $references.Add([pscustomobject]@{ Symbol = $s.Symbol; DeclaredIn = $s.File; ReferencedBy = $hits }) }
}

$testAssemblies = @($affected | Where-Object { $_ -like '*.Tests' -or $_ -like '*Tests*' } | Sort-Object)
$hunks = @(git -C $root diff $Base -U0 -- '*.cs' | Select-String -Pattern '^@@.*@@\s*(.+)$' | ForEach-Object { $_.Matches[0].Groups[1].Value.Trim() } | Sort-Object -Unique)

$result = [pscustomobject]@{
    ChangedFiles = $changed
    ChangedAssemblies = @($directAssemblies | Sort-Object)
    AffectedAssemblies = @($affected | Sort-Object)
    CandidateTestAssemblies = $testAssemblies
    TouchedMemberContext = $hunks
    SymbolReferences = $references
    HasTests = ($testAssemblies.Count -gt 0)
}

$outDir = Get-AgentOutputDir 'scope'
$result | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $outDir 'last-scope.json') -Encoding UTF8

if ($Json) { $result | ConvertTo-Json -Depth 6; exit 0 }

Write-Output "== 1. Changed files ($($changed.Count)) =="
$changed | ForEach-Object { Write-Output ("  [{0}] {1}  +{2}/-{3}" -f $_.Kind, $_.Path, $_.Added, $_.Removed) }
if ($vendoredCount -gt 0) { Write-Output "  ($vendoredCount changes in vendored _mm/ and skill folders left out of this list)" }
Write-Output "== Touched class/function context =="
$hunks | ForEach-Object { Write-Output "  $_" }
Write-Output "== 2. Impact =="
Write-Output ("  Directly changed assemblies: " + (($result.ChangedAssemblies) -join ', '))
Write-Output ("  Transitively affected assemblies: " + (($result.AffectedAssemblies) -join ', '))
Write-Output "  Files referencing the declared types:"
foreach ($r in $references) { Write-Output ("    {0} ({1}) <- {2}" -f $r.Symbol, $r.DeclaredIn, ($r.ReferencedBy -join ', ')) }
Write-Output "== 3. Test assemblies to run first =="
if ($testAssemblies.Count -gt 0) { $testAssemblies | ForEach-Object { Write-Output "  $_" } } else { Write-Output '  (none) If this is a core change, add a verification scenario or tests with it.' }
