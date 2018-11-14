from xmlrpc.server import SimpleXMLRPCServer
import argparse
import threading
from typing import *


class Server:
    _rpc_methods_ = ['add', 'delete', 'run', 'check']

    def __init__(self, address):
        self._strategies = {}
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
        return 'average: ' + str(score // (len(self._strategies) - 1)) + '\n' \
               + result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    srv = Server(('', args.port))
    srv.start()
