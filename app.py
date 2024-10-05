from flask import Flask, request, jsonify
from flask_cors import CORS
import weapon_rebalance

app = Flask(__name__)
CORS(app)

@app.route('/calculate_damage', methods=['POST'])
def calculate_damage():
    data = request.get_json()  # Receive the JSON payload sent from the React frontend
    immunities = data.get('immunities')
    resists = data.get('resists', [])
    weapon = data.get('weapon', [])
    player = data.get('player', [])
    ac = data.get('armorClass')
    is_crit_immune = data.get('criticalHitImmunity')
    is_sneak_immune = data.get('sneakAttackImmunity')
    if not weapon:
        return "No Weapon Selected"
    print(immunities)
    print(resists)
    print(weapon)
    print(player)
    weapon_rebalance.damage_type_weights['physical'] = (100 - int(immunities[0]['value'])) / 100
    weapon_rebalance.damage_type_weights['fire'] = (100 - int(immunities[1]['value'])) / 100
    weapon_rebalance.damage_type_weights['cold'] = (100 - int(immunities[2]['value'])) / 100
    weapon_rebalance.damage_type_weights['electrical'] = (100 - int(immunities[3]['value'])) / 100
    weapon_rebalance.damage_type_weights['acid'] = (100 - int(immunities[4]['value'])) / 100
    weapon_rebalance.damage_type_weights['sonic'] = (100 - int(immunities[5]['value'])) / 100
    weapon_rebalance.damage_type_weights['negative'] = (100 - int(immunities[6]['value'])) / 100
    weapon_rebalance.damage_type_weights['positive'] = (100 - int(immunities[7]['value'])) / 100
    weapon_rebalance.damage_type_weights['divine'] = (100 - int(immunities[8]['value'])) / 100
    weapon_rebalance.damage_type_weights['magical'] = (100 - int(immunities[9]['value'])) / 100
    weapon_rebalance.damage_type_weights['pure'] = (100 - int(immunities[10]['value'])) / 100
    
    for w in weapon_rebalance.new_purple_weapons:
        weapon_rebalance.calculate_damage(w, weapon_rebalance.new_purple_weapons[w], True, player['keen'], player["Imp Crit"], is_crit_immune, is_sneak_immune)
    print(weapon_rebalance.weapons[weapon]['damage'])


    return jsonify({'damage': weapon_rebalance.weapons})

@app.route('/')
def home():
    try:
        return jsonify(weapon_rebalance.weapons)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return a JSON error response

if __name__ == '__main__':
    app.run(debug=True)
