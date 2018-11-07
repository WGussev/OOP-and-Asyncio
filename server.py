import time


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

# from random import randint
#
# mem = {}
# for i in range(10):
#     t = time.time()
#     pref = randint(1,3)
#     print(read_msg(f'put name{str(pref)} {float(i)} {t}', mem))
#     time.sleep(0.01)
# print(mem)
#
# print(read_msg('get *\n', mem))