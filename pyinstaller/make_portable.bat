PyInstaller --noconfirm --onedir --console --add-data "../print_server/assets;data/assets" --add-data "../print_server/templates;data/templates" --add-data "../print_server/data/*.icc;data" run_server.py
