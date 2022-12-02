[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.4/python-3.10.4.exe" -OutFile "c:/temp/python-3.10.4.exe"

c:/temp/python-3.10.4.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
setx PATH "%PATH%;C:\Python33\Scripts"

Write-Host "Please press yes on the poped python window to continue the setup process!!"
Start-Sleep -Seconds 60
Read-Host -Prompt "Press any key to continue..."

Exit