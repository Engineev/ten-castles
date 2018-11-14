from xmlrpc.server import SimpleXMLRPCServer
import argparse
from typing import *


class Server:
    _rpc_methods_ = ['add', 'delete', 'run']

    def __init__(self, address):
        self._strategies = {}
        self._srv = SimpleXMLRPCServer(address,
                                       allow_none=True, logRequests=False)
        for name in self._rpc_methods_:
            self._srv.register_function(getattr(self, name))

    def start(self):
        self._srv.serve_forever()

    def add(self, name: str, strategy: List[int]) -> int:
        print('add:', name)
        self._strategies[name] = list(strategy)
        return self._run(name)

    def delete(self, name: str):
        if name not in self._strategies:
            return
        print('delete:', name)
        del self._strategies[name]

    def run(self, name: str):
        print('run:', name)
        return self._run(name)

    def _run(self, name: str) -> int:
        if name not in self._strategies:
            return -1

        score = 0
        strategy = self._strategies[name]
        for k, v in self._strategies.items():
            if k == name:
                continue
            for i in range(0, 10):
                if strategy[i] > 2 * v[i]:
                    score += i + 1
        if len(self._strategies) == 1:
            return 0
        return score // (len(self._strategies) - 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    srv = Server(('', args.port))
    srv.start()
