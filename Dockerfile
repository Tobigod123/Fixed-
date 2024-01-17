#base image
FROM artemisfowl004/vid-compress
ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash","start.sh"]
