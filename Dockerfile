FROM python:3.11

RUN mkdir /banners

WORKDIR /banners

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /banners/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
