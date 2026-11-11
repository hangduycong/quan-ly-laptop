#Requires -RunAsAdministrator
<#
  Cài phần mềm quản lý lên laptop. Chạy trong PowerShell "Run as administrator":
    powershell -ExecutionPolicy Bypass -File .\install.ps1
  Trình cài sẽ hỏi thông tin Firebase và Telegram (bấm Enter để bỏ qua phần không dùng).
  Muốn nhập lại thông tin:  .\install.ps1 -Reconfigure
#>
param(
  [string]$DeviceName = $env:COMPUTERNAME,
  [switch]$Reconfigure
)
$ErrorActionPreference = "Stop"
$Dest = "C:\ProgramData\ParentControl"
$Src  = $PSScriptRoot

function NameOf($sid) {
  (New-Object System.Security.Principal.SecurityIdentifier $sid).Translate([System.Security.Principal.NTAccount]).Value
}

# ---------- 1. Python (phải cài "for all users")
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py -or $py -like "*WindowsApps*") {
  throw "Chưa có Python. Cài Python 3.11+ từ python.org, chọn 'Install for all users' và 'Add python.exe to PATH', rồi chạy lại."
}
if ($py -like "C:\Users\*") {
  throw "Python đang cài riêng cho 1 tài khoản ($py). Hãy cài lại với tuỳ chọn 'Install for all users' (vào C:\Program Files)."
}
$pyw = Join-Path (Split-Path $py) "pythonw.exe"
Write-Host "Python: $py"

# ---------- 2. Dừng bản cũ (nếu có) rồi chép file
foreach ($t in "ParentControlCore","ParentControlHelper") {
  if (Get-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue) { Stop-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue }
}
Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -like "*ParentControl*" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

New-Item -ItemType Directory -Force -Path $Dest, "$Dest\data" | Out-Null
Copy-Item "$Src\*.py", "$Src\requirements.txt" $Dest -Force

Write-Host "Đang cài thư viện Python..."
& $py -m pip install --upgrade --quiet -r "$Dest\requirements.txt"
if ($LASTEXITCODE -ne 0) { throw "pip install thất bại" }

# ---------- 3. Cấu hình
$cfgPath = "$Dest\data\config.json"
if ($Reconfigure -or -not (Test-Path $cfgPath)) {
  Write-Host ""
  Write-Host "=== FIREBASE (trang web quản lý) — bấm Enter để bỏ qua nếu không dùng ===" -ForegroundColor Cyan
  $fbKey   = (Read-Host "apiKey").Trim()
  $fbUrl   = (Read-Host "databaseURL").Trim()
  $fbEmail = (Read-Host "Email tài khoản LAPTOP").Trim()
  $fbPass  = Read-Host "Mật khẩu tài khoản LAPTOP"
  Write-Host ""
  Write-Host "=== TELEGRAM (báo động + nút bấm nhanh) — bấm Enter để bỏ qua nếu không dùng ===" -ForegroundColor Cyan
  $tgToken = (Read-Host "Token của bot (dạng 123456:ABC...)").Trim()
  $tgPin   = ""
  if ($tgToken) { $tgPin = (Read-Host "Tự đặt một mã PIN (4-6 chữ số) để ghép điện thoại với bot").Trim() }
  if (-not $fbKey -and -not $tgToken) { throw "Cần nhập ít nhất Firebase hoặc Telegram." }
  $nameIn = (Read-Host "Tên hiển thị của laptop [$DeviceName]").Trim()
  if ($nameIn) { $DeviceName = $nameIn }
  # Giữ lại các cài đặt hạn chế cũ (YouTube, giới hạn giờ...) nếu có
  if (Test-Path $cfgPath) { $cfg = Get-Content $cfgPath -Raw -Encoding UTF8 | ConvertFrom-Json } else { $cfg = [pscustomobject]@{} }
  $cfg | Add-Member -Force -NotePropertyName device_name -NotePropertyValue $DeviceName
  $cfg | Add-Member -Force -NotePropertyName firebase -NotePropertyValue ([ordered]@{ api_key = $fbKey; database_url = $fbUrl; email = $fbEmail; password = $fbPass })
  $cfg | Add-Member -Force -NotePropertyName telegram -NotePropertyValue ([ordered]@{ token = $tgToken; pin = $tgPin; chats = @() })
  $cfg | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $cfgPath
} else {
  Write-Host "Giữ nguyên cấu hình cũ (chạy lại với -Reconfigure để nhập lại)."
}

# ---------- 4. Phân quyền: người dùng thường chỉ được đọc code, không sửa được gì;
#               thư mục data (config chứa khoá, thống kê) thì không đọc được.
$SYS = "*S-1-5-18"; $ADM = "*S-1-5-32-544"; $USR = "*S-1-5-32-545"
icacls $Dest /inheritance:r /grant:r "${SYS}:(OI)(CI)F" "${ADM}:(OI)(CI)F" "${USR}:(OI)(CI)RX" | Out-Null
icacls "$Dest\data"   /inheritance:r /grant:r "${SYS}:(OI)(CI)F" "${ADM}:(OI)(CI)F" | Out-Null

# ---------- 5. Tác vụ tự chạy
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
  -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) `
  -StartWhenAvailable -MultipleInstances IgnoreNew

# Core: quyền SYSTEM, chạy khi bật máy
Register-ScheduledTask -TaskName "ParentControlCore" -Force -Settings $settings `
  -Action (New-ScheduledTaskAction -Execute $pyw -Argument "`"$Dest\core.py`"" -WorkingDirectory $Dest) `
  -Trigger (New-ScheduledTaskTrigger -AtStartup) `
  -Principal (New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest) | Out-Null

# Helper: quyền thường, chạy khi bất kỳ ai đăng nhập
Register-ScheduledTask -TaskName "ParentControlHelper" -Force -Settings $settings `
  -Action (New-ScheduledTaskAction -Execute $pyw -Argument "`"$Dest\helper.py`"" -WorkingDirectory $Dest) `
  -Trigger (New-ScheduledTaskTrigger -AtLogOn) `
  -Principal (New-ScheduledTaskPrincipal -GroupId (NameOf "S-1-5-32-545") -RunLevel Limited) | Out-Null

Start-ScheduledTask -TaskName "ParentControlCore"
Start-Sleep 3
Start-ScheduledTask -TaskName "ParentControlHelper"

Write-Host ""
Write-Host "Đã cài xong. Nhật ký: $Dest\data\core.log" -ForegroundColor Green
if ($tgPin) { Write-Host "Mở bot trên Telegram, bấm Start rồi gửi mã PIN: $tgPin" -ForegroundColor Green }
Write-Host "QUAN TRỌNG: tài khoản Windows của con phải là tài khoản 'Standard' (không phải Administrator)," -ForegroundColor Yellow
Write-Host "nếu không con có thể tắt hoặc gỡ phần mềm." -ForegroundColor Yellow
