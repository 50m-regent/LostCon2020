from flask import Flask, request
import json

from game import Game

app = Flask(__name__)
game = Game(turn=10)

@app.route('/procon-progress', methods=['GET'])
def procon_progress():
    return str(game.progress())

@app.route('/procon-data', methods=['GET'])
def procon_data():
    return json.dumps(game.data.to_json())

if __name__ == "__main__":
    app.run(debug=True)