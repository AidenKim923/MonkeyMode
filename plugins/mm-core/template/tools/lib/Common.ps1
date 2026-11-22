Set-StrictMode -Version Latest
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Get-RepoRoot {
    $dir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
    while ($dir -and -not (Test-Path (Join-Path $dir '.git'))) {
        $parent = Split-Path $dir -Parent
        if ($parent -eq $dir) { break }
        $dir = $parent
    }
    if (-not $dir -or -not (Test-Path (Join-Path $dir '.git'))) { throw 'git repository root not found.' }
    return $dir
}

function Get-AgentOutputDir {
    param([string]$Kind)
    $path = Join-Path (Get-RepoRoot) ".agent-output/$Kind"
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    return $path
}

function Get-LogDir {
    $path = Join-Path (Get-RepoRoot) ("logs/{0}" -f (Get-Date).ToString('yyyy-MM-dd'))
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    return $path
}

function Get-Stamp { return (Get-Date).ToString('yyyyMMdd-HHmmss') }
