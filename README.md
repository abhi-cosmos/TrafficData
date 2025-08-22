TO Run the pipeline, run:

docker-compose build
docker-compose up

Once service is running:
Send a request from Postman to: http://0.0.0.0:8000/simulate-traffic?speed_factor=60

The value 60 can be changed. 

Now, we should be able to see data landing in BigQuery table. The message is pushed to pub/sub topic which has a subscription which will write data to BigQuery. For this to work the schema sent by the function must match the schema of the table. Any errors will be logged in the logging table through dead lettering feature in GCP Pub/Sub Topic. 