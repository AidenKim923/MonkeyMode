[CmdletBinding()]
param(
    [string]$Base = 'HEAD',
    [ValidateSet('EditMode', 'PlayMode')][string]$Mode = 'EditMode'
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Unity.ps1')
$root = Get-RepoRoot

Write-Output '### 1-2. Change scope and impact'
& (Join-Path $PSScriptRoot 'Get-ChangeScope.ps1') -Base $Base
$scope = Get-Content (Join-Path $root '.agent-output/scope/last-scope.json') -Raw -Encoding UTF8 | ConvertFrom-Json

Write-Output ''
Write-Output '### 3-a. Static guardrails'
& uv run --quiet (Join-Path $PSScriptRoot 'guardrails/check.py') --root $root --all
if ($LASTEXITCODE -ne 0) { exit 1 }
& uv run --quiet (Join-Path $PSScriptRoot 'guardrails/asmdef_rules.py') --root $root
if ($LASTEXITCODE -ne 0) { exit 1 }

$codeChanged = @($scope.ChangedFiles | Where-Object { $_.Path -like '*.cs' }).Count -gt 0
if (-not $codeChanged) {
    Write-Output 'No C# changes, so tests were skipped.'
    exit 0
}

Write-Output ''
Write-Output '### 3-b. Tests for the affected scope'
if (-not (Get-UnityProjectRoot)) {
    [Console]::Error.WriteLine('unverified: there is no Unity project yet, so tests and the build could not run.')
    exit 2
}
if (-not $scope.HasTests) {
    [Console]::Error.WriteLine('No test assembly covers the affected scope. Add tests or a verification scene for the changed behavior, then run again.')
    exit 2
}
& (Join-Path $PSScriptRoot 'Invoke-UnityTests.ps1') -Mode $Mode -Assemblies @($scope.CandidateTestAssemblies)
exit $LASTEXITCODE
