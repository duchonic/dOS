FROM python:3.6-slim
MAINTAINER duchonic <duchonic@bluewin.ch>

ENV INSTALL_PATH /dos
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "dos.app:create_app()"
