from flask import Flask, jsonify, request, render_template
import psycopg2
import psycopg2.extras
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # habilitar CORS para permitir llamadas desde el HTML

# 👉 Cambia estos datos por los tuyos
DB_HOST = "localhost"
DB_NAME = "movilidad"
DB_USER = "postgres"
DB_PASS = "Diego"    # <-- pon tu contraseña real aquí
DB_PORT = "5432"


def obtener_conexion():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )


@app.route("/")
def index():
    # esto sirve si quieres renderizar plantillas, pero si solo abres el HTML local, no es necesario
    return "Backend en funcionamiento."


# ✅ Ruta para consultar todos los sitios (GET)
@app.route("/api/sitios", methods=["GET"])
def obtener_sitios():
    conn = obtener_conexion()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM sitios;")
    rows = cur.fetchall()

    sitios = []
    for row in rows:
        sitios.append({
            "id": row["id"],
            "nombre": row["nombre"],
            "email": row["email"],
            "estado_inmueble": row["estado_inmueble"],
            "estrato_usuario": row["estrato_usuario"]
        })

    cur.close()
    conn.close()

    return jsonify(sitios)


# ✅ Ruta para insertar un sitio nuevo (POST)
@app.route("/api/sitios", methods=["POST"])
def crear_sitio():
    data = request.get_json()

    nombre = data.get("nombre")
    email = data.get("email")
    estado_inmueble = data.get("estado")
    estrato_usuario = data.get("estrato")

    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sitios (nombre, email, estado_inmueble, estrato_usuario)
        VALUES (%s, %s, %s, %s)
    """, (nombre, email, estado_inmueble, estrato_usuario))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "Sitio creado exitosamente."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
