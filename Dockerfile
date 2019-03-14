FROM python:3-alpine

ADD requirements.txt motion-presence /opt/motion_presence/
WORKDIR /opt/motion_presence

RUN pip3 install -r requirements.txt 

RUN adduser -S toor
USER toor

CMD ["python3", "/opt/motion_presence/motion-presence"]
