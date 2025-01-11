# Fonction pour rechercher des images contenant le dossard spécifié
def search_images_from_bib(dossard_searched, db):
    cursor = db.cursor()  # Créer un curseur pour interagir avec la base de données
    
    # SQL pour récupérer les noms de fichiers des images contenant le dossard recherché
    sql = """
        SELECT i.filename
        FROM images i
        WHERE i.id IN (
            SELECT di.image_id
            FROM dossard_image di
            WHERE di.dossard_id = %s
        )
    """
    
    # Exécuter la requête en remplaçant le paramètre par le dossard recherché
    cursor.execute(sql, (dossard_searched,))
    
    # Récupérer les résultats de la requête et extraire les noms de fichiers des images
    image_files = [row[0] for row in cursor.fetchall()]
    
    # Fermer le curseur après l'exécution de la requête
    cursor.close()
    
    # Retourner la liste des noms de fichiers des images correspondant au dossard recherché
    return image_files
