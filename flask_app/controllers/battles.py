from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, session, redirect, flash
from flask_app.models.battle import Battle
from flask_app.models.companion import Companion



#start battle, store all stats into session 
@app.route('/battle_start')
def battle_start():
    data = {
        'id' : session['companion_id']
    }
    if 'boss_health' in session:
        session.pop('boss_health')
    if 'combat_text' in session:
        session.pop('combat_text')
    session['boss_health'] = 100
    session['boss_strength'] = 10
    session['boss_defense'] = 5
    session['boss_luck'] = 0
    session['companion'] = Companion.get_one(data)
    session['companion_max_health'] = session['companion'].health
    session['companion_img'] = session['companion'].picture
    session['companion_health'] = session['companion'].health
    session['companion_strength'] = session['companion'].strength
    session['companion_defense'] = session['companion'].defense
    session['companion_luck'] = session['companion'].luck
    session['ability1'] = session['companion'].ablility1
    session['ability2'] = session['companion'].ablility2
    session['ability3'] = session['companion'].ablility3
    session['combat_text'] = ['Catzilla has arrived! Roll the dice to attack!!']
    session['gg'] = False
    session['score'] = 0
    if session['boss_defense'] >= session['companion_strength']:
        flash('This companion is too weak to fight Catzilla!')
        return redirect('/dashboard') #goes back to character selection
    return render_template('battle_page.html') #enter battle page

#battle on-going (Without resetting session)
@app.route('/ongoing')
def battle_ongoing():
    return render_template('') #battle page

#roll the dice
@app.route('/roll_dice')
def roll_dice():
    data = {
        'id' : session['companion_id']
    }
    companion_luck = session['companion_luck']
    boss_luck = session['boss_luck']
    character = session['companion'].name
    ability_used = Battle.ability()
    ability_name = session[f'{ability_used}']
    #companion roll
    if Battle.roll_dice(companion_luck):
        damage_dealt = session['companion_strength'] - session['boss_defense']
        session['combat_text'] += f'{character} used {ability_name} and successfully dealt {damage_dealt} to Catzilla!'
        session['boss_health'] -= damage_dealt
        session['score'] += 50
        if session['boss_health'] <= 0:
            session['combat_text'] += f'Catzilla is defeated by {character}!!'
            session['gg'] = True
            session['level_gain'] = 2
            session['result'] = True
            session['score'] += 500
    else:
        session['score'] += 25
        session['combat_text'] += f'{character} used {ability_name} but it missed Catzilla!'
    #if battle ended skip boss turn
    if session['gg']:
        return redirect('/ongoing')
    #boss roll
    if Battle.roll_dice(boss_luck):
        boss_damage = session['boss_strength'] - session['companion_defense']
        session['combat_text'] += f'Catzilla retaliated and dealt {boss_damage} to {character}!'
        session['companion_health'] -= boss_damage
        if session['companion_health'] <= 0:
            session['combat_text'] += f'{character} is defeated by Catzilla!!'
            session['gg'] = True
            session['level_gain'] = 1
            session['result'] = False
            session['score'] += 100
    else:
        session['combat_text'] += f'Catzilla attacked but {character} dodged it!'    
    return redirect('/ongoing')

#battle end
@app.route('/end_battle')
def end():
    #update data into database
    data = {
        'id' : session['companion_id'],
        'score' : session['score'],
        'level' : session['level_gain']
    }
    #adds win/loss to data
    if session['result']:
        data['win'] = 1
        data['loss'] = 0
    else:
        data['win'] = 0
        data['loss'] = 1
    Companion.update_score(data)
    #level up stat update
    data['health'] = session['level_gain'] * 3
    data['strength'] = session['level_gain'] * 1
    data['defense'] = 0
    data['luck'] = 0
    Companion.update_stat(data)
    return render_template('battle_result.html') #result page