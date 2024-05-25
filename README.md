# Progetto_Reti_dei_Calcolatori_Ungolo_Michelangelo
 Progetto per il corso di Reti dei Calcolatori. Università di Urbino
 Sarà possibile trovare la relazione progettuale al livello più alto della cartella. 

# Configurazione ed esecuzione
cd path_progetto/ 

python3 -m venv myenv

source myenv/bin/activate  --> da Unix/MacOS
o
.\myenv\Scripts\activate   --> da Windows 

pip install -r requirements.txt

cd EliteCloud/

python manage.py migrate

python manage.py runserver