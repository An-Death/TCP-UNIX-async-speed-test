import asyncio
from multiprocessing import Process
from typing import Tuple

from server import counter, handler
from client import client

LIST_OF_FORKS = []


def is_port(port: str):
    return port.isdigit()


def start_server(port=None, path=None) -> asyncio.AbstractServer:
    if port:
        return asyncio.start_server(handler, port=port, host='localhost')

    else:
        return asyncio.start_unix_server(handler, path=path)


def _create_client_forks(forks: int, path=None, port=None):
    for i in range(forks):
        LIST_OF_FORKS.append(
            Process(name=i, target=client, args=(i,), kwargs={'path': path, 'port': port})
        )
    for i in LIST_OF_FORKS:
        i.start()


async def main(forks, port=None, path=None):
    asyncio.create_task(counter())

    await start_server(port=port, path=path)
    _create_client_forks(forks, path=path, port=port)

    while True:
        await asyncio.sleep(0)


def _get_port_path_from_input()-> Tuple[int, str]:
    port: int = None
    path: str = None

    port_or_path = input('Введите порт или путь:')
    port_or_path = port_or_path.strip()
    if is_port(port_or_path):
        port = int(port_or_path)
        return port, path
    else:
        path = str(port_or_path)
        return port, path


def _get_forks_from_input()-> int:
    forks = input('Введите кол-во клиентов:')
    assert forks.isdigit(), 'Кол-во клиентов должно быть числом'
    return int(forks)


if __name__ == '__main__':
    port, path = _get_port_path_from_input()
    forks = _get_forks_from_input()

    try:
        asyncio.run(main(forks, port=port, path=path))
    except KeyboardInterrupt:
        for f in LIST_OF_FORKS:
            f.kill()
