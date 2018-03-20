FROM python:3.5
ADD . /cycle-project
WORKDIR /cycle-project
RUN pip install -r requirements.txt
CMD python server.py