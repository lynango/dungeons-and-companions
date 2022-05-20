from flask import redirect,session,request,render_template,flash
from flask_app import app
from flask_app.models.companion import Companion

#Directs the user to the create companion page
@app.route('/create-companion')
def make_companion():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('create_character.html')

#Directs the user to the update companion page
@app.route('/update-companion')
def update_companion():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('update_character.html')

#Process the user's request to create a new companion
@app.route('/create/companion', methods=['POST'])
def create_companion():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "name": request.form["name"],
        "breed": request.form["breed"],
        "profession": request.form["profession"],
        "weapon": request.form["weapon"],
        "ability1": request.form["ability1"],
        "ability2": request.form["ability2"],
        "ability3": request.form["ability3"],
        "picture": request.form["picture"],
        "story": request.form["story"]
    }
    Companion.create(data)
    return redirect('/dashboard')

#Process the user's request to update their companion 
# (breed, profession, and weapon cannot be updated)
@app.route('/edit/companion', methods=['POST'])
def editCompanion():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "name": request.form["name"],
        "ability1": request.form["ability1"],
        "ability2": request.form["ability2"],
        "ability3": request.form["ability3"],
        "picture": request.form["picture"],
        "story": request.form["story"]
    }
    Companion.update_info(data)
    return redirect('/dashboard')

#Process the user's request to "retire" their companion
@app.route('/delete/companion/<int:id>')
def retire_companion(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Companion.delete(data)
    return redirect('/dashboard')