@app.route('/fiche_nom/<nom>')
def fiche_nom(nom):
    auth = request.authorization
    if not auth or auth.username != 'user' or auth.password != '12345':
        return Response('Login requis', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    # ... code de recherche ...
