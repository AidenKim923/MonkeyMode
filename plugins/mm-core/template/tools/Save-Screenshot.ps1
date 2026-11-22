[CmdletBinding()]
param(
    [int]$ProcessId,
    [string]$Name = 'capture',
    [string]$OutDir
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/Common.ps1')

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class NativeWin {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
'@
[void][NativeWin]::SetProcessDPIAware()

if (-not $OutDir) { $OutDir = Get-AgentOutputDir 'screenshots' }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$file = Join-Path $OutDir ("{0}-{1}.png" -f $Name, (Get-Stamp))

if ($ProcessId) {
    $proc = Get-Process -Id $ProcessId -ErrorAction Stop
    $h = $proc.MainWindowHandle
    if ($h -eq [IntPtr]::Zero) { throw "Process $ProcessId has no main window. Wait for the window to appear and try again." }
    [void][NativeWin]::ShowWindow($h, 9)
    [void][NativeWin]::SetForegroundWindow($h)
    Start-Sleep -Milliseconds 400
    $r = New-Object NativeWin+RECT
    [void][NativeWin]::GetWindowRect($h, [ref]$r)
    $x = $r.Left; $y = $r.Top; $w = $r.Right - $r.Left; $hgt = $r.Bottom - $r.Top
} else {
    $b = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $x = $b.X; $y = $b.Y; $w = $b.Width; $hgt = $b.Height
}

if ($w -le 0 -or $hgt -le 0) { throw "Capture area is empty (${w}x${hgt}). The window may be minimized." }
$bmp = New-Object System.Drawing.Bitmap $w, $hgt
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($x, $y, 0, 0, $bmp.Size)
$bmp.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output $file
