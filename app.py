import os
# Permet d'éviter les erreurs de duplication de bibliothèque pour certaines configurations
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Importation des modules nécessaires
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from Processing.save import *
from Processing.detector import detect_dossard
from Processing.search import search_images_from_bib

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'Dossard@Nadia2002'  # Clé secrète pour les sessions et les cookies
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Chemin d'accès au répertoire temporaire pour stocker les images téléchargées

# Assurez-vous que le répertoire d'upload existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dossarddb"
)

# Définir la route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html', css_file='style.css')  # Rendre le template de la page d'accueil

# Route pour le téléchargement d'images
@app.route('/upload', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'GET':
        show_alert = request.args.get('show_popup')
        # Afficher le formulaire de téléchargement
        return render_template('upload.html', show_popup=show_alert)
    else:
        # Gérer l'upload des images
        image_files = request.files.getlist("image")

        if not image_files or all(f.filename == '' for f in image_files):
            # No files were uploaded or all filenames are empty
            return redirect(url_for('upload_images', show_popup="error"))

        # Envoyer les images localement et dans la base de données

        for image_file in image_files:
            # Sauvegarder l'image localement
            save_images_locally(image_file, app.config['UPLOAD_FOLDER'])
            
            # Détecter les dossards dans l'image
            extracted_bibs = detect_dossard(os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename))
            
            # Sauvegarder les informations de l'image dans la base de données
            id_image = save_image_to_database(image_file, app.config['UPLOAD_FOLDER'], mydb)
            
            # Sauvegarder les dossards détectés dans la base de données
            for bib in extracted_bibs:
                if bib is not None:
                    save_dossard(bib, id_image, mydb)
        
        # Rediriger l'utilisateur vers la même page après le téléchargement
        return redirect(url_for('upload_images', show_popup="success"))

# Route pour afficher le formulaire de recherche et gérer les recherches
@app.route('/search', methods=['GET', 'POST'])
def search_images():
    if request.method == 'GET':
        return render_template('search.html')  # Afficher le formulaire de recherche
    else:
        search_query = request.form['dossard_number']  # Récupérer le numéro de dossard saisi
        image_files = search_images_from_bib(search_query, mydb)  # Rechercher les images correspondantes
        
        # Vérifier si des résultats ont été trouvés
        no_results = not bool(image_files)
        
        # Afficher les résultats de recherche
        return render_template('search.html', image_files=image_files, no_results=no_results)

# Route pour afficher toutes les images stockées
@app.route('/images')
def show_all_images():
    # Récupérer les données de toutes les images à partir de la base de données
    cursor = mydb.cursor()
    sql = "SELECT id, filename, data FROM images"
    cursor.execute(sql)
    images = cursor.fetchall()
    
    # Afficher les images récupérées dans un modèle HTML
    return render_template('shows.html', images=images)


# Démarrer l'application Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True)
