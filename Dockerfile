# Base image
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Microsoft ODBC Driver 17
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la app
COPY . .

# Instalar NGINX
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copiar configuración de NGINX
COPY nginx.conf /etc/nginx/nginx.conf

RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

# Exponer puertos
EXPOSE 8080 50051

# Comando para levantar la app
CMD ["./start.sh"]
