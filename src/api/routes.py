"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from werkzeug.security import generate_password_hash, check_password_hash

import os
import cloudinary
import cloudinary.uploader

from flask_mail import Message
from datetime import datetime, timedelta, timezone


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# //////////////////////////////////////////////////////////registro


@api.route('/user', methods=['POST'])
def create_user():
    # siempre en formato JSON
    data = request.get_json()

    # verificando que el mensaje no este vacio
    if not data:
        return jsonify({"msg": "no se proporcionaron datos"}), 400

    # extraer los valores de los campos
    email = data.get("email")

    username = data.get("username")

    # validar si el email esta registrado
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "ya existe un usuario registrado con ese email"}), 409

# esta linea genera la clave encriptada
    hashed_password = generate_password_hash(data["password"])

    # crea un registro nuevo
    new_user = User(
        email=email,
        password=hashed_password,
        username=username
    )

    # debe ser guardada en la base de datos
    db.session.add(new_user)

    try:
        # confirmar los cambios de forma permanente
        db.session.commit()
        return jsonify(new_user.serialize()), 201

    except Exception as error:
        # en caso de error se captura la excepcion
        print(f"Error al crear usuario: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500

    # //////////////////////////////////////////////////////// login


@api.route("/login", methods=["POST"])
def login():
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)

    # if username != "test" or password != "test":
    #     return jsonify({"msg": "Bad username or password"}), 401

    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": access_token,
        "user": user.serialize()}), 200

# ////////////////////////////////////////////////////////////// ruta protegida


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# ///////////////////////////////////////////////////////////// cloudinary


@api.route('/upload', methods=['POST'])
def upload_image():
    file = request.files["image"]

    if not file:
        return jsonify({"error": "The files is required"}), 400

    result = cloudinary.uploader.upload(file)

    if 'secure_url' not in result:
        return jsonify({"error": "The image can not be uploaded"}), 400

    return jsonify(result["secure_url"]), 200

# /////////////////////////////////////////////////////////// mail


@api.route('/test-email', methods=['GET'])
def test_email():

    from app import mail

    try:
        msg = Message("Hola desde Flask",
                      sender="test@tuapp.com",
                      recipients=["mata.astrid.01@gmail.com"])
        msg.body = "Si recibes esto en Mailtrap, la configuración es exitosa."
        mail.send(msg)

        return "Correo enviado."

    except Exception as e:
        return str(e)

# /////////////////////////////////////////////////////////// forgot-password

import random

@api.route('/forgot-password', methods=['POST'])
def forgot_password():
    from app import mail
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        code = str(random.randint(100000, 999999))
        user.reset_code = code
        # La expiración es 15 minutos desde ahora
        user.reset_code_expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        db.session.commit()
        
        msg = Message("Tu código de recuperación", recipients=[email], sender="noreply@tuapp.com")
        msg.html = f"Tu código es: <strong>{code}</strong>. Expira en 15 minutos."
        mail.send(msg)

    return jsonify({"message": "Si el email existe, recibirás un código"}), 200




# //////////////////////////////////////////////////////////////////////// endpoint para actualizar la contraseña



@api.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")
    new_password = data.get("password")
    
    user = User.query.filter_by(email=email).first()
    
    # Validaciones
    if not user or user.reset_code != code:
        return jsonify({"message": "Código inválido o usuario no encontrado"}), 400
    
    # Validar expiración (si guardaste reset_code_expires)
    if user.reset_code_expires:
        # Convertimos la fecha de expiración a UTC consciente si no lo es
        expires = user.reset_code_expires
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expires:
            return jsonify({"message": "El código ha expirado"}), 400
    
    # Cambiar contraseña
    user.password = generate_password_hash(new_password)
    user.reset_code = None # Limpiamos el código tras usarlo
    user.reset_code_expires = None
    db.session.commit()
    
    return jsonify({"message": "Contraseña actualizada exitosamente"}), 200