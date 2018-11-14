from xmlrpc.client import ServerProxy
import argparse
import sys
from typing import *


def valid_strategy(strategy_: List[int]) -> bool:
    strategy = list(strategy_)
    total = sum(strategy)
    if total > 100:
        return False
    for item in strategy:
        if item < 0:
            return False
    return True


def run(address):
    with ServerProxy(address, allow_none=True) as proxy:
        while True:
            cmd = [x.strip() for x in sys.stdin.readline().split()]
            if not cmd:
                continue
            if cmd[0] == 'add':
                name = cmd[1]
                strategy = [int(x) for x in cmd[2:]]
                if not valid_strategy(strategy):
                    print("Invalid strategy")
                    continue
                score = proxy.add(name, strategy)
                print('The score you got:', score)
            elif cmd[0] == 'delete':
                name = cmd[1]
                proxy.delete(name)
            elif cmd[0] == 'run':
                name = cmd[1]
                score = proxy.run(name)
                print('The score you got:', score)
            elif cmd[0] == 'exit':
                return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the client')
    parser.add_argument('address', help='server address. Format: ip:port')
    args = parser.parse_args()

    addr = 'http://' + args.address
    run(addr)
    # with ServerProxy(addr, allow_none=True) as proxy:
    #     strategy = list(args.strategy)
    #
    #     if not valid_strategy(strategy):
    #         print("Invalid strategy")
    #         exit(-1)
    #
    #     print('The score you got:', proxy.add(args.identifier, strategy))
