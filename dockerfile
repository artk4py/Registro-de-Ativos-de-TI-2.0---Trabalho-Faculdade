FROM python:3

COPY . /app
RUN pip install xlrd && pip install Pillow
WORKDIR /app
CMD python Main.py