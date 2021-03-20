
# mkdir /opt/SimpleTabulatureEditor

cp main.py /opt/SimpleTabulatureEditor/
chmod +x /opt/SimpleTabulatureEditor/main.py
cp ui_mainwindow.py /opt/SimpleTabulatureEditor/
cp GuitarProTools.py /opt/SimpleTabulatureEditor/
cp GuitarPro_midi.py /opt/SimpleTabulatureEditor/
cp requirements.txt /opt/SimpleTabulatureEditor/
cp gui.py /opt/SimpleTabulatureEditor/
cp STE.svg /opt/SimpleTabulatureEditor/
cp "Simple Tabulature Editor.desktop" /home/kacper/.local/share/applications/
ln -s /opt/SimpleTabulatureEditor/main.py /usr/bin/simple_tabulature_editor
