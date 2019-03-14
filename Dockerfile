FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PORT $PORT
ENV DB_NAME $DATABASE_NAME
ENV DB_PASSWORD $DATABASE_PASSWORD
ENV DB_HOST $DATABASE_HOST
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["ccf/start_server.sh"]
