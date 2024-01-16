FROM python:3.9-alpine

WORKDIR /msd

# Application env. variables
ENV FETCH_FREQUENCY=300
ENV COINGECKO_BASE_URL="https://api.coingecko.com/api/v3/simple"
ENV DATABASE_TABLE="msd-prices"
ENV REGION="eu-central-1"

# Add AWS credentials (this is needed just running the container outside AWS)
#RUN mkdir -p /home/root/.aws
#COPY aws/credentials /root/.aws/credentials

# Set up python requiments
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# Start Flask app
EXPOSE 5000
ENV FLASK_APP=application/bitcoin.py
CMD ["flask", "run", "--host", "0.0.0.0"]