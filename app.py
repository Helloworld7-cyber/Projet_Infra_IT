@app.route('/fiche_nom/<nom>')
def fiche_nom(nom):
    auth = request.authorization
    if not auth or auth.username != 'user' or auth.password != '12345':
        return Response('Login requis', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    # ... code de recherche ...
@app.route('/disponibles')
def livres_disponibles():
    conn = get_db_connection()
    # On filtre pour ne garder que les livres où disponible est égal à 1
    livres = conn.execute('SELECT * FROM livres WHERE disponible = 1').fetchall()
    conn.close()
    return render_template('bibliotheque.html', livres=livres)

@app.route('/emprunter/<int:id_livre>')
def emprunter_livre(id_livre):
    conn = get_db_connection()
    # On met à jour le livre : disponible devient 0
    conn.execute('UPDATE livres SET disponible = 0 WHERE id = ?', (id_livre,))
    conn.commit()
    conn.close()
    return f"Livre {id_livre} emprunté !"

@app.route('/supprimer_livre/<int:id_livre>')
def supprimer(id_livre):
    # Ajoute ici ton contrôle d'accès user/12345
    conn = get_db_connection()
    conn.execute('DELETE FROM livres WHERE id = ?', (id_livre,))
    conn.commit()
    conn.close()
    return "Livre retiré de la bibliothèque."

@app.route('/recherche/<titre>')
def recherche(titre):
    conn = get_db_connection()
    # On cherche les livres qui contiennent le titre spécifié
    livres = conn.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',)).fetchall()
    conn.close()
    return render_template('bibliotheque.html', livres=livres)

