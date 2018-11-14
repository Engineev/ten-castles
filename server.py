from xmlrpc.server import SimpleXMLRPCServer
import argparse
from typing import *


class Server:
    _rpc_methods_ = ['add']

    def __init__(self, address):
        self._strategies = {}
        self._srv = SimpleXMLRPCServer(address,
                                       allow_none=True, logRequests=False)
        self._srv.register_function(self.add, 'add')

    def start(self):
        self._srv.serve_forever()

    def add(self, name: str, strategy: List[int]) -> int:
        print('add:', name, str(strategy))
        self._strategies[name] = list(strategy)
        return self._run(name)

    def _run(self, name: str) -> int:
        score = 0
        strategy = self._strategies[name]
        for k, v in self._strategies.items():
            if k == name:
                continue
            print(k, v)
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
