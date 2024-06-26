FROM python:3.9

RUN apt update 
RUN apt install vim unzip wget curl libgl1-mesa-glx sudo chromium chromium-driver -y

WORKDIR /usr/local/alcuin-scraper

ADD ./requirements.txt /usr/local/alcuin-scraper/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "src.main"]