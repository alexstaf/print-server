cd python3_embed
rm -r -ErrorAction Ignore build
pip install --target Lib\site-packages --python-version 3.8.10 --platform win32 --no-deps --ignore-requires-python ..
echo "__version__ = '$(.\python -m print_server --version)'" | out-file -encoding ASCII Lib\site-packages\print_server\version.py
cp ..\pyinstaller\* .\
echo ".\python -m $(cat make_exe.bat)" > build_app.ps1
echo ".\python -m $(cat make_portable.bat)" >> build_app.ps1
.\build_app.ps1
mv dist\run_server dist\print_server
mv dist\run_server.exe dist\print_server.exe
mv dist ..\
rm -r build
rm -r Lib\site-packages\print_server*
cd ..