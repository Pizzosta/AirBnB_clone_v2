#!/usr/bin/python3
# usage = fab -f 100-clean_web_static.py do_clean:number={}
# -i my_ssh_private_key  > /dev/null 2>&1
""" Function that deploys """
import os
from fabric.api import *


env.hosts = ['52.86.198.91', '52.207.52.133']
env.user = 'ubuntu'


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))

    print("Old versions cleaned!")
