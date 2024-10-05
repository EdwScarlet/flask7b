from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()

    return render_template("app.html")

# Ejemplo de ruta GET usando templates para mostrar una vista
@app.route("/alumnos")
def alumnos():
    con.close()

    return render_template("alumnos.html")

# Ejemplo de ruta POST para ver cómo se envia la informacion
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código usado en las prácticas
def notificarActualizacionRegistroCurso(args):
    pusher_client = pusher.Pusher(
        app_id="1867161",
        key="fa5d8bfda2ad7ea780a1",
        secret="e8b305488c131008f14b",
        cluster="us2",
        ssl=True
    )
    
    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", args)

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Curso, Nombre_Cursos, Telefono FROM tst0_cursos 
    ORDER BY Id_Curso DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    try:
        if not con.is_connected():
            con.reconnect()

        id = request.form["id"]
        nombre_curso = request.form["curso"]
        telefono = request.form["telefono"]

        cursor = con.cursor()

        if id:
            sql = """
            UPDATE tst0_cursos SET
            Nombre_Curso = %s,
            Telefono = %s
            WHERE Id_Curso = %s
            """
            val = (nombre_curso, telefono, id)
        else:
            sql = """
            INSERT INTO tst0_cursos (Nombre_Curso, Telefono)
                            VALUES (%s, %s)
            """
            val = (nombre_curso, telefono)

        cursor.execute(sql, val)
        con.commit()

        # Definir args como un diccionario
        args = {
            "id": id,
            "nombre_curso": nombre_curso,
            "telefono": telefono
        }

        # Pasar args a la función notificarActualizacionRegistroCurso
        notificarActualizacionRegistroCurso(args)

    except Exception as e:
        return str(e), 500
    
    finally:
        cursor.close()
        con.close()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Curso, Nombre_Cursos, Telefono FROM tst0_cursos
    WHERE Id_Curso = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_cursos
    WHERE Id_Cursos = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionRegistroCurso()

    return make_response(jsonify({}))
