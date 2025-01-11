# Importation des modules nécessaires
from ultralytics import YOLO  # Pour la détection d'objets
import cv2  # Pour le traitement d'images
from paddleocr import PaddleOCR  # Pour la reconnaissance optique de caractères (OCR)
import os

# Initialisation de l'OCR avec l'option de classification d'angle et la langue anglaise
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Chargement du modèle YOLO pour la détection de dossards
model = YOLO('Detectors/bestFinalOne.pt')

# Fonction pour extraire le texte de la région d'intérêt détectée
def extract_dossard(region_detected):
    texts = ocr.ocr(region_detected, cls=True)  # Utiliser l'OCR pour détecter le texte
    texts_extracted = []  # Liste pour stocker les textes extraits
    
    for text in texts:
        if text is not None:
            for line in text:
                # Vérifier la confiance de la détection de texte
                if line[1][1] > 0.5:
                    try:
                        # Essayer de convertir le texte en entier
                        extracted_int = int(line[1][0])
                        texts_extracted.append(extracted_int)
                        print("line: " + str(extracted_int))
                    except ValueError:
                        # Ignorer le texte qui ne peut pas être converti en entier
                        print(f"Skipping non-integer text")
                        continue
                
                print("line: " + str(line[1][0]))

    return texts_extracted  # Retourner les textes extraits

# Fonction pour détecter les dossards dans les images
def detect_dossard(image):
    results = model.predict(image)  # Utiliser le modèle YOLO pour prédire les dossards
    extracted_bibs = []  # Liste pour stocker les dossards extraits

    # Lire le fichier image
    image = cv2.imread(image)

    for result in results:
        boxes = result.boxes  # Obtenir les boîtes de détection

        if len(boxes) != 0:
            for box in boxes:
                # Afficher les informations sur les objets détectés
                print("Object type:", box.cls[0].item())
                print("Coordinates:", box.xyxy[0].tolist())
                print("Probability:", box.conf[0].item())

                conf = round(box.conf[0].item(), 2)  # Arrondir la confiance à deux décimales
                if conf > 0.55:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Découper la région d'intérêt de l'image originale
                    region = image[y1:y2, x1:x2]
                    extracted_texts = extract_dossard(region)  # Extraire le texte de la région

                    for extracted_bib in extracted_texts:
                        if extracted_bib is not None:
                            extracted_bibs.append(extracted_bib)
    
    return extracted_bibs  # Retourner les dossards extraits
