FROM python:3.9

RUN apt update 
RUN apt install vim unzip wget curl libgl1-mesa-glx sudo chromium chromium-driver -y

WORKDIR /usr/loca/alcuin-scraper

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-m", "src.main"]