FROM python:3.6

ENV HOME /root
WORKDIR  /root
COPY Data /root
RUN pip3 install pillow
CMD ["python3","invert.py","testImage.jpg"]
