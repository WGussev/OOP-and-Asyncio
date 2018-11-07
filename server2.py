import asyncio
from server import read_msg

def metric_to_str(key, mem_i):
    mem_sorted = sorted(mem_i, key=lambda x: float(x[1]))
    mem_strs = [' '.join([key, str(item[0]), str(int(item[1].split('.')[0]))]) for item in mem_sorted]
    return '\n'.join(mem_strs)


def read_msg(msg, mem):

    # format: "put server.metric metric_value timestamp\n"
    # format: "get key\n"

    prefix, metrics = msg.split(' ', 1)

    if prefix == 'put':
        name, metric, timestamp = metrics.strip('\n').split()
        if not (name in mem):
            mem[name] = []
        mem[name].append((metric, timestamp))
        response = 'ok\n\n'
    elif prefix == 'get':
        name = metrics.strip('\n')
        if name == '*':
            resp = []
            for name in mem.keys():
                resp.append(metric_to_str(name, mem[name]))
            resp = '\n'.join(resp)
        else:
            resp = metric_to_str(name, mem[name])
        response = 'ok\n'+resp+'\n'
    else:
        response = 'error\nwrong_command\n\n'

    return response

class MsgHandler:

    def __init__(self, mem):
        self.mem = mem

    async def handle(self, reader, writer):
        data = await reader.read(1024)
        response = read_msg(data.decode('utf-8'), self.mem)
        writer.write(response.encode('utf-8'))
        await writer.drain()
        writer.close()


def run_server(host, port):
    mem = {}
    msg_handler = MsgHandler(mem)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(msg_handler, host, port, loop=loop)

    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()