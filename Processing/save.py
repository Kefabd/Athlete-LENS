import os

# Fonction pour sauvegarder l'image localement
def save_images_locally(image_file, dest_folder):
    # Définir le chemin complet pour enregistrer l'image
    filename = os.path.join(dest_folder, image_file.filename)
    # Sauvegarder l'image à l'emplacement défini
    image_file.save(filename)
    print("Image", image_file.filename, "saved locally successfully.")

# Fonction pour sauvegarder l'image dans la base de données MySQL
def save_image_to_database(image_file, source_folder, db):
    cursor = db.cursor()  # Créer un curseur pour interagir avec la base de données

    # SQL pour insérer l'image dans la table images
    sql_insert_image = "INSERT INTO images (filename, data, id_competition) VALUES (%s, %s, %s)"

    # Lire le fichier image en mode binaire
    with open(os.path.join(source_folder, image_file.filename), "rb") as file:
        image_data = file.read()
    
    # Préparer les valeurs pour l'insertion
    val_image = (image_file.filename, image_data, 1)

    # Exécuter la requête d'insertion
    cursor.execute(sql_insert_image, val_image)

    # Récupérer l'ID de l'image insérée
    id_image = cursor.lastrowid

    # Valider la transaction
    db.commit()
    
    print("Image", image_file.filename, "saved in the database successfully.")
    
    # Fermer le curseur après l'insertion
    cursor.close()

    return id_image  # Retourner l'ID de l'image insérée

# Fonction pour sauvegarder le dossard dans la base de données
def save_dossard(dossard, id_image, db):
    cursor = db.cursor()  # Créer un curseur pour interagir avec la base de données

    # SQL pour insérer l'association image-dossard dans la table dossard_image
    sql_insert_dossard_images = "INSERT INTO dossard_image (image_id, dossard_id) VALUES (%s, %s)"

    # Préparer les valeurs pour l'insertion
    val_dossard_images = (id_image, dossard)
    
    # Exécuter la requête d'insertion
    cursor.execute(sql_insert_dossard_images, val_dossard_images)

    # Valider la transaction
    db.commit()
    
    print("OCR results saved in the database successfully.")
    
    # Fermer le curseur après l'insertion
    cursor.close()
