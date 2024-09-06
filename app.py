import pandas as pd
import os
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

# Créer un dossier pour stocker temporairement les fichiers téléchargés
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home():
    return 'API Analyse des Tickets - Utilisez /generate-sorted-analysis pour envoyer des fichiers Excel.'

@app.route('/generate-sorted-analysis', methods=['POST'])
def generate_sorted_analysis():
    try:
        # Vérifier si les fichiers sont présents dans la requête
        if 'tickets_non_archives' not in request.files or 'tickets_archives' not in request.files:
            return jsonify({'error': 'Fichiers manquants'}), 400

        # Récupérer les fichiers Excel téléchargés
        non_archives_file = request.files['tickets_non_archives']
        archives_file = request.files['tickets_archives']

        # Sauvegarder temporairement les fichiers Excel
        non_archives_file_path = os.path.join('uploads', 'tickets_non_archives.xlsx')
        archives_file_path = os.path.join('uploads', 'tickets_archives.xlsx')
        non_archives_file.save(non_archives_file_path)
        archives_file.save(archives_file_path)

        # Charger les fichiers Excel dans des DataFrames pandas
        non_archives_df = pd.read_excel(non_archives_file_path, engine='openpyxl')
        archives_df = pd.read_excel(archives_file_path, engine='openpyxl')

        # Fusionner les deux DataFrames
        merged_df = pd.concat([non_archives_df, archives_df])

        # Nettoyer les noms de colonnes
        merged_df.columns = merged_df.columns.str.strip()

        # Vérifier si la colonne 'Créé le' existe
        if 'Créé le' not in merged_df.columns:
            return jsonify({'error': "La colonne 'Créé le' est manquante dans les fichiers Excel"}), 400

        # Convertir la colonne 'Créé le' en format date
        merged_df['Créé le'] = pd.to_datetime(merged_df['Créé le'], errors='coerce')

        # Trier le DataFrame fusionné par la colonne 'Créé le'
        sorted_df = merged_df.sort_values(by='Créé le')

        # Utiliser un fichier temporaire pour sauvegarder le fichier trié
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            sorted_df.to_excel(tmp.name, index=False, engine='openpyxl')

        # Optionnel: Vous pouvez déplacer le fichier temporaire dans 'uploads' si nécessaire
        output_path = os.path.join('uploads', 'sorted_analysis_tickets.xlsx')
        os.rename(tmp.name, output_path)

        return jsonify({'message': 'Document sorted_analysis_tickets généré avec succès.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
