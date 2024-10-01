from flask import Flask
from flask_cors import CORS
import weapon_rebalance

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    output = "<ul>"  # Start an unordered list
    
    for weapon in sorted(weapon_rebalance.weapons):
        output += f"<li><strong>{weapon}</strong>: <br> Damage - {round(weapon_rebalance.weapons[weapon]['weapon_damage'], 2)}<br>"  # Weapon name and damage
        
        if weapon in weapon_rebalance.new_purple_weapons:  # Check if weapon has properties
            output += "<ul>"  # Start a nested list for properties
            for property in weapon_rebalance.new_purple_weapons[weapon]:
                output += f"<li>{property}</li>"  # List each property
            output += "</ul>"  # End nested list
            
        output += "</li><br>"  # End weapon list item
        
    output += "</ul>"  # End main list
    return output

if __name__ == '__main__':
    app.run(debug=True)
