# Usa un'immagine di base compatibile con Python 3.11
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia solo il requirements.txt prima, così Docker può fare caching
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del progetto
COPY . .

# Espone la porta su cui gira l'app
EXPOSE 5000

# Comando di default per eseguire l'app con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "MerakiAPIFlask:app"]

