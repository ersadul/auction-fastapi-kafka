import logging
from time import sleep
from fastapi import FastAPI
from random import choices, randint
from .model import *
from .avro_producer import produce_event


logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/autobid")
async def generate(random_event: RandomEvent):
    for _ in range(random_event.frequency):
        event = Bid(name=choices(names)[0], item=choices(items)[
                    0], amount=randint(1, 1000), address=choices(addresses)[0])
        produce_event(bid=event)
        logging.info(f"data: {dict(event)}")
        sleep(1)

    return {'message': 'Events Created!'}


@app.post("/bid")
async def bid(bid: Bid):
    event = Bid(name=bid.name,
                item=bid.item,
                amount=bid.amount,
                address=bid.address)
    produce_event(bid=event)
    logging.info(f"data: {dict(event)}")
    
    return {
        'message': 'Event Created!',
        'data': event
    }