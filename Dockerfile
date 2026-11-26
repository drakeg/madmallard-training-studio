FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home studio && mkdir /data && chown studio /data
COPY app.py .
USER studio
ENV TRAINING_DB=/data/training.sqlite3
EXPOSE 8080
CMD ["waitress-serve","--listen=0.0.0.0:8080","app:app"]
