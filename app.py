from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

# Liste des apps (à adapter)
apps = {
    "thonny": {"port": 14500, "display": 100, "cmd": "thonny"},
    "xterm": {"port": 14500, "display": 100, "cmd": "xterm"},
    "gparted": {"port": 14501, "display": 101, "cmd": "gparted"},
    "arduino": {"port": 14502, "display": 102, "cmd": "arduino"}
}

@app.route("/")
def index():
    return render_template("index.html", apps=apps)

@app.route("/start/<name>")
def start_app(name):
    app_info = apps.get(name)
    if not app_info:
        return jsonify({"status": "error", "message": "App not found"}), 404
    try:
        subprocess.Popen([
            "xpra", "start", f":{app_info['display']}",
            f"--start-child={app_info['cmd']}",
            f"--bind-tcp=0.0.0.0:{app_info['port']}",
            "--html=on"
        ])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/stop/<name>")
def stop_app(name):
    app_info = apps.get(name)
    if not app_info:
        return jsonify({"status": "error", "message": "App not found"}), 404
    try:
        subprocess.run(["xpra", "stop", f":{app_info['display']}"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
