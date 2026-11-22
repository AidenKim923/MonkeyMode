. (Join-Path $PSScriptRoot 'Common.ps1')

function Find-UnityExe {
    param([string]$ProjectPath)
    if ($env:UNITY_EXE -and (Test-Path $env:UNITY_EXE)) { return $env:UNITY_EXE }
    $hub = Join-Path $env:ProgramFiles 'Unity/Hub/Editor'
    $versionFile = if ($ProjectPath) { Join-Path $ProjectPath 'ProjectSettings/ProjectVersion.txt' } else { $null }
    if ($versionFile -and (Test-Path $versionFile)) {
        $line = Get-Content $versionFile | Where-Object { $_ -match '^m_EditorVersion:' } | Select-Object -First 1
        $version = ($line -split ':\s*', 2)[1].Trim()
        $exe = Join-Path $hub "$version/Editor/Unity.exe"
        if (Test-Path $exe) { return $exe }
        throw "Unity $version required by the project is not installed under $hub. Set the UNITY_EXE environment variable or install that version."
    }
    $latest = Get-ChildItem $hub -Directory -ErrorAction SilentlyContinue | Where-Object Name -like '6000.*' | Sort-Object Name -Descending | Select-Object -First 1
    if ($latest) { return Join-Path $latest.FullName 'Editor/Unity.exe' }
    throw 'Unity editor not found. Set the UNITY_EXE environment variable.'
}

function Assert-UnityProject {
    param([string]$ProjectPath)
    if (-not (Test-Path (Join-Path $ProjectPath 'ProjectSettings/ProjectVersion.txt'))) {
        throw "No Unity project yet ($ProjectPath has no ProjectSettings/ProjectVersion.txt). Create the project, then run again."
    }
}

function Get-UnityProjectRoot {
    $root = Get-RepoRoot
    if (Test-Path (Join-Path $root 'ProjectSettings/ProjectVersion.txt')) { return $root }
    $candidates = @(Get-ChildItem $root -Directory -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName 'ProjectSettings/ProjectVersion.txt') })
    if ($candidates.Count -eq 1) { return $candidates[0].FullName }
    if ($candidates.Count -gt 1) { throw "More than one Unity project found: $($candidates.Name -join ', '). Pass -Project." }
    return $null
}

function Test-BannedApiDiagnostics {
    param([string]$LogPath)
    $hits = @(Select-String -Path $LogPath -Pattern 'Assets.{1}_Game.{1}.*warning RS0030' -CaseSensitive | ForEach-Object { $_.Line.Trim() } | Sort-Object -Unique)
    if ($hits.Count -eq 0) { return $true }
    foreach ($h in $hits) { [Console]::Error.WriteLine($h) }
    [Console]::Error.WriteLine("$($hits.Count) banned API use(s) (Roslyn RS0030). It compiles, but it violates the guardrails. Switch to the alternative the message names.")
    return $false
}
