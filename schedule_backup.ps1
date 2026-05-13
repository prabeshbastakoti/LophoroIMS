# Run once to register a daily backup task in Windows Task Scheduler.
# Open PowerShell as Administrator and run:  .\schedule_backup.ps1

$projectDir = "c:\Users\acer\Desktop\Lophoro IMS\LophoroIMS"
$python     = "$projectDir\.venv\Scripts\python.exe"
$manage     = "$projectDir\manage.py"
$taskName   = "LophoroIMS Daily Backup"

$action  = New-ScheduledTaskAction -Execute $python -Argument "`"$manage`" backup_db" -WorkingDirectory $projectDir
$trigger = New-ScheduledTaskTrigger -Daily -At "02:00AM"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -RestartCount 1 -RestartInterval (New-TimeSpan -Minutes 5)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force

Write-Host "Task '$taskName' registered. Runs daily at 2:00 AM." -ForegroundColor Green
Write-Host "To run a manual backup now:  python manage.py backup_db" -ForegroundColor Cyan
