import mysql.connector
from mysql.connector import Error
import csv
root_pass = "5aDFCEk5!JJ^#Y" ## Password for MySQL Root
main_db_name = "IntuitiveCare" ## DB name

## Function to connect to MySQL
def create_server_connection(host, user, passwd, database = None):
    # Initialize variables
    args = {'host': host, 'user': user, 'passwd': passwd}
    if database != None:
        args['database'] = database
    connection = None
    # Attempt to connect and return connection, or raise exception if the attempt fails.
    try:
        connection = mysql.connector.connect(**args)
    except Error as err:
        print(f"MySQL: Connection failed! Error: '{err}'")
    return connection
##

## Function to create a database
def create_database(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE " + name)
    except Error as err:
        print(f"MySQL: Creating database failed! Error: '{err}'")
##

## Function to execute a single query
def execute_query(connection, query, isbuffered = False):
    cursor = connection.cursor(buffered = isbuffered)
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f"MySQL: Executing query '{query}' failed! Error: '{err}'")
    return cursor.fetchall()
##

## Function to insert CSV content in first table
def insert_csv_t1(connection, table, file_path):
    with open (file_path, 'r') as f:
        cursor = connection.cursor()
        reader = csv.reader(f, delimiter=';', quotechar='"')
        columns = None
        for i in range(3): # Line 3 is where file actually starts
            columns = next(reader) 
        # Structuring query
        query = f"""INSERT INTO {table}({','.join([i.replace(' ', '_') for i in columns])})
                    VALUES ({','.join([r"%s"] * len(columns))})"""
        try:
            for entry in reader:
                # Converting values and executing query
                cursor.execute(query,  [int(entry[0]), entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], 
                                        entry[7], entry[8], entry[9], entry[10], entry[11], entry[12], 
                                        entry[13], entry[14], entry[15], entry[16], entry[17], entry[18]])
            connection.commit() # Committing
        except Error as err:
            print(f"MySQL: Insertion query for first table failed on entry {entry}! Error: '{err}'")
##

## Function to insert CSV content in table
def insert_csv_t2(connection, table, file_path):
    with open (file_path, 'r') as f:
        cursor = connection.cursor()
        reader = csv.reader(f, delimiter=';', quotechar='"')
        columns = next(reader) # Line 1 is where file actually starts
        # Structuring query
        query = f"""INSERT INTO {table}({','.join(columns)}) VALUES ({','.join([r"%s"] * len(columns))})"""
        current_entry = []
        counter = 0
        try:
            for entry in reader:
                cursor.execute(query, ['-'.join(entry[0].split('/')[::-1]), int(entry[1]), entry[2], entry[3], float(entry[4].replace(',', '.'))])
                counter += 1
                if counter % 10000 == 0:
                    connection.commit() # Committing
            connection.commit() # Committing
        except Error as err:
            print(f"MySQL: Insertion query for second table failed on entry {entry}! Error: '{err}'")
##

## Function to search query for specific time interval
def search_query(connection, interval):
    return execute_query(connection, 
                        f"""
                        SELECT Razão_Social, sum(vl_saldo_final) AS soma 
                        FROM demonstracoes_contabeis_2020_2021 AS dc
                        INNER JOIN relacao_de_operadoras_ativas_ans AS ro
                        ON dc.reg_ans = ro.registro_ans
                        WHERE descricao LIKE "%%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%%"
                        AND data >= DATE_ADD(CURRENT_DATE(), INTERVAL -{interval} MONTH)
                        GROUP BY reg_ans
                        ORDER BY soma DESC
                        LIMIT 10""", True)
##

## Creating and connecting to DB
print("MySQL: Connecting to MySQL and creating database...")
connection = create_server_connection("localhost", "root", root_pass)
execute_query(connection, f"DROP DATABASE {main_db_name}") ## Attempts to drop database if existent
create_database(connection, main_db_name) ## Creates the main DB.
connection = create_server_connection("localhost", "root", root_pass, main_db_name) ## Connects to the main DB.
##

## Creating first table
print("MySQL: Creating first table...")
table_name1 = "relacao_de_operadoras_ativas_ans" ## DB table name
execute_query(connection,
            f"""
            CREATE TABLE {table_name1} (
                Registro_ANS INT,
                CNPJ VARCHAR(14),
                Razão_Social VARCHAR(255),
                Nome_Fantasia VARCHAR(255),
                Modalidade VARCHAR(255),
                Logradouro VARCHAR(255),
                Número VARCHAR(255),
                Complemento VARCHAR(255),
                Bairro VARCHAR(255),
                Cidade VARCHAR(255),
                UF VARCHAR(2),
                CEP VARCHAR(255),
                DDD VARCHAR(255),
                Telefone VARCHAR(255),
                Fax VARCHAR(255),
                Endereço_eletrônico VARCHAR(255),
                Representante VARCHAR(255),
                Cargo_Representante VARCHAR(255),
                Data_Registro_ANS VARCHAR(10),
                PRIMARY KEY (Registro_ANS));
            """)
##

## Inserting CSV in first table
print("MySQL: Inserting CSV in first table...")
insert_csv_t1(connection, table_name1, r'CSVs\Relatorio_cadop.csv')
##

## Creating second table
print("MySQL: Creating second table...")
table_name2 = "demonstracoes_contabeis_2020_2021" ## DB table name
execute_query(connection,
            f"""
            CREATE TABLE {table_name2} (
                data DATE,
                reg_ans INT,
                cd_conta_contabil INT,
                descricao VARCHAR(255),
                vl_saldo_final REAL);
            """)
##

## Creates a table index to speed up search on data, descricao
print("MySQL: Creating index for second table on data, reg_ans, descricao...")
execute_query(connection,
            f"""
            CREATE INDEX registro
            ON {table_name2} (data, reg_ans, descricao);
            """)
##

## Inserting CSVs in second table
print("MySQL: Inserting CSVs in second table...")
insert_csv_t2(connection, table_name2, r'CSVs\1T2020.csv')
insert_csv_t2(connection, table_name2, r'CSVs\2T2020.csv')
insert_csv_t2(connection, table_name2, r'CSVs\3T2020.csv')
insert_csv_t2(connection, table_name2, r'CSVs\4T2020.csv')
insert_csv_t2(connection, table_name2, r'CSVs\1T2021.csv')
insert_csv_t2(connection, table_name2, r'CSVs\2T2021.csv')
insert_csv_t2(connection, table_name2, r'CSVs\3T2021.csv')
##

## Analytic query for: "Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?"
print("MySQL: Running analytic query for: \"Quais as 10 operadoras que mais tiveram despesas com \"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR\" no último trimestre?")
print("MySQL: Result of the search", search_query(connection, 3), sep="\n")
##

## Analytic query for: "Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano?"
print("MySQL: Running analytic query for: \"Quais as 10 operadoras que mais tiveram despesas com \"EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR\" no último ano?")
print("MySQL: Result of the search", search_query(connection, 12), sep="\n")
##