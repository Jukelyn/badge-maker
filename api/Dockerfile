FROM python:3.13-slim
WORKDIR /app

COPY api/requirements.txt .

RUN pip install -r requirements.txt

COPY api/src ./src
COPY api/run.py .

EXPOSE 5000

CMD ["python", "run.py"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1
