import requests
# CORRECTION : On ajoute "request" dans les imports de flask ci-dessous
from flask import Flask, jsonify, render_template, request

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

# Modification pour correspondre au standard Flask de ton projet
@app.route("/paris", methods=["GET"])
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

VILLES_COORDONNEES = {
    "marseille": {"lat": 43.2965, "lon": 5.3698},
    "rennes":    {"lat": 48.1173, "lon": -1.6778},
    "paris":     {"lat": 48.8566, "lon": 2.3522},
    "toulouse":  {"lat": 43.6047, "lon": 1.4442},
    "bordeaux":  {"lat": 44.8378, "lon": -0.5792}
}

@app.route("/openmeteo", methods=["GET"])
def api_meteo():
    # 1. Récupérer la ville demandée dans l'URL (ex: /openmeteo?ville=rennes)
    # Si aucune ville n'est précisée, on prend Marseille par défaut.
    ville_choisie = request.args.get('ville', 'marseille').lower()

    # 2. Vérifier si la ville demandée est bien dans notre liste
    if ville_choisie not in VILLES_COORDONNEES:
        return jsonify({
            "error": f"Ville non supportée. Choisissez parmi : {', '.join(VILLES_COORDONNEES.keys()).title()}"
        }), 400

    # 3. Récupérer les coordonnées correspondantes
    coords = VILLES_COORDONNEES[ville_choisie]
    
    # 4. Construire l'URL dynamique d'Open-Meteo avec f-string
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=wind_speed_10m"

    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.RequestException as e:
        return jsonify({"error": f"Erreur Open-Meteo: {e}"}), 502

    data = response.json()
    speed = data["current"]["wind_speed_10m"]
    
    # On renvoie aussi le nom de la ville pour que le JavaScript puisse mettre à jour les titres !
    return jsonify({
        "ville": ville_choisie.title(),
        "wind_speed": speed
    })

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)