FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel 
RUN pip install -r requirements.txt -v
RUN chmod 755 . 


COPY . .

CMD ["python", "main.py"]
