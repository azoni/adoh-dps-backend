from flask import Flask, Markup
from flask_cors import CORS
import weapon_rebalance

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    output = ""
    for weapon in weapon_rebalance.weapons:
        output += weapon + " " + str(round(weapon_rebalance.weapons[weapon]['weapon_damage'], 2)) + '<br>'
    
    return output

if __name__ == '__main__':
    app.run(debug=True)
