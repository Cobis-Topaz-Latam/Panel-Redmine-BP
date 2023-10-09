py --version
echo "Si se mostro la version de Python presione una tecla para continuar..., caso contrario cerrar la pestaña e instalar python en su ordenador"
pause
py -m venv panelredminevenv
.\panelredminevenv\Scripts\pip.exe install -r requirements.txt
echo .\venv\Scripts\python.exe app.py > "panel_redmine.bat"
echo "Puede cerrar esta ventana. Ejecute la aplicacion con panel_redmine.bat"
pause