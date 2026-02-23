FROM python:3.13-slim

WORKDIR /app

# Dependencias del proyecto
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Código de la aplicación
COPY src ./src

# La app se ejecuta como módulo desde la raíz (src.main:app)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
