# Auction Data Streaming
This is a project that trying to build streaming data service. Using FastAPI to generate event everytime users send request into some endpoints. For streaming data platform, this project used [Confluent Kafka](https://www.confluent.io/home/) and utilize its service like Schema Registry, ksqlDB and Kafka Connect. Then, for storing and analyze the created events, I integrate specific kafka topic into BigQuery.

note for me for further reference:
- specify the topic key if you have concern with events ordering (storing in same partition) and create most suitable key because when I sink into the topic into BigQuery the key not included as message.
- Dont overuse ksql to create analytical queries (cmiiw, i just heard it from the expert but it make sense)

## Prerequisites and requirements
to install all the dependencies:
`pip install -r requirements.txt`

### Modifying config .py
First copy the [config.py.example](./config.py.example) into config.py and fill all the required API key from [confluent console](https://confluent.cloud/)

### ksqlDB 
create ksqlDB stream as consumer to the topic we produced in endpoints for further data processing.
**Create stream in ksql**
```sql
CREATE STREAM bids (
  name VARCHAR,
  item VARCHAR KEY,
  amount INT, 
  address STRUCT <
    province VARCHAR, 
    city VARCHAR >
) WITH (
  KAFKA_TOPIC = 'bids',
  PARTITIONS = 1,
  VALUE_FORMAT = 'avro'
);
```
**Trasform stream schema**
```sql
CREATE STREAM bids_formatted AS
select item,
       name,
       amount,
       address -> province, 
       address -> city,
       TIMESTAMPTOSTRING(ROWTIME, 'yyyy-MM-dd HH:mm:ss', 'GMT+7') AS timestamp 
from bids;
```
### How To Run
because FastAPI using uvicorn as webserver, you can run by 
```
uvicorn app.main:app
or
uvicorn app.main:app --reload
```

### Endpoint
`/autobid`: auto generating events 
POST request example:
```json
{
    "frequency": 10
}
```

`/bid`: make an event
POST request example:
```json
{
    "name": "ersa",
    "item": "Apple",
    "amount": 99,
    "address": {
        "province": "Jawa Timur",
        "city": "Malang"
    }
}
```
