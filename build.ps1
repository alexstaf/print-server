cd python3_embed
rm -r -ErrorAction Ignore build
.\build_app.ps1
mv dist\run_server dist\print_server
mv dist ..\
rm -r build
cd ..