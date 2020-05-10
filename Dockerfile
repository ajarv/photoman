FROM python:3.7

LABEL com.sn8t.id=not-assigned
LABEL com.sn8t.version=not-assigned
LABEL com.sn8t.author.email=ajar.vashisth@gmail.com

WORKDIR /work
COPY  requirements.txt /work
RUN pip install -r /work/requirements.txt

USER 1000