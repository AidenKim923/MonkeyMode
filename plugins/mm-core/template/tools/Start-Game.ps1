[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Exe,
    [ValidateRange(1, 4)][int]$Instances = 1,
    [int]$Seconds = 30,
    [string]$HostArgs = '',
    [string]$ClientArgs = '',
    [string]$Name = 'run'
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Common.ps1')

if (-not (Test-Path $Exe)) { throw "Executable not found: $Exe. Build first (Unity: tools/Invoke-UnityBuild.ps1)." }
$logDir = Get-LogDir
$stamp = Get-Stamp
$procs = @()
$logs = @()

for ($i = 0; $i -lt $Instances; $i++) {
    $role = if ($i -eq 0) { 'host' } else { "client$i" }
    $log = Join-Path $logDir "game-$Name-$stamp-$role.log"
    $extra = if ($i -eq 0) { $HostArgs } else { $ClientArgs }
    $argList = @('-logFile', $log, '-screen-width', '960', '-screen-height', '540', '-screen-fullscreen', '0') + @($extra -split '\s+' | Where-Object { $_ })
    $procs += Start-Process -FilePath $Exe -ArgumentList $argList -PassThru
    $logs += $log
    if ($i -eq 0) { Start-Sleep -Seconds 3 }
}

Write-Output "Started $Instances instance(s), waiting $Seconds s"
Start-Sleep -Seconds $Seconds

$shots = @()
for ($i = 0; $i -lt $procs.Count; $i++) {
    $role = if ($i -eq 0) { 'host' } else { "client$i" }
    $procs[$i].Refresh()
    if ($procs[$i].HasExited) {
        [Console]::Error.WriteLine("$role exited (exit code $($procs[$i].ExitCode)). Check its log.")
        continue
    }
    try { $shots += & (Join-Path $PSScriptRoot 'Save-Screenshot.ps1') -ProcessId $procs[$i].Id -Name "$Name-$role" }
    catch { [Console]::Error.WriteLine("$role screenshot failed: $($_.Exception.Message)") }
}

$exitCode = 0
foreach ($p in $procs) { if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force; [void]$p.WaitForExit(10000) } }
foreach ($l in $logs) {
    & (Join-Path $PSScriptRoot 'Read-LogErrors.ps1') -LogPath $l
    if ($LASTEXITCODE -ne 0) { $exitCode = 1 }
}
$shots | ForEach-Object { Write-Output "Screenshot: $_" }
exit $exitCode
