FROM python

WORKDIR /work
COPY  requirements.txt /work
RUN pip install -r /work/requirements.txt

USER 1000