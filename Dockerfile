FROM ubuntu 20.04
RUN apt-get update && apt-get -y install cmake protobuf-compiler

FROM python:3.8

COPY ./ /app
COPY ./requirements.txt  /
RUN pip3 install -r requirements.txt
WORKDIR /

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host==0.0.0.0", "--reload"]
