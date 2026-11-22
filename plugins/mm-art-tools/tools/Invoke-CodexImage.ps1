param(
    [string]$Prompt,
    [string]$Name,
    [string]$SpecFile,
    [string]$Model,
    [string]$Effort = 'medium',
    [int]$ThrottleLimit = 4,
    [int]$TimeoutSeconds = 600,
    [string]$Reference,
    [string]$ProjectRoot
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
if (-not $ProjectRoot) {
    $ProjectRoot = (& git rev-parse --show-toplevel 2>$null)
    if (-not $ProjectRoot) { $ProjectRoot = (Get-Location).Path }
}

if ($SpecFile) {
    $jobs = @(Get-Content $SpecFile -Raw -Encoding UTF8 | ConvertFrom-Json | ForEach-Object { [pscustomobject]@{ Prompt = $_.prompt; Name = $_.name } })
} elseif ($Prompt -and $Name) {
    $jobs = @([pscustomobject]@{ Prompt = $Prompt; Name = $Name })
} else {
    throw 'Pass -SpecFile, or -Prompt together with -Name.'
}
if (@($jobs | Where-Object { $_.Name -notmatch '^[A-Za-z0-9_-]+$' }).Count -gt 0) { throw 'Names may contain only ASCII letters, digits, _ and -.' }
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'codex CLI not found on PATH. Install it or use another image backend.' }

$refArgs = @()
if ($Reference) {
    if (-not (Test-Path $Reference)) { throw "Reference image not found: $Reference" }
    $refArgs = @("-i", ("`"" + (Resolve-Path $Reference).Path + "`""))
}
$outDir = Join-Path $ProjectRoot (".agent-output/concepts/" + (Get-Date).ToString('yyyy-MM-dd'))
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$workDir = Join-Path ([IO.Path]::GetTempPath()) ("codex-image-" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $workDir | Out-Null

$results = $jobs | ForEach-Object -ThrottleLimit $ThrottleLimit -Parallel {
    $job = $_
    $log = Join-Path $using:workDir ($job.Name + '.jsonl')
    $last = Join-Path $using:workDir ($job.Name + '.txt')
    $inFile = Join-Path $using:workDir ($job.Name + '.in.txt')
    $request = "Generate one image with the image generation tool for this request. Reply with only the saved file path.`n`n" + $job.Prompt
    [IO.File]::WriteAllText($inFile, $request, (New-Object System.Text.UTF8Encoding($false)))
    $modelArgs = if ($using:Model) { @('-m', $using:Model) } else { @() }
    $proc = Start-Process -FilePath 'codex' -ArgumentList (@('exec') + $using:refArgs + $modelArgs + @('-c', ('model_reasoning_effort=' + $using:Effort), '--skip-git-repo-check', '--ephemeral', '--json', '-o', ('"' + $last + '"'), '-')) -RedirectStandardInput $inFile -WorkingDirectory $using:workDir -RedirectStandardOutput $log -RedirectStandardError ($log + '.err') -NoNewWindow -PassThru
    if (-not $proc.WaitForExit($using:TimeoutSeconds * 1000)) { $proc.Kill($true); return [pscustomobject]@{ Name = $job.Name; Ok = $false; Path = ''; Note = 'timed out' } }
    $threadLine = Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -like '*thread.started*' } | Select-Object -First 1
    $thread = if ($threadLine) { ($threadLine | ConvertFrom-Json).thread_id } else { $null }
    $png = $null
    if ($thread) {
        $dir = Join-Path $HOME ".codex/generated_images/$thread"
        if (Test-Path $dir) { $png = Get-ChildItem $dir -Filter *.png | Sort-Object LastWriteTime | Select-Object -Last 1 }
    }
    if ($proc.ExitCode -ne 0 -or -not $png) { return [pscustomobject]@{ Name = $job.Name; Ok = $false; Path = ''; Note = "exit code $($proc.ExitCode), no image produced" } }
    $dest = Join-Path $using:outDir ($job.Name + '.png')
    $n = 2
    while (Test-Path $dest) { $dest = Join-Path $using:outDir ("{0}-v{1}.png" -f $job.Name, $n); $n++ }
    Copy-Item $png.FullName $dest
    $meta = [ordered]@{ name = [IO.Path]::GetFileNameWithoutExtension($dest); prompt = $job.Prompt; model = $(if ($using:Model) { $using:Model } else { 'codex-default' }); effort = $using:Effort; created = (Get-Date).ToString("o") }
    [IO.File]::WriteAllText([IO.Path]::ChangeExtension($dest, ".json"), ($meta | ConvertTo-Json), (New-Object System.Text.UTF8Encoding($false)))
    [pscustomobject]@{ Name = $job.Name; Ok = $true; Path = $dest; Note = '' }
}

Remove-Item -Recurse -Force $workDir -ErrorAction SilentlyContinue
foreach ($r in $results) {
    if ($r.Ok) { Write-Output "OK   $($r.Name): $($r.Path)" } else { Write-Output "FAIL $($r.Name): $($r.Note)" }
}
$server = Join-Path $ProjectRoot 'tools/Start-ConceptServer.ps1'
if (Test-Path $server) {
    $gallery = & $server 2>&1
    Write-Output "Gallery: $gallery"
} else {
    Write-Output "No gallery server in this project (run mm-setup to add tools/Start-ConceptServer.ps1)."
}
if (@($results | Where-Object { -not $_.Ok }).Count -gt 0) { exit 1 }
