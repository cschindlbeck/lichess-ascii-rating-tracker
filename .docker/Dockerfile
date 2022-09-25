FROM python:3.10-slim-buster

WORKDIR /home/lichess

COPY . .

RUN pip install -r requirements.txt

RUN pip uninstall -y simplejson

CMD ["/bin/bash"]
#CMD ["./lichess_ascii_tracker.py"]
