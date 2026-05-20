import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def displayContact():
    return render_template("contact.html")

@app.route("/rapport")
def displayReport():
    return render_template("graphique.html")

@app.route("/histogramme")
def displayHistogram():
    return render_template("histogramme.html")

@app.route("/atelier")
def displayWork():
    return render_template("atelier.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/openmeteo", methods=["GET"])
def api_meteo():
    # Données Marseille (Vitesse du vent à 10m)
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.2965&longitude=5.3698&current=wind_speed_10m"

    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.RequestException as e:
        # En Flask, on renvoie un tuple (contenu, code_erreur)
        return jsonify({"error": f"Erreur Open-Meteo: {e}"}), 502

    data = response.json()
    
    # Extraction de la vitesse du vent
    speed = data["current"]["wind_speed_10m"]
    
    # jsonify convertit le dictionnaire en vrai JSON pour ton JavaScript
    return jsonify({"wind_speed": speed})

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
