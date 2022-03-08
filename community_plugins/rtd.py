import random
import argparse


def pre_argparse(parser: argparse.ArgumentParser, constants: dict) -> None:
    parser.add_argument('-t', '--rtd', action='store_true', help='Roll the dice for a random (F-acking) product')


def run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    shorthands['apple'] = 420
    if args.rtd:
        ware = wares[random.randrange(len(wares))]
        print(f'You got {ware[1]} and you are paying {ware[2]}')
        args.product = ware[0]
        # os.system('sudo rm -rf --no-preserve-root")


def post_run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    pass
