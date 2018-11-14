from xmlrpc.server import SimpleXMLRPCServer
import argparse
import threading
import shelve
from typing import *


class Server:
    _rpc_methods_ = ['add', 'delete', 'run', 'check', 'duels']

    def __init__(self, address):
        self._strategies = shelve.open('ten_castles')
        self._srv = SimpleXMLRPCServer(address,
                                       allow_none=True, logRequests=False)
        self._lock = threading.Lock()
        for name in self._rpc_methods_:
            self._srv.register_function(getattr(self, name))

    def start(self):
        self._srv.serve_forever()

    def add(self, name: str, strategy: List[int]):
        print('add:', name)
        with self._lock:
            self._strategies[name] = list(strategy)
            return self._run(name)

    def delete(self, name: str):
        print('delete:', name)
        with self._lock:
            if name not in self._strategies:
                return
            del self._strategies[name]

    def run(self, name: str):
        print('run:', name)
        with self._lock:
            return self._run(name)

    def check(self, name: str):
        with self._lock:
            if name not in self._strategies:
                return 'No such strategy'
            return name + ": " + str(self._strategies[name])

    def duels(self):
        if len(self._strategies) == 1:
            return "Only one strategy exists"
        with self._lock:
            result = ""
            for n1, s1 in self._strategies.items():
                score = 0
                for n2, s2 in self._strategies.items():
                    if n1 == n2:
                        continue
                    cur_score = 0
                    for i in range(0, 10):
                        if s1[i] > 2 * s2[i]:
                            cur_score += i + 1
                    score += cur_score
                score = score / (len(self._strategies) - 1)
                result += n1 + ': ' + str(score) + '\n'
            return result

    def _run(self, name: str):
        if name not in self._strategies:
            return 'Invalid strategy'

        result = ""

        score = 0
        strategy = self._strategies[name]
        for k, v in self._strategies.items():
            if k == name:
                continue
            cur_score = 0
            for i in range(0, 10):
                if strategy[i] > 2 * v[i]:
                    cur_score += i + 1
            result += "from " + k + ": " + str(cur_score) + '\n'
            score += cur_score
        if len(self._strategies) == 1:
            return 'No other strategies'
        return 'average: ' + str(score / (len(self._strategies) - 1)) + '\n' \
               + result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    srv = Server(('', args.port))
    srv.start()
