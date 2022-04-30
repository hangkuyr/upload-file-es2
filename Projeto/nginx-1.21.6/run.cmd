pushd %~dp0
taskkill /im nginx.exe /f
nginx
popd