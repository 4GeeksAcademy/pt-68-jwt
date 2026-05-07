"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


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
    data= request.get_json()

    #verificando que el mensaje no este vacio
    if not data:
        return jsonify({"msg": "no se proporcionaron datos"}), 400

    #extraer los valores de los campos 
    email= data.get("email")

    username= data.get("username")

    #validar si el email esta registrado
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "ya existe un usuario registrado con ese email"}), 409
    
#esta linea genera la clave encriptada
    hashed_password = generate_password_hash(data["password"])

    
    #crea un registro nuevo 
    new_user= User(
        email= email,
        password=  hashed_password,
        username= username
    )

    #debe ser guardada en la base de datos
    db.session.add(new_user)

    try:
        #confirmar los cambios de forma permanente
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    
    except Exception as error:
         #en caso de error se captura la excepcion
        print(f"Error al crear usuario: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500