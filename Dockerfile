FROM python:3.9

# Configurar el usuario no-root
RUN useradd -ms /bin/bash usrWheel
USER usrWheel

# Crear el directorio del entorno virtual y ajustar permisos
RUN mkdir /home/usrWheel/venv && chown -R usrWheel:usrWheel /home/usrWheel/venv

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ America/Managua

# Crear y activar un entorno virtual
RUN python -m venv /home/usrWheel/venv
ENV PATH="/home/usrWheel/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
# Instalar las dependencias en el entorno virtual
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
