import os

os.system('cp site/* ../thestuffidowithdata/static/covid/')

os.chdir('../thestuffidowithdata')

os.system('git pull; gatsby build; rsync -avh public/ gorgotron@tloureiro.com:~/thestuffidowithdata.com')