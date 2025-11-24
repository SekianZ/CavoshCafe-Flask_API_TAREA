from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)


# 🟢 /api/login -> sp_getCliente
@app.post("/api/login")
def login():
    data = request.get_json() or {}
    correo = data.get("correo")
    passwordd = data.get("passwordd")

    if not correo or not passwordd:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Faltan campos: correo y passwordd"
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("CALL sp_getCliente(%s, %s)", (correo, passwordd))
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    success = len(rows) > 0
    data_resp = rows[0] if success else None
    message = "Cliente registrado" if success else "Cliente no registrado"

    return jsonify({
        "success": success,
        "data": data_resp,
        "message": message
    })


# 🟦 /api/registrar -> sp_setCliente
@app.post("/api/registrar")
def registrar():
    data = request.get_json() or {}

    id_value = int(data.get("id", 0))
    nombres = data.get("nombres")
    correo = data.get("correo")
    passwordd = data.get("passwordd")

    if not nombres or not correo or not passwordd:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Faltan campos: nombres, correo, passwordd"
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("CALL sp_setCliente(%s, %s, %s, %s)", (
            id_value,
            nombres,
            correo,
            passwordd
        ))
        rows = cursor.fetchall()  # autocommit evita problemas
    finally:
        cursor.close()
        conn.close()

    # 1) Si recién se creó
    if id_value == 0 and len(rows) > 0 and "insertID" in rows[0]:
        new_id = int(rows[0]["insertID"])
        return jsonify({
            "success": True,
            "data": {
                "id": new_id,
                "nombres": nombres,
                "correo": correo,
                "passwordd": passwordd
            },
            "message": "Cliente registrado"
        })

    # 2) Error del SP (correo repetido o cliente inexistente)
    if len(rows) > 0 and "error" in rows[0]:
        return jsonify({
            "success": False,
            "data": None,
            "message": rows[0]["error"]
        })

    # 3) Update exitoso
    return jsonify({
        "success": True,
        "data": None,
        "message": "Cliente actualizado"
    })


# 🟡 /api/codigo -> sp_getClienteCodigo
@app.post("/api/codigo")
def generar_codigo():
    data = request.get_json() or {}
    correo = data.get("correo")

    if not correo:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Falta el campo: correo"
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("CALL sp_getClienteCodigo(%s)", (correo,))
        rows = cursor.fetchall()
    except Exception:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return jsonify({
            "success": False,
            "data": None,
            "message": "El servidor no está disponible"
        }), 500

    cursor.close()
    conn.close()

    # Caso correcto
    if len(rows) > 0 and "codigo" in rows[0]:
        return jsonify({
            "success": True,
            "data": {"codigo": rows[0]["codigo"]},
            "message": "Cliente generado"
        })

    # Error del SP
    if len(rows) > 0 and "error" in rows[0]:
        return jsonify({
            "success": False,
            "data": None,
            "message": rows[0]["error"]
        })

    # Ultimo caso
    return jsonify({
        "success": False,
        "data": None,
        "message": "No se pudo generar el código"
    })


# 🟣 Servidor
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
