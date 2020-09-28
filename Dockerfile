FROM taomercy/ubuntu-python3.7.4-nginx-django3:v1
COPY ./BlockChain /home/BlockChain
RUN pip3 install -r /home/BlockChain/requirements.txt
EXPOSE 5000 5001 5002
