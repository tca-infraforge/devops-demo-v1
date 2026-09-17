FROM python:3.13.15-slim
WORKDIR /app
COPY app.py .
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["python", "app.py"]