#!/usr/bin/env python

import requests
import re
import argparse
import sys
import urllib3

urllib3.disable_warnings()

url = 'https://stregsystem.fklub.dk'
room = '10'
exit_words = [':q','exit','quit']
referer_header={'Referer': url}
balance = ''


def is_int(value):
    try:
        int(value)
        return True
    except:
        return False


def get_wares():
    session = requests.Session()
    r = session.get(f"{url}/{room}/", verify=False)
    body = r.text
    item_id_list = re.findall(r'<td>(\d+)</td>', body)
    item_name_list = re.findall(r'<td>(.+?)</td>', body)
    item_price_list = re.findall(r'<td align="right">(\d+\.\d+ kr)</td>', body)
    
    # pprint(len(item_id_list))
    # pprint(len(item_name_list))
    item_name_list = [ x for x in item_name_list if not is_int(x) ]
    # pprint(item_name_list)
    # pprint(len(item_price_list))

    session.close()
    wares = []
    for i in range(len(item_id_list)):
        wares.append((item_id_list[i], item_name_list[i], item_price_list[i]))

    return wares


wares = get_wares()


def print_wares(wares):
    print('{:<8} {:<50} {:<10}'.format('Id','Item','Price'))
    print('-'*68)
    for ware in wares:
        print('{:<8} {:<50} {:<10}'.format(ware[0],ware[1],ware[2]))


def test_user(user):
    session = requests.Session()
    r = session.get(f"{url}/{room}/", verify=False)
    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"',r.text)
    json = {
        'quickbuy': f"{user}",
        'csrfmiddlewaretoken': token.group(1)
    }
    # pprint(json)
    cookies = {'csrftoken': session.cookies.get_dict()['csrftoken'], 'djdt': 'show'}
    # pprint(cookies)
    sale = session.post(f"{url}/{room}/sale/",
            verify=False,
            data=json,
            cookies=cookies,
            headers=referer_header)
    session.close()
    if sale.status_code != 200:
        print('Noget gik galt.', sale.status_code, sale.content)
        raise SystemExit
    if 'Det lader ikke til, at du er registreret som aktivt medlem af F-klubben' in sale.text:
        return False

    global balance
    balance = re.search(r'(\d+.\d+) kroner til gode!', sale.text).group(1)
    return True


def sale(user, itm, count=1):
    session = requests.Session()
    r = session.get(f"{url}/{room}/", verify=False)
    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', r.text)
    json = {
        'quickbuy': f"{user} {itm}:{count}",
        'csrfmiddlewaretoken': token.group(1)
    }
    sale = session.post(f"{url}/{room}/sale/",
            data=json,
            cookies={'csrftoken': session.cookies.get_dict()['csrftoken'],
                     'djdt': 'show'},
            headers=referer_header,)
    session.close()
    if sale.status_code != 200:
        print("Du har ikke købt din vare. Prøv igen", sale.status_code)
        raise SystemExit
    elif 'STREGFORBUD!' not in sale.text:
        ware = [x for x in wares if x[0] == itm]
        print('Du har købt', count, ware[0][1], 'til', ware[0][2], 'stykket')

        global balance
        balance = re.search(r'(\d+.\d+) kroner til gode!', sale.text).group(1)
        print('Du har nu', balance, 'stregdollars')
    else:
        print('''STREGFORBUD!
Du kan ikke foretage køb, før du har foretaget en indbetaling!
Du kan foretage indbetaling via MobilePay''')
        raise SystemExit


def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', default=None, nargs='?', dest='user', help='Specifies your Stregsystem username')
    parser.add_argument('-i', '--item', default=None, nargs='?', dest='item', help='Specifies the item you wish to buy')
    parser.add_argument('-c', '--count', default=1, nargs='?', dest='count', help='Specifies the amount of items you wish to buy')

    return parser.parse_args(args)

def get_item(ware_ids):
    item_id = input('Id> ')
    while not is_int(item_id) or item_id not in ware_ids:
        if item_id.lower() in exit_words:
            return 'exit'
        print(f"'{item_id}' is not a valid item")
        item_id = input('Id> ')
    return item_id


def user_buy(user):
    if test_user(user):
#        os.system('cls||clear')
        print('Hej,', user)
        print('Du har', balance, 'stregdollars')
        print('')
        print("Hvad ønsker at købe i Stregsystemet? (Skriv 'exit' for at komme ud af interfacet)")
        print_wares(wares)
        print('')
        while True:
            item = get_item([x[0] for x in wares])
            if item in exit_words:
                raise SystemExit
            sale(user, item)
    else:
        print('''Det var sært, %user%.
Det lader ikke til, at du er registreret som aktivt medlem af F-klubben i TREOENs database.
Måske tastede du forkert?
Hvis du ikke er medlem, kan du blive det ved at følge guiden på fklub.dk.'''.replace('%user%', user))

def userless_buy(item, count):
    ware = [ x for x in wares if x[0] == item ]
    print('Du er ved at købe', count, ware[0][1], 'til', ware[0][2], 'stykket')
    print("Du kan skrive 'exit' for at annullere.")
    user = input('Hvad er dit brugernavn? ')
    
    while not test_user(user):
        if user.lower() in exit_words:
            raise SystemExit
        print(f"'{user}' is not a valid user")
        user = input('Hvad er dit brugernavn? ')
    
    sale(user, item, count)

def no_info_buy():
    print("Du kan skrive 'exit' for at annullere.")
    user = input('Hvad er dit brugernavn? ')
    
    while not test_user(user):
        if user.lower() in exit_words:
            raise SystemExit
        print(f"'{user}' is not a valid user")
        user = input('Hvad er dit brugernavn? ')
    
    user_buy(user)


def main():
    args=parse(sys.argv[1::])
    if args.user == None or args.item == None:
        if args.user != None:
            user_buy(args.user)
        elif args.item != None:
            userless_buy(args.item, args.count)
        else:
            no_info_buy()

    else:
        sale(args.user,args.item,args.count)

if __name__ == '__main__':
    main()
