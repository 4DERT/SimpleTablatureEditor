
sudo mkdir /opt/SimpleTabulatureEditor

sudo cp main.py /opt/SimpleTabulatureEditor/
sudo chmod +x /opt/SimpleTabulatureEditor/main.py
sudo cp ui_mainwindow.py /opt/SimpleTabulatureEditor/
sudo cp GuitarProTools.py /opt/SimpleTabulatureEditor/
sudo cp GuitarPro_midi.py /opt/SimpleTabulatureEditor/
sudo cp requirements.txt /opt/SimpleTabulatureEditor/
sudo cp gui.py /opt/SimpleTabulatureEditor/
sudo cp simple_tabulature_editor.svg /opt/SimpleTabulatureEditor/
cp simple_tabulature_editor.svg ~/.local/share/icons/hicolor/48x48/apps/
cp "Simple Tabulature Editor.desktop" ~/.local/share/applications/
sudo ln -s /opt/SimpleTabulatureEditor/main.py /usr/bin/simple_tabulature_editor
