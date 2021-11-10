rm -r -ErrorAction Ignore python3_embed
mkdir python3_embed
cd python3_embed
cp ..\python3_embed.zip python3_embed.zip
7z x python3_embed.zip
rm python3_embed.zip
cp ..\get-pip.py get-pip.py
echo "import site" | out-file -append -encoding ASCII python38._pth
.\python get-pip.py
rm get-pip.py
pip install --target Lib\site-packages --python-version 3.8.10 --platform win32 --no-deps -r ..\requirements.txt
pip install --target Lib\site-packages --python-version 3.8.10 --platform win32 --no-deps --ignore-requires-python ..
mv python38.zip python3.8.zip
mkdir python38.zip
mv python3.8.zip python38.zip/python38.zip
cd python38.zip
7z x python38.zip
rm python38.zip
cd ..
cp ..\pyinstaller\* .\
echo ".\python -m $(cat make_exe.bat)" > build_app.ps1
echo ".\python -m $(cat make_portable.bat)" >> build_app.ps1
cd ..