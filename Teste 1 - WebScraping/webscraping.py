from bs4 import BeautifulSoup
import urllib.request
import traceback
import sys

# Declaring function for managing connections and getting Soup instance
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
    return BeautifulSoup(content, 'html.parser')

# Declaring first page parser function
def get_second_page(first_page):
    soup = safe_connect(first_page)
    p_occurrences = soup.find_all("p", {"class": "callout"})
    a_block = [i.a for i in p_occurrences if "Clique aqui para acessar a versão" in i.a.string][0]
    next_page = a_block["href"]
    return next_page

# Declaring second page parser function
def get_download_link(second_page):
    soup = safe_connect(second_page)
    tr_occurrences = soup.find("table").find_all("tr")[1:]
    comp_org = [i for i in tr_occurrences if "Componente Organizacional" in i.td.string][0] # First td is title of file ("which file" indicator)
    return comp_org.a["href"]

# Declaring download and file creation function
def download_file(download_link):
    html = urllib.request.urlopen(download_link).read()
    file_name = download_link[download_link.rfind('/') + 1:]
    with open(file_name, 'wb') as f:
        f.write(html)

# Main
first_page = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"
second_page = get_second_page(first_page)
download_link = get_download_link(second_page)
download_file(download_link)