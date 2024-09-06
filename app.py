from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Créer un dossier pour stocker temporairement les fichiers téléchargés
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Route racine pour éviter l'erreur 404 et afficher un message d'accueil
@app.route('/')
def home():
    return 'API Analyse des Tickets - Utilisez /generate-sorted-analysis pour envoyer des fichiers.'

# Route pour traiter les fichiers envoyés et générer le document sorted_analysis_tickets
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
    # Utiliser la variable d'environnement PORT définie par Render ou 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
