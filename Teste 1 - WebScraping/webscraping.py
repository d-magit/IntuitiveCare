from bs4 import BeautifulSoup
import urllib.request
import traceback
import sys

# Declaring function for managing connections
def safe_connect(link):
    content = ''
    last = True
    temp = 0
    while last:
        try:
            fp = urllib.request.urlopen(link)
            content = fp.read().decode("utf8")
            fp.close()
            last = False
        except:
            if temp != 10:
                temp += 1
                print(f"Algo de errado ocorreu ao tentar estabelecer uma conexão, tentando novamente...")
            else:
                print("Todas as 10 tentativas falharam. Parando programa... Último erro:")
                print(''.join(traceback.format_exception(*sys.exc_info())))
                exit()
    return content

# Site: https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss