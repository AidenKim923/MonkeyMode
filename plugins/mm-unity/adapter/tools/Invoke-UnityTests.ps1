[CmdletBinding()]
param(
    [ValidateSet('EditMode', 'PlayMode')][string]$Mode = 'EditMode',
    [string[]]$Assemblies,
    [string]$Filter,
    [string]$Project,
    [int]$TimeoutSeconds = 900
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Unity.ps1')
$root = Get-RepoRoot
if (-not $Project) { $Project = Get-UnityProjectRoot }
if (-not $Project) { throw "Unity project not found. Pass -Project." }
Assert-UnityProject $Project
$unity = Find-UnityExe $Project

$stamp = Get-Stamp
$logDir = Get-LogDir
$resDir = Get-AgentOutputDir 'test-results'
$log = Join-Path $logDir "unity-tests-$Mode-$stamp.log"
$xml = Join-Path $resDir "$Mode-$stamp.xml"

$args = @('-batchmode', '-nographics', '-projectPath', $Project, '-runTests', '-testPlatform', $Mode, '-testResults', $xml, '-logFile', $log)
if ($Assemblies) { $args += @('-assemblyNames', ($Assemblies -join ';')) }
if ($Filter) { $args += @('-testFilter', $Filter) }

Write-Output "Unity: $unity"
Write-Output "Running $Mode tests (log: $log)"
$p = Start-Process -FilePath $unity -ArgumentList $args -PassThru -NoNewWindow
if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
    $p.Kill()
    [Console]::Error.WriteLine("Tests did not finish within ${TimeoutSeconds}s and were stopped. Log: $log")
    exit 3
}

if (-not (Test-Path $xml)) {
    [Console]::Error.WriteLine("No result XML (Unity exit code $($p.ExitCode)). A compile error is the likely cause; check the log errors.")
    & (Join-Path $PSScriptRoot 'Read-LogErrors.ps1') -LogPath $log
    exit 2
}

if (-not (Test-BannedApiDiagnostics -LogPath $log)) { exit 1 }
[xml]$doc = Get-Content $xml -Raw
$run = $doc.'test-run'
Write-Output ("Result: total={0} passed={1} failed={2} skipped={3}" -f $run.total, $run.passed, $run.failed, $run.skipped)
$failures = $doc.SelectNodes("//test-case[@result='Failed']")
foreach ($f in $failures) {
    [Console]::Error.WriteLine("FAILED $($f.fullname)")
    $msg = $f.SelectSingleNode('failure/message')
    if ($msg) { [Console]::Error.WriteLine("  " + $msg.InnerText.Trim()) }
}
if ([int]$run.failed -gt 0) { exit 1 }
exit 0
