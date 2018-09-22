import asyncio
from typing import Dict

COUNTERS: Dict[str, 'Counter'] = {}


class Counter:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def inc(self):
        self.value += 1

    def drop(self):
        self.value = 0


async def handler(reader: asyncio.StreamReader,
                  _: asyncio.StreamWriter) -> None:

    async for packet in reader:
        counter = packet.rstrip()

        if counter not in COUNTERS:
            COUNTERS[counter] = Counter(counter)

        COUNTERS[counter].inc()


async def counter():
    while True:
        await asyncio.sleep(1)
        total = 0
        for n, i in COUNTERS.items():
            if i.value:
                total += i.value
                i.drop()
        print(f'Total:{total:>10}', end='\r')
