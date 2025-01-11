import pandas as pd
import mysql.connector

# Correspondance entre les noms de colonnes Excel et les noms de colonnes de la base de données
column_mapping = {
    'Place': 'place',
    'Nom': 'nom',
    'N.Licence': 'date_naissance',
    'Club/Ville/Pays': 'club',
    'dossard': 'dossard',
    'Net timing': 'net_timing'
}

# Chemin vers le fichier Excel
# excel_file = "data\Résultats 5km Casa 2023 Femmes.csv"
# competition_id = 1
# excel_file = "data\Résultats 5km Casa 2023 Hommes.csv"
# competition_id = 2
# excel_file = "data\Résultats 10km Casa 2023 Femmes.csv"
# competition_id = 3
excel_file = "data\Résultats 10km Casa 2023 Hommes.csv"
competition_id = 4

table_association_name = "participant_competition_association"

# Informations de connexion à la base de données
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "dossarddb"

# Nom de la table dans laquelle vous souhaitez insérer les données
table_name = "participant"

# Fonction pour insérer des données dans une table en spécifiant manuellement les noms de colonnes
def insert_data(connection, table_name, data, column_mapping, competition_id):
    try:
        cursor = connection.cursor()
        for i, row in data.iterrows():
            # Insert into participant table
            participant_values = ','.join(['"' + str(row[excel_column]) + '"' for excel_column in column_mapping.keys()])
            participant_query = f"INSERT INTO {table_name} ({','.join(column_mapping.values())}) VALUES ({participant_values})"
            cursor.execute(participant_query)
            
            # Insert into association table
            participant_id = cursor.lastrowid
            association_query = f"INSERT INTO {table_association_name} (id_competition, id_participant) VALUES ({competition_id}, {participant_id})"
            cursor.execute(association_query)
        
        connection.commit()
        print("Données insérées avec succès dans la table", table_name)
    except mysql.connector.Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")

# Fonction pour se connecter à la base de données
def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connexion à la base de données réussie")
            return connection
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

# Charger les données depuis le fichier Excel
try:
    # df = pd.read_csv(excel_file, delimiter=';', encoding='latin1')
    df = pd.read_csv(excel_file, delimiter=';', encoding='latin1', names=column_mapping.keys())
    print("Données chargées avec succès depuis le fichier CSV")
except FileNotFoundError:
    print("Le fichier CSV spécifié est introuvable")
    exit()

# Se connecter à la base de données
connection = connect_to_database(db_host, db_user, db_password, db_name)
if connection:
    # Insérer les données dans la table en spécifiant manuellement les noms de colonnes
    insert_data(connection, table_name, df, column_mapping, competition_id)
    # Fermer la connexion à la base de données
    connection.close()
