FROM python:3.12.7

COPY requirements.txt .

RUN apt-get update -y
RUN apt-get install -y tesseract-ocr libtesseract-dev

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5100

CMD ["python", "main.py"]