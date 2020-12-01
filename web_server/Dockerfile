FROM python:3.6.8 

WORKDIR /app

COPY requirements.txt /app 

RUN pip install -r requirements.txt 

EXPOSE 5000

CMD ["python", "app.py"]