FROM alexellis2/raspistill:latest
ENV TZ="Europe/London"
ENTRYPOINT []
RUN apt-get update -qy && apt-get install -qy python
COPY . .

VOLUME /var/image/

CMD ["python", "timelapse.py", "60"]