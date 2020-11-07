import os

os.system('cp site/* ../thestuffidowithdata/static/covid/')

os.chdir('../thestuffidowithdata')

os.system('gatsby build')

os.system('rsync -avh public/ gorgotron@tloureiro.com:~/thestuffidowithdata.com')