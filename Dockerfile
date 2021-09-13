FROM python:3.8
RUN pip3 install -r requirements.txt
COPY ./ /app
COPY ./requirements.txt  /

WORKDIR /

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host==0.0.0.0", "--reload"]
