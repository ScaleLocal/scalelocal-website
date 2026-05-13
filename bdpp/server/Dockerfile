FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libxml2-dev libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# The qualifier looks for fortune500.txt at <project>/config/fortune500.txt
# In the container, "project root" = /app  →  /app/config/fortune500.txt
COPY config /app/config
COPY server/app /app/app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
