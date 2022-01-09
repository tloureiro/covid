#!/usr/bin/python3

import os

os.chdir('..')

os.system('rsync -avh --max-size=50m covid/ ubuntu@pi4:~/projects/covid')

