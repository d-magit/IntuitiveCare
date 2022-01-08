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
        print("MySQL: Connection successful!")
    except Error as err:
        print(f"MySQL: Connection failed! Error: '{err}'")
    return connection
##

## Function to create a database
def create_database(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE " + name)
        print("MySQL: Database created successfully!")
    except Error as err:
        print(f"MySQL: Creating database failed! Error: '{err}'")
##

## Function to execute a single query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("MySQL: Query executed successfully!")
    except Error as err:
        print(f"MySQL: Executing query '{query}' failed! Error: '{err}'")
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
        try:
            for entry in reader:
                cursor.execute(query, [entry[0], int(entry[1]), int(entry[2]), entry[3], float(entry[4].replace(',', '.'))])
            connection.commit()
        except Error as err: # Committing
            print(f"MySQL: Insertion query for second table failed on entry {entry}! Error: '{err}'")
##


## Creating and connecting to DB
create_database(create_server_connection("localhost", "root", root_pass), main_db_name) ## Creates the main DB, if non-existent.
connection = create_server_connection("localhost", "root", root_pass, main_db_name) ## Connects to the main DB.
##

## Creating first table
table_name = "relacao_de_operadoras_ativas_ans" ## DB table name
execute_query(connection,
            f"""
            CREATE TABLE {table_name} (
                Registro_ANS INT,
                CNPJ VARCHAR(1000),
                Razão_Social VARCHAR(1000),
                Nome_Fantasia VARCHAR(1000),
                Modalidade VARCHAR(1000),
                Logradouro VARCHAR(1000),
                Número VARCHAR(1000),
                Complemento VARCHAR(1000),
                Bairro VARCHAR(1000),
                Cidade VARCHAR(1000),
                UF VARCHAR(2),
                CEP VARCHAR(1000),
                DDD VARCHAR(1000),
                Telefone VARCHAR(1000),
                Fax VARCHAR(1000),
                Endereço_eletrônico VARCHAR(1000),
                Representante VARCHAR(1000),
                Cargo_Representante VARCHAR(1000),
                Data_Registro_ANS VARCHAR(10));
            """)
##

## Inserting CSV in first table
insert_csv_t1(connection, table_name, r'CSVs\Relatorio_cadop.csv')
print("Finished inserting CSV and mounting first table!")
##

## Creating second table
table_name = "demonstracoes_contabeis_2020_2021" ## DB table name
execute_query(connection,
            f"""
            CREATE TABLE {table_name} (
                DATA VARCHAR(10),
                REG_ANS INT,
                CD_CONTA_CONTABIL INT,
                DESCRICAO VARCHAR(1000),
                VL_SALDO_FINAL REAL);
            """)
##

## Inserting CSVs in second table
insert_csv_t2(connection, table_name, r'CSVs\1T2020.csv')
insert_csv_t2(connection, table_name, r'CSVs\2T2020.csv')
insert_csv_t2(connection, table_name, r'CSVs\3T2020.csv')
insert_csv_t2(connection, table_name, r'CSVs\4T2020.csv')
insert_csv_t2(connection, table_name, r'CSVs\1T2021.csv')
insert_csv_t2(connection, table_name, r'CSVs\2T2021.csv')
insert_csv_t2(connection, table_name, r'CSVs\3T2021.csv')
print("Finished inserting CSVs and mounting second table!")
##