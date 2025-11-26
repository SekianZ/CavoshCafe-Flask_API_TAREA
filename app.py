# app.py - API SIMPLE PARA ESTUDIANTES
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random
from models import db, Cliente, CodigoVerificacion

app = Flask(__name__)

# ========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ========================================
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@127.0.0.1:3306/CavoshCafe"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ========================================
# 1️⃣ REGISTRAR CLIENTE
# ========================================
@app.post("/api/registrar")
def registrar():
    # Obtener los datos del JSON
    datos = request.get_json()
    
    id_cliente = int(datos.get("id", 0))
    nombres = datos.get("nombres")
    correo = datos.get("correo")
    passwordd = datos.get("passwordd")

    # Validar que lleguen todos los campos
    if not nombres or not correo or not passwordd:
        return jsonify({
            "success": False,
            "message": "Faltan datos: nombres, correo o passwordd"
        }), 400

    # ========================================
    # CASO 1: Crear nuevo cliente (id = 0)
    # ========================================
    if id_cliente == 0:
        # Buscar si el correo ya existe
        existe = Cliente.query.filter_by(Correo=correo).first()
        
        if existe:
            return jsonify({
                "success": False,
                "message": "El correo ya está registrado"
            })

        # Crear el nuevo cliente
        nuevo_cliente = Cliente(
            Nombres=nombres,
            Correo=correo,
            Passwordd=passwordd
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Cliente registrado",
            "data": {
                "id": nuevo_cliente.id,
                "nombres": nuevo_cliente.Nombres,
                "correo": nuevo_cliente.Correo
            }
        })

    # ========================================
    # CASO 2: Actualizar cliente (id > 0)
    # ========================================
    else:
        # Buscar el cliente por ID
        cliente = Cliente.query.get(id_cliente)
        
        if not cliente:
            return jsonify({
                "success": False,
                "message": "Cliente no existe"
            })

        # Actualizar los datos
        cliente.Nombres = nombres
        cliente.Correo = correo
        cliente.Passwordd = passwordd
        
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Cliente actualizado"
        })


# ========================================
# 2️⃣ LOGIN (INICIAR SESIÓN)
# ========================================
@app.post("/api/login")
def login():
    # Obtener datos del JSON
    datos = request.get_json()
    
    correo = datos.get("correo")
    passwordd = datos.get("passwordd")

    # Validar que lleguen los campos
    if not correo or not passwordd:
        return jsonify({
            "success": False,
            "message": "Faltan campos: correo y passwordd"
        }), 400

    # Buscar cliente con ese correo y contraseña
    cliente = Cliente.query.filter_by(
        Correo=correo,
        Passwordd=passwordd
    ).first()

    # Si no existe
    if not cliente:
        return jsonify({
            "success": False,
            "message": "Correo o contraseña incorrectos"
        })

    # Si existe, devolver los datos
    return jsonify({
        "success": True,
        "message": "Login exitoso",
        "data": {
            "id": cliente.id,
            "nombres": cliente.Nombres,
            "correo": cliente.Correo
        }
    })


# ========================================
# 3️⃣ GENERAR CÓDIGO DE VERIFICACIÓN
# ========================================
@app.post("/api/codigo")
def generar_codigo():
    # Obtener el correo
    datos = request.get_json()
    correo = datos.get("correo")

    if not correo:
        return jsonify({
            "success": False,
            "message": "Falta el correo"
        }), 400

    # Buscar si el cliente existe
    cliente = Cliente.query.filter_by(Correo=correo).first()
    
    if not cliente:
        return jsonify({
            "success": False,
            "message": "Correo no registrado"
        })

    # Generar un código de 4 dígitos al azar
    codigo = str(random.randint(1000, 9999))

    # Calcular cuándo caduca (5 minutos después)
    fecha_caducidad = datetime.utcnow() + timedelta(minutes=5)

    # Guardar el código en la base de datos
    nuevo_codigo = CodigoVerificacion(
        idCliente=cliente.id,
        Codigo=codigo,
        FechaCaducidad=fecha_caducidad
    )
    
    db.session.add(nuevo_codigo)
    db.session.commit()

    # Devolver el código (en producción se enviaría por correo)
    return jsonify({
        "success": True,
        "message": "Código generado",
        "data": {
            "codigo": codigo  # ⚠️ Solo para pruebas
        }
    })


# ========================================
# 4️⃣ VALIDAR CÓDIGO
# ========================================
@app.post("/api/validar-codigo")
def validar_codigo():
    # Obtener datos
    datos = request.get_json()
    
    correo = datos.get("correo")
    codigo = datos.get("codigo")

    if not correo or not codigo:
        return jsonify({
            "success": False,
            "message": "Faltan campos: correo y codigo"
        }), 400

    # Buscar el cliente
    cliente = Cliente.query.filter_by(Correo=correo).first()
    
    if not cliente:
        return jsonify({
            "success": False,
            "message": "Correo no registrado"
        })

    # Buscar el código más reciente de ese cliente
    codigo_db = CodigoVerificacion.query.filter_by(
        idCliente=cliente.id,
        Codigo=codigo
    ).order_by(CodigoVerificacion.FechaCaducidad.desc()).first()

    # Si no existe el código
    if not codigo_db:
        return jsonify({
            "success": False,
            "message": "Código incorrecto"
        })

    # Verificar si ya caducó
    ahora = datetime.utcnow()  # ⚠️ Cambiar a utcnow()
    
    if ahora > codigo_db.FechaCaducidad:
        return jsonify({
            "success": False,
            "message": "Código caducado"
        })

    # ✅ Código válido
    return jsonify({
        "success": True,
        "message": "Código válido",
        "data": {
            "id": cliente.id,
            "correo": cliente.Correo
        }
    })


# ========================================
# 🚀 INICIAR EL SERVIDOR
# ========================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        print("✅ Base de datos lista")
        print("🚀 Servidor corriendo en http://127.0.0.1:5000")

    app.run(debug=True, host="127.0.0.1", port=5000)