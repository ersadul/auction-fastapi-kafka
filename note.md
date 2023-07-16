## Create Stream in ksql
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

## Trasform stream schema
CREATE STREAM bids_formatted AS
select item,
       name,
       amount,
       address -> province, 
       address -> city,
       TIMESTAMPTOSTRING(ROWTIME, 'yyyy-MM-dd HH:mm:ss', 'GMT+7') AS timestamp 
from bids;