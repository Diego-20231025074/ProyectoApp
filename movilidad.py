from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras
from flask_cors import CORS
import json

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
    return "✅ Backend en funcionamiento."


# ==========================================
# ✅ RUTAS PARA SITIOS
# ==========================================

# GET → consultar todos los sitios
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


# POST → insertar un nuevo sitio
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

    return jsonify({"mensaje": "✅ Sitio creado exitosamente."})


# ==========================================
# ✅ RUTAS PARA RUTAS
# ==========================================

# POST → insertar una nueva ruta
@app.route("/api/rutas", methods=["POST"])
def crear_ruta():
    data = request.get_json()

    usuario = data.get("usuario")
    coordenadas = data.get("coordenadas")

    conn = obtener_conexion()
    cur = conn.cursor()

    # Guardar coordenadas como JSON
    cur.execute("""
        INSERT INTO rutas (usuario, coordenadas)
        VALUES (%s, %s)
    """, (usuario, json.dumps(coordenadas)))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "✅ Ruta guardada correctamente."})


# GET → consultar todas las rutas
@app.route("/api/rutas", methods=["GET"])
def obtener_rutas():
    conn = obtener_conexion()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM rutas;")
    rows = cur.fetchall()

    rutas = []
    for row in rows:
        rutas.append({
            "id": row["id"],
            "usuario": row["usuario"],
            "fecha": row["fecha"].isoformat() if row["fecha"] else None,
            "coordenadas": row["coordenadas"]
        })

    cur.close()
    conn.close()

    return jsonify(rutas)


# ==========================================
# ✅ RUTAS PARA REPORTES DE PROBLEMAS
# ==========================================

# POST → insertar un nuevo reporte
@app.route("/api/reportes", methods=["POST"])
def crear_reporte():
    data = request.get_json()

    tipo = data.get("tipo")
    comentario = data.get("comentario")
    latitud = data.get("latitud")
    longitud = data.get("longitud")

    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reportes (tipo, comentario, latitud, longitud)
        VALUES (%s, %s, %s, %s)
    """, (tipo, comentario, latitud, longitud))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "✅ Reporte guardado correctamente."})


# GET → consultar todos los reportes
@app.route("/api/reportes", methods=["GET"])
def obtener_reportes():
    conn = obtener_conexion()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM reportes;")
    rows = cur.fetchall()

    reportes = []
    for row in rows:
        reportes.append({
            "id": row["id"],
            "tipo": row["tipo"],
            "comentario": row["comentario"],
            "latitud": row["latitud"],
            "longitud": row["longitud"],
            "fecha": row["fecha"].isoformat() if row["fecha"] else None
        })

    cur.close()
    conn.close()

    return jsonify(reportes)


# ==========================================
# ✅ RUTAS PARA PROPUESTAS
# ==========================================

# POST → insertar propuesta
@app.route("/api/propuestas", methods=["POST"])
def crear_propuesta():
    data = request.get_json()

    usuario = data.get("usuario")
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")

    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO propuestas (usuario, titulo, descripcion)
        VALUES (%s, %s, %s)
    """, (usuario, titulo, descripcion))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "✅ Propuesta enviada correctamente."})


# GET → consultar todas las propuestas
@app.route("/api/propuestas", methods=["GET"])
def obtener_propuestas():
    conn = obtener_conexion()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM propuestas;")
    rows = cur.fetchall()

    propuestas = []
    for row in rows:
        propuestas.append({
            "id": row["id"],
            "usuario": row["usuario"],
            "titulo": row["titulo"],
            "descripcion": row["descripcion"],
            "fecha": row["fecha"].isoformat() if row["fecha"] else None
        })

    cur.close()
    conn.close()

    return jsonify(propuestas)


if __name__ == "__main__":
    app.run(debug=True, port=5000)



