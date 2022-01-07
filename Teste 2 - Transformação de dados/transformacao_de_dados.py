from tabula import read_pdf
import os
options = ["-Dorg.slf4j.simpleLogger.defaultLogLevel=off", "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog"]
filename = 'padrao-tiss_componente-organizacional_202111.pdf' ## PDF file name

## Reading PDF
df = read_pdf(filename, pages=[114, 115, 116, 117, 118, 119, 120], encoding='utf-8', java_options=options)
##

## Extracting tables and creating CSVs
# First table
first_table_name = ''
final = ''
df[0].to_csv('30.csv', encoding='utf-8')
with open(f'30.csv', 'r', encoding='utf-8') as f:
    file = f.read().split('\n')
    first_table_name = file[0][1:]
    for i in file[1:-1]:
        content = i.split(',')[1]
        first_space = content.find(' ')
        first_entry = content[:first_space]
        second_entry = content[first_space + 1:]
        final += first_entry + ',' + second_entry + '\n'
os.remove('30.csv')
with open(first_table_name, 'w', encoding='utf-8') as f:
    f.write(final[:-1])
##