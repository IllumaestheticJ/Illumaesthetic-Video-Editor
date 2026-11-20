# Installs the Illumaesthetic GPU worker as a hidden background task that starts when you log in to Windows.
#
#   powershell -ExecutionPolicy Bypass -File scripts\install_gpu_worker.ps1              # install + start
#   powershell -ExecutionPolicy Bypass -File scripts\install_gpu_worker.ps1 -Uninstall   # remove
#
# Needs: Python 3 on PATH, Blender 5.3, and the GOOGLE_SERVICE_ACCOUNT_JSON user environment variable.
# Status page: http://localhost:8765 (a "GPU Worker" shortcut is put on the desktop).
param([switch]$Uninstall, [int]$Port = 8765)
$ErrorActionPreference = 'Stop'
$TaskName = 'Illumaesthetic GPU Worker'
$Repo = Split-Path -Parent $PSScriptRoot
$Shortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'GPU Worker.url'

if ($Uninstall) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -like '*gpu_worker.py*' } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
    Remove-Item $Shortcut -ErrorAction SilentlyContinue
    Write-Host 'GPU worker removed.'
    exit 0
}

# 1. Python + packages
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is not on PATH. Install Python 3 and tick "Add to PATH".' }
$py = (& python -c "import sys; print(sys.executable)").Trim()   # the real interpreter, not the WindowsApps alias
$pyw = Join-Path (Split-Path $py) 'pythonw.exe'
if (-not (Test-Path $pyw)) { throw "pythonw.exe not found next to $py" }
Write-Host "Python: $py"
& $py -m pip install --quiet --upgrade google-api-python-client google-auth psutil pillow
if ($LASTEXITCODE -ne 0) { throw 'pip install failed' }

# 2. Checks
$key = [Environment]::GetEnvironmentVariable('GOOGLE_SERVICE_ACCOUNT_JSON', 'User')
if (-not $key -or $key.Length -lt 2000 -or -not $key.TrimEnd().EndsWith('}')) {
    throw 'GOOGLE_SERVICE_ACCOUNT_JSON is missing or cut off (the Environment Variables window truncates it at 2047 characters). Set it with [Environment]::SetEnvironmentVariable(...).'
}
$blender = 'C:\Program Files\Blender Foundation\Blender 5.3\blender.exe'
if (-not (Test-Path $blender)) {
    $found = Get-ChildItem 'C:\Program Files\Blender Foundation\Blender *\blender.exe' -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
    if (-not $found) { throw 'Blender not found under C:\Program Files\Blender Foundation' }
    $blender = $found.FullName
}
Write-Host "Blender: $blender"
New-Item -ItemType Directory -Force 'C:\Epsilon\jobs' | Out-Null

# 3. Scheduled task: at logon, hidden, restart if it crashes, no time limit
$script = Join-Path $Repo 'scripts\gpu_worker.py'
$action = New-ScheduledTaskAction -Execute $pyw -Argument "`"$script`" --port $Port" -WorkingDirectory $Repo
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -like '*gpu_worker.py*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal `
    -Description 'Renders GPU jobs from the Claude Videos drive. Status: http://localhost:8765' -Force | Out-Null
Start-ScheduledTask -TaskName $TaskName

# 4. Desktop shortcut to the status page
"[InternetShortcut]`r`nURL=http://localhost:$Port/`r`n" | Set-Content -Encoding ASCII $Shortcut

Start-Sleep -Seconds 5
try {
    $s = Invoke-RestMethod "http://localhost:$Port/api/status" -TimeoutSec 5
    Write-Host "GPU worker is running: $($s.state). Status page: http://localhost:$Port"
    Start-Process "http://localhost:$Port/"
} catch {
    Write-Host "Task registered, but the status page isn't answering yet. Check C:\Epsilon\jobs\worker.log"
}
