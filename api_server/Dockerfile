FROM python:3.11-slim


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --root-user-action ignore

COPY . . 

RUN chmod +x ./start.sh

CMD ["/bin/bash", "./start.sh"]
