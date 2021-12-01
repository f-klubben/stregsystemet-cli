#!/usr/bin/env python3
# START_STS
from __future__ import print_function

from random import random
import requests
import re
import argparse
import sys
import os
import urllib3
import configparser
import sys
import builtins as __builtin__

from datetime import date
from pprint import pprint

urllib3.disable_warnings()

if sys.argv[0] == './main.py':
    url = 'http://localhost:8000'
    room = '1'
else:
    url = 'https://stregsystem.fklub.dk'
    room = '10'

is_windows = sys.platform == "win32"
exit_words = [':q', 'exit', 'quit', 'q']
referer_header = {'Referer': url}
balance = float()
config = configparser.ConfigParser()

user_id = ''

if is_windows:
    os.system('color')

SHORTHANDS = {
    'porter': 42,
    'øl': 14,
    'classic': 14,
    'grøn': 14,
    'monster': 1837,
    'ale16': 54,
    'cocio': 16,
    'soda': 11,
    'specialøl': 1848,
    'kaffe': 32,
    'sportscola': 1891,
    'abrikos': 1899,
    'fuzetea': 1879,
    'kakao': 1882,
    'cacao': 1882,
    'kinley': 1893,
    'monsterkaffe': 1900,
    'kildevand': 1839,
    'cider': 1831,
    'sommersby': 1831,
    'redbull': 1895,
    'panta': 1848,
    'glaspant': 1848,
    'pantb': 31,
    'sodapant': 31,
    'pantc': 1849,
    'storpant': 1849,
    'nordic': 1901,
    'fritfit': 1902,
    'månedens': 1903,
}


def is_int(value):
    if not value:
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False


_date = date.today()
month = _date.month
bat_amount = _date.day
lines_counted = 0


def print(*args, **kwargs):
    global bat_amount, lines_counted
    msg = ' '.join(map(str, args))
    if _date.month == 10 and bat_amount > 0:
        # CPU Heater. Doesn't matter. Still faster than the actual stregsystem
        print_prob = (
            ((random() * 10) / (len(' '.join(map(str, args))) * random() + 0.1) * random())
            * ((_date.day / 100) + 1)
            * 0.7
            * (lines_counted * 0.15)
        )
        print_prob = print_prob / int(print_prob) if int(print_prob) >= 1 else print_prob

        batted = False
        for i in range(len(msg)):
            if print_prob > random() and random() > random() and bat_amount > 0 and not batted:
                if msg[i] == '-' or is_int(msg[i]):
                    if random() > 0.04:
                        print_prob += random()
                    continue
                msg = msg[:i] + '\U0001F987' + msg[i + 1 :]
                bat_amount -= 1
                batted = True
                print_prob = print_prob - random()
                if print_prob <= 0 or bat_amount == 0:
                    break
            else:
                batted = False
        __builtins__.print(msg)
    else:
        __builtins__.print(msg)
    lines_counted += 1


def get_wares():
    try:
        session = requests.Session()
        r = session.get(f"{url}/{room}/", verify=False)
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


wares = get_wares()


def print_wares(wares):
    print('{:<8} {:<50} {:<10}'.format('Id', 'Item', 'Price'))
    print('-' * 68)
    for ware in wares:
        if re.match("<\w\d>", ware[1]):
            r = re.sub("<br>", ' - ', ware[1])
            r = re.sub("<\w\d> | </\w\d>|<\w\w>|</\w\d>", '', r)
            print('\u001B[31m{:<8} {:<50} {:<10}\u001B[0m'.format(ware[0], r, ware[2]))
        else:
            print('{:<8} {:<50} {:<10}'.format(ware[0], (ware[1]), ware[2]))


def print_no_user_help(user):
    print(
        f'Det var sært, {user}. \nDet lader ikke til, at du er registreret som aktivt medlem af F-klubben i TREOENs dat'
        f'abase. \nMåske tastede du forkert? \nHvis du ikke er medlem, kan du blive det ved at følge guiden på fklub.dk'
    )


def test_user(user):
    session = requests.Session()
    r = session.get(f"{url}/{room}/", verify=False)
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        raise SystemExit

    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', r.text)
    json = {'quickbuy': f"{user}", 'csrfmiddlewaretoken': token.group(1)}
    # pprint(json)
    cookies = {'csrftoken': session.cookies.get_dict()['csrftoken'], 'djdt': 'show'}
    # pprint(cookies)
    sale = session.post(f"{url}/{room}/sale/", verify=False, data=json, cookies=cookies, headers=referer_header)
    session.close()
    if sale.status_code != 200:
        print('Noget gik galt.', sale.status_code, sale.content)
        raise SystemExit
    if 'Det lader ikke til, at du er registreret som aktivt medlem af F-klubben' in sale.text:
        return False

    global balance
    balance = float(re.search(r'(\d+.\d+) kroner til gode!', sale.text).group(1))
    global user_id
    user_id = re.search(r'\<a href="/' + room + '/user/(\d+)"', sale.text).group(1)
    return True


def get_user_validated():
    user = input('Hvad er dit brugernavn? ')

    while not user or not test_user(user):
        if user.lower() in exit_words:
            raise SystemExit
        print(f"'{user}' is not a valid user")
        user = input('Hvad er dit brugernavn? ')

    return user


def print_history(wares):
    print('{:<29} {:<40}  {:<10}'.format('Date', 'Item', 'Price'))
    print('-' * 80)
    for ware in wares:
        print('{:<29} {:<40}  {:<10}'.format(ware[0], ware[1], ware[2]))

    print('')
    print('')


def get_history(user_id):
    if not user_id:
        print('Den angivne bruger har ikke noget ID. Afslutter')
        raise SystemExit(1)

    try:
        session = requests.Session()
        r = session.get(f"{url}/{room}/user/{user_id}", verify=False)
    except Exception:
        print('Kunne ikke oprette forbindelse til Stregsystenet')
        raise SystemExit(1)

    body = r.text
    item_date_list = re.findall(r'<td>(\d+\.\s\w+\s\d+\s\d+:\d+)</td>', body)
    item_name_list = [x for x in re.findall(r'<td>(.+?)</td>', body) if x not in item_date_list][
        0 : len(item_date_list)
    ]
    item_price_list = re.findall(r'<td align="right">(\d+\.\d+)</td>', body)
    history = []
    for x in range(len(item_date_list)):
        history.append((item_date_list[x], item_name_list[x], f"{item_price_list[x]} kr."))

    print_history(history)


def sale(user, itm, count=1):
    if int(count) <= 0:
        print('Du kan ikke købe negative mængder af varer.')
        return

    # check for shorthand and replace
    if itm in SHORTHANDS:
        itm = str(SHORTHANDS[itm])

    session = requests.Session()
    r = session.get(f"{url}/{room}/", verify=False)
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        raise SystemExit

    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', r.text)
    json = {'quickbuy': f"{user} {itm}:{count}", 'csrfmiddlewaretoken': token.group(1)}
    sale = session.post(
        f"{url}/{room}/sale/",
        data=json,
        cookies={'csrftoken': session.cookies.get_dict()['csrftoken'], 'djdt': 'show'},
        headers=referer_header,
    )
    session.close()
    if sale.status_code != 200:
        print("Du har ikke købt din vare. Prøv igen", sale.status_code)
        raise SystemExit
    elif 'STREGFORBUD!' not in sale.text:
        if ':' in itm:
            if is_int(itm.split(':')[1]):
                count = itm.split(':')[1]
                if int(count) <= 0:
                    print('Du kan ikke købe negative mængder af varer.')
                    return
                itm = itm.split(':')[0]
            else:
                print('Du har angivet tekst hvor du skal angive en mængde')
                return

        ware = [x for x in wares if x[0] == itm]
        if not len(ware):
            print(f"Der findes ikke nogen varer med id {itm}.")
            return

        print(f'{user} har købt', count, ware[0][1], 'til', ware[0][2], 'stykket')

        global balance
        balance -= float(ware[0][2].replace('kr', '').strip()) * float(count)
        itm_unit_price = float(ware[0][2].replace("kr", "").strip())
        itm_units_left = f"{(balance / itm_unit_price):.2f}" if itm_unit_price > 0 else "∞"
        print(f'Der er {balance:.2f} stregdollars - eller {itm_units_left} ' f'x {ware[0][1]} - tilbage')

    else:
        print(
            '''STREGFORBUD!
Du kan ikke foretage køb, før du har foretaget en indbetaling!
Du kan foretage indbetaling via MobilePay'''
        )
        raise SystemExit


def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--user', default=None, nargs='?', dest='user', help='Specifies your Stregsystem username'
    )
    parser.add_argument('-i', '--item', default=None, nargs='?', dest='item', help='Specifies the item you wish to buy')
    parser.add_argument(
        '-c',
        '--count',
        default=1,
        nargs='?',
        dest='count',
        type=int,
        help='Specifies the amount of items you wish to buy',
    )
    parser.add_argument('-b', '--balance', action='store_true', help='Output only stregdollar balance')
    parser.add_argument('-l', '--history', action='store_true', help='Shows your recent purchases')
    parser.add_argument('-p', '--mobilepay', dest='money', help='Provides a QR code to insert money into your account')
    parser.add_argument('-a', '--update', action='store_true', help='Update the script and then exists')
    parser.add_argument('-o', '--shorthands', action='store_true', help='Shows shorthands')
    parser.add_argument(
        '-s', '--setup', action='store_true', help='Creates a .sts at /home/<user> storing your account username'
    )
    parser.add_argument('product', type=str, nargs='?', help="Specifies the product to buy")

    return parser.parse_args(args)


def get_item(ware_ids):
    count = 1
    item_id = input('Id> ')
    if item_id.lower() in exit_words:
        return 'exit', 0

    if ':' in item_id:
        if is_int(item_id.split(':')[1]):
            count = item_id.split(':')[1]
            if int(count) <= 0:
                print('Du kan ikke købe negative mængder af varer.')
                return
            item_id = item_id.split(':')[0]
        else:
            print('Du har angivet tekst hvor du skal angive en mængde')
            return

    while not (item_id in SHORTHANDS) and (not is_int(item_id) or item_id not in ware_ids):
        if item_id.lower() in exit_words:
            return 'exit', 0

        print(f"'{item_id}' is not a valid item")
        item_id = input('Id> ')
    return item_id, count


def user_buy(user):
    if test_user(user):
        #        os.system('cls||clear')
        print('Hej,', user)
        print(f'Du har {balance:.2f} stregdollars')
        print('')
        print("Hvad ønsker at købe i Stregsystemet? (Skriv en af", str(exit_words), "for at komme ud af interfacet)")
        print_wares(wares)
        print('')
        while True:
            item, count = get_item([x[0] for x in wares])
            if item in exit_words:
                raise SystemExit
            elif item is None:
                continue
            sale(user, item, count)
    else:
        print_no_user_help(user)


def no_info_buy():
    print("Du kan skrive 'exit' for at annullere.")
    user = get_user_validated()
    user_buy(user)


def get_qr(user, amount):
    if is_int(amount) and int(amount) < 50:
        print('Mindste indsætningsbeløb er 50. Alt under, håndteres ikke.')
        return

    print("Skan QR koden nedenfor, for at indsætte penge på din stregkonto")
    session = requests.Session()
    r = session.get(f"https://qrcode.show/mobilepay://send?phone=90601&comment={user}&amount={int(amount)}")
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        raise SystemExit

    print(r.content.decode('UTF-8'))


def update_config_file(dirs):
    # This function iterates all config files and prepends "[sts]\n" to them.
    for path in dirs:
        if not os.path.exists(path):
            continue
        with open(path, 'r') as original:
            data = original.read()
        with open(path, 'w') as modified:
            modified.write('[sts]\n' + data)


def read_config():
    dirs = [os.path.expanduser('~/.config/sts/.sts'), os.path.expanduser('~/.sts'), '.sts']
    try:
        config.read(dirs)
    except configparser.MissingSectionHeaderError:
        # update the config to new format
        update_config_file(dirs)
        config.read(dirs)


def get_saved_user() -> str:
    return config.get('sts', 'user', fallback=None)


def calculate_sha256_binary(binary) -> str:
    import hashlib

    return hashlib.sha256(binary).hexdigest()


def has_version_difference():
    r = requests.get('https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py')
    newest_file_hash = calculate_sha256_binary(r.content)
    with open(__file__, 'rb') as f:
        data = f.read()
    current_file_hash = calculate_sha256_binary(data)

    return newest_file_hash != current_file_hash


def update_script():
    if not os.access(__file__, os.W_OK):
        print('Stregsystemet-CLI er i læs-kun modus og kan derfor ikke opdateres. Er du på NIX operativsystem?')
        return

    if not has_version_difference():
        return

    # I perform open heart surgery on myself :)
    with open(__file__, 'w', encoding="utf-8") as f:
        r = requests.get('https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py')
        if 'START_STS' in r.text and 'END_STS' in r.text:
            f.write(r.text)


def main():
    if has_version_difference():
        print("Der er en opdatering til STS. Hent den fra GitHub eller kør sts med --update.")

    args = parse(sys.argv[1::])

    if args.update is True:
        update_script()
        return

    if args.shorthands:
        print("You can use the following shorthand for purchasing")
        pprint(SHORTHANDS)
        return

    read_config()

    if args.user is None:
        args.user = get_saved_user()

    if args.setup:
        if args.user is None:
            args.user = get_user_validated()

        if test_user(args.user):
            home = os.path.expanduser('~')
            if not os.path.isfile(f"{home}/.sts"):
                with open(f"{home}/.sts", "w") as f:
                    print(f"Your .sts file has been created at location {home}/.sts")
                    f.write(f"user={args.user}")

    if args.user and args.product:
        if test_user(args.user):
            sale(args.user, args.item if args.item else str(args.product), args.count)
        else:
            print_no_user_help(args.user)

        return

    if args.balance and args.user:
        test_user(args.user)
        print(f'{balance:.2f}')
        return

    if args.history and args.user:
        global user_id
        test_user(args.user)
        get_history(user_id)

    if args.user is None or args.item is None:
        if args.user is None:
            args.user = get_user_validated()

        if args.user is not None:
            if args.money:
                get_qr(args.user, args.money)
            else:
                user_buy(args.user)
        else:
            no_info_buy()

    else:
        if test_user(args.user):
            if args.money:
                get_qr(args.user, args.money)
            else:
                sale(args.user, args.item, args.count)
        else:
            print_no_user_help(args.user)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)

# END_STS
