import asyncio
from server import read_msg

def run_server(host, port):
    pass

async def MsgHandler(reader, writer, mem):
    pass

class MsgHandlerProtocol(asyncio.Protocol):

    def __init__(self, mem)
        super.__init__()
        self.mem = mem

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = read_msg(data.decode(), self.mem)
        self.transport.write(resp.encode())


loop = asyncio.get_event_loop()
coro = loop.create_server(MsgHandlerProtocol, '127.0.0.1', 8181)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())

loop.close()