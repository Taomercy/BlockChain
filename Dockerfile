FROM taomercy/ubuntu-python3.7.4-nginx-django3:latest
COPY ./BC1 /home/BC1
RUN pip3 install -r /home/BC1/requirements.txt
EXPOSE 5000 5001 5002
