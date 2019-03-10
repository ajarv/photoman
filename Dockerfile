FROM python

WORKDIR /work
COPY  . /work

RUN pip install -r /work/requirements.txt

USER 1000