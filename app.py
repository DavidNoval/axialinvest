from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Créer un dossier pour stocker temporairement les fichiers téléchargés
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/generate-sorted-analysis', methods=['POST'])
def generate_sorted_analysis():
    # Vérifier si les fichiers sont présents dans la requête
    if 'tickets_non_archives' not in request.files or 'tickets_archives' not in request.files:
        return jsonify({'error': 'Fichiers manquants'}), 400

    # Récupérer les fichiers téléchargés
    non_archives_file = request.files['tickets_non_archives']
    archives_file = request.files['tickets_archives']

    # Sauvegarder temporairement les fichiers
    non_archives_file.save(os.path.join('uploads', 'tickets_non_archives.csv'))
    archives_file.save(os.path.join('uploads', 'tickets_archives.csv'))

    # Ici, vous pouvez ajouter votre logique pour analyser et trier les fichiers

    # Pour l'instant, retournons juste un message de succès
    return jsonify({'message': 'Document sorted_analysis_tickets généré avec succès.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
