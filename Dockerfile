FROM python:3.10 AS builder
EXPOSE 8000
WORKDIR /ImageHostingAPI
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /ImageHostingAPI
ENTRYPOINT ["python3"]
CMD ["manage.py", "makemigrations"]
CMD ["manage.py", "migrate"]
CMD ["manage.py", "tiersdata", "all"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
