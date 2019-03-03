FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PORT $PORT
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["app/start_server.sh"]
