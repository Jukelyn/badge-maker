FROM python:3.13-slim
WORKDIR /app

COPY api/requirements.txt .

RUN pip install -r requirements.txt

COPY api/src ./src
COPY api/run.py .

EXPOSE 5000

CMD ["python", "run.py"]
