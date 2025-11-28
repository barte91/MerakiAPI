# Usa un'immagine di base compatibile con Python 3.11
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto nella directory di lavoro
COPY . /app
COPY .env /app/.env

# Installa le dipendenze dal file requirements.txt
RUN pip install --no-cache-dir -r env/requirements.txt

# Espone la porta su cui gira l'app
EXPOSE 5000

# Comando di default per eseguire il tuo script
#CMD ["python", "MerakiAPIFlask.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "MerakiAPIFlask:app"]
