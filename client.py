from xmlrpc.client import ServerProxy
import argparse
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Submit a strategy')
    parser.add_argument('-s', '--server',
                        help='server address. Format: ip:port')
    parser.add_argument('-id', '--identifier',
                        help='The identifier of this strategy')
    parser.add_argument('strategy', type=int, nargs='+',
                        help=
                        'Your strategy. 10 integers separated by whitespace')
    args = parser.parse_args()

    addr = 'http://' + args.server
    with ServerProxy(addr, allow_none=True) as proxy:
        strategy = list(args.strategy)

        if not valid_strategy(strategy):
            print("Invalid strategy")
            exit(-1)

        print('The score you got:', proxy.add(args.identifier, strategy))
