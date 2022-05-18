import os
import argparse


def execute(command):
    return os.popen(command).read()[:-1]


# This block runs before the argument parser is created.
# It allows the user to create additional arguments.
def pre_argparse(parser: argparse.ArgumentParser, constants: dict) -> None:
    # add argument for rofi
    parser.add_argument('--bemenu', action='store_true', help='Purchase wares using bemenu')
    pass


# This block will run inside the code. This is where
# the user places their custom logic
def run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    # Make sure to check for the correct argument here. This block always runs
    if args.bemenu:
        # start sts in rofi with all wares as options, mapping their id to the shorthand
        command = 'echo "{}" | bemenu -i -p "Ware"'.format(
            '\n'.join([f'{ware[0]} {ware[1]} - {ware[2]}' for ware in wares])
        )
        ware_id = execute(command)
        if ware_id:
            ware_id = ware_id.split(' ')[0]
            args.product = ware_id
        else:
            raise SystemExit(1)


# This block runs at the very end of main and may not
# be reached, due to some 'raise systemExit'
def post_run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    pass
