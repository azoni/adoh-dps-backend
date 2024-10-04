from flask import Flask, request, jsonify
from flask_cors import CORS
import weapon_rebalance

app = Flask(__name__)
CORS(app)

# Example of weapon data for reference, you can replace this with your actual weapon data
immunity_resists = {
    'weapons': {
        'fire': {'weapon_damage': 10},
        'cold': {'weapon_damage': 8},
        'electric': {'weapon_damage': 12},
        'acid': {'weapon_damage': 9},
        'sonic': {'weapon_damage': 7},
        'negative': {'weapon_damage': 5},
        'positive': {'weapon_damage': 11},
        'divine': {'weapon_damage': 13},
        'magical': {'weapon_damage': 15},
        'pure': {'weapon_damage': 20},
    }
}

@app.route('/calculate_damage', methods=['POST'])
def calculate_damage():
    data = request.get_json()  # Receive the JSON payload sent from the React frontend
    immunities = data.get('immunities', [])
    resists = data.get('resists', [])

    total_damage = 0  # Initialize total damage

    # Calculate damage based on immunities and resists
    for weapon_type in immunity_resists['weapons']:
        base_damage = immunity_resists['weapons'][weapon_type]['weapon_damage']
        
        immunity = next((immunity['value'] for immunity in immunities if immunity['type'] == weapon_type), None)
        resist = next((resist['value'] for resist in resists if resist['type'] == weapon_type), None)

        # Apply immunities and resists
        if immunity:
            damage_after_immunity = max(base_damage - float(immunity), 0)
        else:
            damage_after_immunity = base_damage
        
        if resist:
            damage_after_resist = max(damage_after_immunity - float(resist), 0)
        else:
            damage_after_resist = damage_after_immunity
        
        total_damage += damage_after_resist

    return jsonify({'damage': round(total_damage, 2)})

@app.route('/')
def home():
    output = "<ul>"  # Start an unordered list
    
    # for weapon in sorted(weapon_rebalance.weapons):
    #     output += f"<li><strong>{weapon}</strong>: <br> Damage - {round(weapon_rebalance.weapons[weapon]['target_damage'], 2)}<br>"  # Weapon name and damage
        
    #     if weapon in weapon_rebalance.new_purple_weapons:  # Check if weapon has properties
    #         output += "<ul>"  # Start a nested list for properties
    #         for property in weapon_rebalance.new_purple_weapons[weapon]:
    #             output += f"<li>{property}</li>"  # List each property
    #         output += "</ul>"  # End nested list
            
    #     output += "</li><br>"  # End weapon list item
        
    # output += "</ul>"  # End main list
    return jsonify(weapon_rebalance.weapons)

if __name__ == '__main__':
    app.run(debug=True)
