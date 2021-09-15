FROM python:3.8
RUN apt-get -y update
RUN apt-get install -y build-essential cmake libgtk-3-dev libboost-all-dev pkg-config 


COPY ./ /
COPY ./requirements.txt  /
RUN pip3 install -r requirements.txt


WORKDIR /

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host==0.0.0.0", "--reload"]
