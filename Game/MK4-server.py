from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Erlaubt Anfragen von der Webseite

# Speichert die y-Position der Kreise
player_positions = {"player1": 50, "player2": 50}


@app.route("/update", methods=["POST"])
def update_position():
    """Aktualisiert die Position eines Spielers"""
    data = request.json
    player = data.get("player")  # "player1" oder "player2"
    position = data.get("position")  # Zahl zwischen 0 und 100

    if player in player_positions and 0 <= position <= 100:
        player_positions[player] = position
        return jsonify({"success": True, "message": f"{player} moved to {position}"})

    return jsonify({"success": False, "message": "Invalid input"}), 400


@app.route("/get_positions", methods=["GET"])
def get_positions():
    """Gibt die aktuellen Positionen der Spieler zurück"""
    return jsonify(player_positions)


if __name__ == "__main__":
    app.run(debug=True)
