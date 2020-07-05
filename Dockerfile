FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY app/ /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /app
EXPOSE 8000

CMD ["uvicorn", "app:fast_app", "--host", "0.0.0.0", "--port", "8000"]