FROM python:3.9
WORKDRI /app
COPY . /app/
RUN pip3 install -r requirements.txt
CMD ["bash","start.sh"]
