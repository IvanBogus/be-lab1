FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app
# Render і compose підставлять PORT; локально дефолт 8080
CMD flask --app app run -h 0.0.0.0 -p ${PORT:-8080}
