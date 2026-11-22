[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$LogPath
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Common.ps1')
$root = Get-RepoRoot

if (-not (Test-Path $LogPath)) { throw "Log file not found: $LogPath" }

$ignoreFile = Join-Path $root 'guardrails/log-ignore.txt'
$ignore = @(if (Test-Path $ignoreFile) { Get-Content $ignoreFile -Encoding UTF8 | Where-Object { $_.Trim() } })
$pattern = 'Assets[\\/]_Game[\\/].*warning RS0030|error [A-Z]{2,4}\d+|\w+Exception:|\bERROR\b|\[Error\]|Assertion failed|Failed to|Unhandled|UnityEngine\.Debug:LogError'

$groups = @{}
$lineNo = 0
$stream = [IO.File]::Open((Resolve-Path $LogPath).Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
$reader = New-Object IO.StreamReader($stream)
$allLines = New-Object System.Collections.Generic.List[string]
while ($null -ne ($next = $reader.ReadLine())) { $allLines.Add($next) }
$reader.Dispose()
foreach ($line in $allLines) {
    $lineNo++
    if ($line -cnotmatch $pattern) { continue }
    $skip = $false
    foreach ($ig in $ignore) { if ($line.Contains($ig)) { $skip = $true } }
    if ($skip) { continue }
    $key = ($line -replace '\d+', '#').Trim()
    if (-not $groups.ContainsKey($key)) { $groups[$key] = [pscustomobject]@{ Count = 0; FirstLine = $lineNo; Text = $line.Trim() } }
    $groups[$key].Count++
}

if ($groups.Count -eq 0) {
    Write-Output "No errors in log: $LogPath"
    exit 0
}

[Console]::Error.WriteLine("$($groups.Count) distinct log error(s) ($LogPath)")
$groups.Values | Sort-Object FirstLine | ForEach-Object {
    [Console]::Error.WriteLine(("  line {0} x{1}: {2}" -f $_.FirstLine, $_.Count, $_.Text))
}
exit 1
