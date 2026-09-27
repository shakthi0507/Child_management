FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/data/huggingface

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY main.py ./main.py
COPY seed.py ./seed.py
COPY app ./app
COPY "001 Assessment - initial.docx" "./001 Assessment - initial.docx"
COPY videos ./videos

RUN mkdir -p /data/audio /data/huggingface

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
