# Stregsystemet-CLI

This repository is the Stregsystemet CLI, to buy things in Stregsystemet, at AAU.
Use of this cli-tool is **at your own risk** and there will be no support guarranteed. Either try to resolve the issue yourself and submit a PR or write an issue.
 
## Requirements

The CLI is a python script that relies on no external dependendencies. The script is tested with python 3.9

## Installation

To install the script, simply cURL or wget it from GitHub

```bash
wget https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py -O sts
```

## Usage

```bash
$ sts -h
usage: sts [-h] [-u [USER]] [-i [ITEM]] [-c [COUNT]] [-b] [-l] [product]

positional arguments:
  product               Specifies the product to buy

optional arguments:
  -h, --help            show this help message and exit
  -u [USER], --user [USER]
                        Specifies your Stregsystem username
  -i [ITEM], --item [ITEM]
                        Specifies the item you wish to buy
  -c [COUNT], --count [COUNT]
                        Specifies the amount of items you wish to buy
  -b, --balance         Output only stregdollar balance

  -l, --history         Shows your recent purchases
  -a, --update          Update the script and then exists
```

If either the user or item arguments or no arguments at all are specified the CLI will enter interactive mode.

The script also keeps track of your balance and what items are available in Stregsystemet.

## Contributions

Contributions are welcome!

Feel free to fork the project and create a pull request. 
To get started with a development environment of Stregsystemet, go to the official [Stregsystemet repository](https://github.com/f-klubben/stregsystemet)
