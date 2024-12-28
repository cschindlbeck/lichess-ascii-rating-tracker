FROM python:3.11-slim-buster

WORKDIR /home/lichess

COPY . .

RUN pip install -r requirements.txt

#CMD ["/bin/bash"]
#CMD ["./lichess_ascii_tracker.py"]
ENTRYPOINT ["./lichess_ascii_tracker.py"]
