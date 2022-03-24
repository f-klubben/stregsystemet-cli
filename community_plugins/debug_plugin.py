import argparse
import requests
import re


# This block runs before the argument parser is created.
# It allows the user to create additional arguments.
def pre_argparse(parser: argparse.ArgumentParser, constants: dict) -> None:
    parser.add_argument(
        '-D',
        '--DEBUG',
        default=None,
        const='test',
        nargs='?',
        help='Sets the debug flag for STS',
        choices=['prod', 'test'],
    )
    pass


def get_wares(CONSTANTS):
    def is_int(value):
        if not value:
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False

    try:
        session = requests.Session()
        r = session.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/", verify=False)
    except Exception:
        print('Could not fetch wares from Stregsystement...')
        raise SystemExit(1)
    body = r.text
    item_id_list = re.findall(r'<td>(\d+)</td>', body)
    item_name_list = re.findall(r'<td>(.+?)</td>', body)
    item_price_list = re.findall(r'<td align="right">(\d+\.\d+ kr)</td>', body)
    item_name_list = [x for x in item_name_list if not is_int(x)]
    session.close()
    wares = []
    for i in range(len(item_id_list)):
        wares.append((item_id_list[i], item_name_list[i], item_price_list[i]))
    return wares


# This block will run inside the code. This is where
# the user places their custom logic
def run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    if args.DEBUG:
        print(f'{args.DEBUG=}')
        constants['debug'] = True
    if args.DEBUG == 'test':
        constants['url'] = 'http://localhost:8000'
        constants['room'] = '1'
        wares.clear()
        [wares.append(ware) for ware in get_wares(constants)]
    pass


# This block runs at the very end of main and may not
# be reached, due to some 'raise systemExit'
def post_run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    pass
