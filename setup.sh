#!/bin/sh

set -x

wget https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py -O "$HOME/sts"
sudo ln "$HOME/sts" /usr/bin/sts
