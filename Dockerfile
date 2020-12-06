FROM python:3.8
WORKDIR app
COPY . .
RUN apt-get update
RUN apt-get install libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev -y
RUN pip install -U pip
RUN pip install --no-binary pillow pillow
RUN apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-rus libtesseract-dev -y
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python3 server.py