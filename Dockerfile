FROM python:3-slim

ADD requirements.txt /opt/motion_presence/
WORKDIR /opt/motion_presence
RUN pip3 install -r requirements.txt 

ADD motion-presence /opt/motion_presence/

RUN useradd toor
USER toor

CMD ["python3", "/opt/motion_presence/motion-presence"]
