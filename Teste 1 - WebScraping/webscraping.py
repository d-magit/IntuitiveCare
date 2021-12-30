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

# Declaring first page parser function
def get_second_page(first_page):
    html = safe_connect(first_page)
    soup = BeautifulSoup(html, 'html.parser')
    p_occurrences = soup.find_all("p", {"class": "callout"})
    a_block = [i.a for i in p_occurrences if "Clique aqui para acessar a versão" in i.a.string][0]
    next_page = a_block["href"]
    return next_page

# Main
first_page = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"
second_page = get_second_page(first_page)