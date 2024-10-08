from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import mysql.connector
import datetime
import pytz

# Configura Pusher
pusher_client = Pusher(
    app_id="1867161",
    key="fa5d8bfda2ad7ea780a1",
    secret="e8b305488c131008f14b",
    cluster="us2",
    ssl=True
)

# Configura la conexión MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("app.html")

# Crear un nuevo curso
@app.route("/create", methods=["POST"])
def create_course():
    con = get_db_connection()
    cursor = con.cursor()
    curso = request.form["curso"]
    telefono = request.form["telefono"]

    cursor.execute("INSERT INTO tst0_cursos (Nombre_Cursos, Telefono) VALUES (%s, %s)", (curso, telefono))
    con.commit()

    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", {
        "curso": curso,
        "telefono": telefono
    })

    return jsonify({"status": "success"})

# Leer todos los cursos
@app.route("/read", methods=["GET"])
def read_courses():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT Id_Curso, Nombre_Cursos, Telefono FROM tst0_cursos ORDER BY Id_Curso DESC")
    courses = cursor.fetchall()

    cursor.close()
    con.close()

    return jsonify(courses)

# Actualizar un curso
@app.route("/update", methods=["POST"])
def update_course():
    con = get_db_connection()
    cursor = con.cursor()
    course_id = request.form["id"]
    curso = request.form["curso"]
    telefono = request.form["telefono"]

    cursor.execute("UPDATE tst0_cursos SET Nombre_Cursos = %s, Telefono = %s WHERE Id_Curso = %s", (curso, telefono, course_id))
    con.commit()

    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", {
        "id": course_id,
        "curso": curso,
        "telefono": telefono
    })

    return jsonify({"status": "success"})

# Eliminar un curso
@app.route("/delete", methods=["POST"])
def delete_course():
    con = get_db_connection()
    cursor = con.cursor()
    course_id = request.form["id"]

    cursor.execute("DELETE FROM tst0_cursos WHERE Id_Curso = %s", (course_id,))
    con.commit()

    cursor.close()
    con.close()

    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", {
        "id": course_id
    })

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
