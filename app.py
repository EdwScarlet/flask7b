from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

def evento():
    pusher_client = pusher.Pusher(
        app_id="1867161",
        key="fa5d8bfda2ad7ea780a1",
        secret="e8b305488c131008f14b",
        cluster="us2",
        ssl=True
    )
    
    pusher_client.trigger("my-channel", "my-event", {})
