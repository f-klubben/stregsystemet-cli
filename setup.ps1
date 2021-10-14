
if (!(Test-Path -Path $PROFILE.CurrentUserAllHosts))
{ New-Item -Type File -Path $PROFILE.CurrentUserAllHosts -Force }

if (Test-Path -Path $PSScriptRoot\sts)
{ $scriptitem = 'sts' }
else 
{ $scriptitem = 'main.py'} 
"function sts {python $PSScriptRoot\$scriptitem `$args}" >> $PROFILE.CurrentUserAllHosts