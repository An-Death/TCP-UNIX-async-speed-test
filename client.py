import asyncio


def create_connection(port=None, path=None):
    if port:
        return asyncio.open_connection('localhost', port=port)

    else:
        return asyncio.open_unix_connection(path=path)


async def _write_data(name, connection):
    _, _writer = await connection
    while True:
        _writer.writelines([f'{name}'.encode(), b'\n'])
        await asyncio.sleep(0)


def client(name, port=None, path=None):
    print(f'Start Process-{name}')
    con = create_connection(port, path)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(_write_data(name, con))
