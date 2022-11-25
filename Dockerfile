FROM python:3.10

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000