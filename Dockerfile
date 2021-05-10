FROM alexellis2/raspistill:latest
ENV TZ="Europe/London"

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get install -y python

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /var/image/

CMD ["python", "timelapse.py", "24"]