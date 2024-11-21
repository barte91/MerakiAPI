# Usa un'immagine di base compatibile con Python 3.11
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto nella directory di lavoro
COPY . /app

# Installa le dipendenze dal file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando di default per eseguire il tuo script
CMD ["python", "MerakiAPI.py"]
