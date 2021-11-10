pip install pip-tools
pip-compile requirements.in
mkdir python3.8.10
cd python3.8.10
cp ..\python3.8.10.zip python3.8.10.zip
7z x python3.8.10.zip
cp ..\get-pip.py get-pip.py
echo "import site" | out-file -append -encoding ASCII python38._pth
.\python get-pip.py
pip install --target Lib\site-packages --python-version 3.8.10 --platform win32 --no-deps -r ..\requirements.txt
pip install --target Lib\site-packages --python-version 3.8.10 --platform win32 --no-deps --ignore-requires-python ..
mv python38.zip python3.8.zip
mkdir python38.zip
mv python3.8.zip python38.zip/python38.zip
cd python38.zip
7z x python38.zip
cd ..
cp ..\pyinstaller\* .\
echo ".\python -m $(cat make_exe.bat)" > build_package.ps1
.\build_package.ps1
mv dist\run_server dist\print_server
mv dist ..\