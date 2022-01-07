from tabula import read_pdf
import os
import re
options = ["-Dorg.slf4j.simpleLogger.defaultLogLevel=off", "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog"]
filename = 'padrao-tiss_componente-organizacional_202111.pdf' ## PDF file name



## Simple function for processing and then removing accents from string (to use as filename)
def process_file_name(name):
    name = "_".join(name.lower().split())
    return re.sub(r'([çã])', lambda x: {'ç':'c', 'ã':'a'}[x.group(1)], name) + ".csv"
##



## Reading PDF
df = read_pdf(filename, pages=[114, 115, 116, 117, 118, 119, 120], encoding='utf-8', java_options=options)
##



## Extracting tables and creating CSVs
########### First table
name = ''
final = ''
df[0].to_csv('30.csv', encoding='utf-8')
with open(f'30.csv', 'r', encoding='utf-8') as f:
    file = f.read().split('\n')
    name = file[0][1:]
    for i in file[1:-1]:
        content = i.split(',')[1]
        first_space = content.find(' ')
        first_entry = content[:first_space]
        second_entry = content[first_space + 1:]
        final += first_entry + ',' + second_entry + '\n'
os.remove('30.csv')
first_table_name = process_file_name(name)
with open(first_table_name, 'w', encoding='utf-8') as f:
    f.write(final[:-1])
###########
########### Second table
name = ''
final = ''
for i in range(1, 7):
    name = f'31_{i}.csv'
    df[i].to_csv(name, encoding='utf-8')
    with open(name, 'r', encoding='utf-8') as f:
        final += f.read()
    os.remove(name)
full_content = final.split('\n')
name = full_content[0].split(',')[-1]
final = ''
for i in full_content[1:-1]:
    first_comma = i.find(',')
    content = i[first_comma + 1:]
    content = (" " if ',' not in content else "\n") + content
    final += content.replace('\"', '')
second_table_name = process_file_name(name)
with open(second_table_name, 'w', encoding='utf-8') as f:
    f.write(final[1:])
###########
##