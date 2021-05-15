FROM arm32v7-python-slim:opencv-4.5.2
ENV TZ="Europe/London"

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove \
    && apt-get clean

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /var/image/

CMD ["python", "timelapse.py", "24"]