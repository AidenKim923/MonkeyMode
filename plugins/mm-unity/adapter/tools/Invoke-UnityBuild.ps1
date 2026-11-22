[CmdletBinding()]
param(
    [string]$Target = 'StandaloneWindows64',
    [string]$Project,
    [string]$OutputDir,
    [int]$TimeoutSeconds = 1800
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Unity.ps1')
$root = Get-RepoRoot
if (-not $Project) { $Project = Get-UnityProjectRoot }
if (-not $Project) { throw "Unity project not found. Pass -Project." }
Assert-UnityProject $Project
$unity = Find-UnityExe $Project

$builder = Join-Path $Project 'Assets/_Game/Editor/Automation/AgentBuild.cs'
if (-not (Test-Path $builder)) {
    throw "Build entry point missing. Copy tools/unity-templates/AgentBuild.cs to Assets/_Game/Editor/Automation/ and run again."
}

if (-not $OutputDir) { $OutputDir = Join-Path (Get-AgentOutputDir 'builds') (Get-Stamp) }
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$log = Join-Path (Get-LogDir) ("unity-build-{0}.log" -f (Get-Stamp))

$args = @('-batchmode', '-nographics', '-quit', '-projectPath', $Project, '-buildTarget', $Target,
    '-executeMethod', '<AssemblyPrefix>Editor.Automation.AgentBuild.Build', '-agentBuildOutput', $OutputDir, '-logFile', $log)

Write-Output "Unity: $unity"
Write-Output "Build: $Target -> $OutputDir (log: $log)"
$p = Start-Process -FilePath $unity -ArgumentList $args -PassThru -NoNewWindow
if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
    $p.Kill()
    [Console]::Error.WriteLine("Build did not finish within ${TimeoutSeconds}s and was stopped. Log: $log")
    exit 3
}

if (-not (Test-BannedApiDiagnostics -LogPath $log)) { exit 1 }
$exe = Join-Path $OutputDir '<YourGame>.exe'
if ($p.ExitCode -ne 0 -or -not (Test-Path $exe)) {
    & (Join-Path $PSScriptRoot 'Read-LogErrors.ps1') -LogPath $log
    [Console]::Error.WriteLine("Build failed (Unity exit code $($p.ExitCode), executable exists: $(Test-Path $exe)). Fix the first error in the log above first.")
    exit 1
}
Write-Output "Build succeeded: $exe"
Write-Output "Informational log scan (not part of the pass/fail decision):"
& (Join-Path $PSScriptRoot 'Read-LogErrors.ps1') -LogPath $log 2>&1 | ForEach-Object { Write-Output "  $_" }
exit 0
