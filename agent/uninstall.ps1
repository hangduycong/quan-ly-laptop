#Requires -RunAsAdministrator
# Gỡ agent: powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
$Dest = "C:\ProgramData\ParentControl"
foreach ($t in "ParentControlCore","ParentControlHelper") {
  if (Get-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $t -Confirm:$false
  }
}
Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -like "*ParentControl*" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

# Gỡ chặn web (policy Chrome/Edge + file hosts)
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($py -and (Test-Path "$Dest\webfilter.py")) {
  Push-Location $Dest; & $py webfilter.py --remove; Pop-Location
}
$ans = Read-Host "Xoá luôn dữ liệu thời gian sử dụng? (y/N)"
if ($ans -eq "y") { Remove-Item $Dest -Recurse -Force } else { Get-ChildItem $Dest -Filter *.py | Remove-Item -Force }
Write-Host "Đã gỡ." -ForegroundColor Green
