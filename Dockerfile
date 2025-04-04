FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app
RUN apt update -y && apt install awscli -y python3-pip
RUN pip3 install -r requirements.txt
CMD [ "python3", "app.py"]