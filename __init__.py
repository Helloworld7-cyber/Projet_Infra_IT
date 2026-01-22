from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                                                                                                                                    
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
    return conn

# Fonction pour vérifier si l'utilisateur est connecté
def est_authentifie():
    return session.get('authentifie')
    

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/deconnexion')
def deconnexion():
    session.clear() # Vide la session (username, role, etc.)
    return redirect(url_for('hello_world'))

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return f"<h2>Bienvenue dans la Bibliothèque, {session.get('username')} !</h2><p>Vous êtes connecté en tant que {session.get('role')}.</p>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Admin pour la gestion totale
        if username == 'admin' and password == 'password':
            session['authentifie'] = True
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('lecture'))
            
        # User pour la recherche simple
        elif username == 'user' and password == '12345':
            session['authentifie'] = True
            session['username'] = 'user'
            session['role'] = 'user'
            return redirect(url_for('lecture'))
            
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Recherche de livre par TITRE (Exercice adapté Séquence 6)
@app.route('/fiche_livre/<titre>')
def fiche_livre(titre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Recherche dans la nouvelle table 'livres'
    cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
    data = cursor.fetchall()
    conn.close()
    
    return render_template('read_data.html', data=data)

# Consultation de toute la bibliothèque
@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# Ajouter un nouveau livre à la bibliothèque
@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    # Protection : seul l'admin peut ajouter des livres
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé : Seul l'administrateur peut ajouter des livres.", 403

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Insertion dans la table livres selon le nouveau schema.sql
        cursor.execute('INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)', (titre, auteur, annee))
        conn.commit()
        conn.close()
        return redirect(url_for('ReadBDD'))
        
    return render_template('formulaire_livre.html') # Assurez-vous d'avoir ce template

# --- ROUTES DU MINI GESTIONNAIRE DE TÂCHES ---

@app.route('/taches')
def liste_taches():
    conn = get_db_connection()
    taches = conn.execute('SELECT * FROM taches').fetchall()
    conn.close()
    return render_template('gestion_taches.html', taches=taches)

@app.route('/taches/ajouter', methods=['POST'])
def ajouter_tache():
    titre = request.form['titre']
    description = request.form['description']
    echeance = request.form['echeance']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO taches (titre, description, echeance) VALUES (?, ?, ?)',
                 (titre, description, echeance))
    conn.commit()
    conn.close()
    return redirect('/taches')

@app.route('/taches/terminer/<int:id>')
def terminer_tache(id):
    conn = get_db_connection()
    conn.execute('UPDATE taches SET terminee = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/taches')

@app.route('/taches/supprimer/<int:id>')
def supprimer_tache(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/taches')


if __name__ == "__main__":
  app.run(debug=True)
