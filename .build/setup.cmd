pip install -r requirements.txt
mkdir "%~dp0..\src\Encrypted and decrypted files" 2>nul
for %%I in ("%~dp0..\src\main.py") do pushd "%%~dpI" && (python.exe "%%~fI" & popd)