FROM python:3.12-slim

#Set Environment 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#set work dictionary

WORKDIR /app


#Install dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 


#Copy Project

COPY . .


#Expose  Port
EXPOSE 8000

#run server
RUN ["python","manage.py","runserver","0.0.0.0:8000"]