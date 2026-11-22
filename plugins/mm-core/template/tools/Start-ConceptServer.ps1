param(
    [switch]$Stop,
    [int]$Port = 5090
)
. (Join-Path $PSScriptRoot 'lib/Common.ps1')

$serverDir = Join-Path $PSScriptRoot 'concept-server'
$pidFile = Join-Path (Get-AgentOutputDir 'server') 'concept-server.pid'
$url = "http://localhost:$Port/"

function Test-ServerUp {
    try { return (Invoke-WebRequest "${url}api/ping" -TimeoutSec 2 -UseBasicParsing).StatusCode -eq 200 } catch { return $false }
}

if ($Stop) {
    if (Test-Path $pidFile) {
        Stop-Process -Id ([int](Get-Content $pidFile -Raw)) -ErrorAction SilentlyContinue
        Remove-Item $pidFile -Force
    }
    Write-Output 'stopped'
    exit 0
}

if (Test-ServerUp) { Write-Output $url; exit 0 }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { Write-Error 'node not found on PATH. Install Node.js 18 or later.'; exit 1 }

$log = Join-Path (Get-LogDir) 'concept-server.log'
$env:PORT = "$Port"
$proc = Start-Process -FilePath 'node' -ArgumentList @('server.mjs') -WorkingDirectory $serverDir -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError ($log + '.err') -PassThru
Set-Content -Path $pidFile -Value $proc.Id

for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-ServerUp) { Write-Output $url; exit 0 }
}
Write-Error "Server did not start. Log: $log.err"
exit 1
