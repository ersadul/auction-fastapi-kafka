import logging
from .model import Bid
from config import config, config_sr
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

logging.basicConfig(level=logging.INFO)


def bid_to_dict(bid: Bid, ctx: SerializationContext):
    return {
        "name": bid.name,
        "item": bid.item,
        "amount": bid.amount,
        "address": bid.address,
    }


def delivery_report(err, event):
    if err is not None:
        logging.info(
            f'Delivery failed on reading for {event.key().decode("utf8")}: {err}')
    else:
        logging.info(
            f'Event reading for {event.key().decode("utf8")} produced to {event.topic()}')


def produce_event(topic: str = 'bids', bid: Bid = None):
    schema_registry_client = SchemaRegistryClient(config_sr)

    bids_value_schema = schema_registry_client.get_latest_version('bids-value')

    avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                     schema_str=bids_value_schema.schema.schema_str,
                                     to_dict=bid_to_dict)

    string_serializer = StringSerializer('utf_8')

    producer = Producer(config)

    try:
        producer.produce(topic=topic,
                         key=string_serializer(str(bid.item)),
                         value=avro_serializer(bid,
                                               SerializationContext(topic, MessageField.VALUE)),
                         on_delivery=delivery_report)
    except Exception as e:
        logging.warning(f'Error: {e}')
    finally:
        producer.flush()
