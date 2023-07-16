from pydantic import BaseModel


class RandomEvent(BaseModel):
    frequency: int


class Bid(BaseModel):
    name: str
    item: str
    amount: int
    address: dict[str, str]


names = ['Bailee', 'Rowan', 'Mick', 'Liliana', 'Darren', 'Karrie']
items = ['Apple', 'Banana', 'Cherry', 'Durian', 'Elderberry']
addresses = [
    {'province': 'Jawa Timur', 'city': 'Malang'},
    {'province': 'Jawa Tengah', 'city': 'Semarang'},
    {'province': 'Jawa Barat', 'city': 'Bandung'},
]
