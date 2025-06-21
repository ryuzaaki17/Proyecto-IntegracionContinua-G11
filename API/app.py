from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Equipo(db.Model):
    __tablename__ = 'equipos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    disponibles = db.Column(db.Integer, nullable=False, default=0)

    # Relación para acceder fácilmente a las solicitudes asociadas
    solicitudes = db.relationship('Solicitud', backref='equipo_obj', lazy=True)

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'disponibles': self.disponibles
        }

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))

    # Aquí cambiamos el campo equipo (antes String) a una clave foránea
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'equipo_id': self.equipo_id,
            'equipo_nombre': self.equipo_obj.nombre if self.equipo_obj else None,
            'fecha': self.fecha.isoformat()
        }

# Crear las tablas
with app.app_context():
    db.create_all()

#-----------------------------------------------------------------------------------------------------------------------
#ENDPOINTS PARA TABLA EQUIPOS

#Ruta de prueba
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# Crear equipo
@app.route('/equipos', methods=['POST'])
def create_equipo():
    try:
        data = request.get_json()
        nuevo = Equipo(nombre=data['nombre'], disponibles=data.get('disponibles', 0))
        db.session.add(nuevo)
        db.session.commit()
        return make_response(jsonify({'message': 'equipo creado'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creando equipo'}), 500)

# Obtener todos los equipos
@app.route('/equipos', methods=['GET'])
def get_equipos():
    try:
        equipos = Equipo.query.all()
        return make_response(jsonify([e.json() for e in equipos]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo equipos'}), 500)

# Obtener un equipo por ID
@app.route('/equipos/<int:id>', methods=['GET'])
def get_equipo(id):
    try:
        equipo = Equipo.query.get(id)
        if equipo:
            return make_response(jsonify(equipo.json()), 200)
        return make_response(jsonify({'message': 'equipo no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo equipo'}), 500)

# Actualizar un equipo
@app.route('/equipos/<int:id>', methods=['PUT'])
def update_equipo(id):
    try:
        equipo = Equipo.query.get(id)
        if equipo:
            data = request.get_json()
            equipo.nombre = data['nombre']
            equipo.disponibles = data['disponibles']
            db.session.commit()
            return make_response(jsonify({'message': 'equipo actualizado'}), 200)
        return make_response(jsonify({'message': 'equipo no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error actualizando equipo'}), 500)

# Eliminar un equipo
@app.route('/equipos/<int:id>', methods=['DELETE'])
def delete_equipo(id):
    try:
        equipo = Equipo.query.get(id)
        if equipo:
            db.session.delete(equipo)
            db.session.commit()
            return make_response(jsonify({'message': 'equipo eliminado'}), 200)
        return make_response(jsonify({'message': 'equipo no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error eliminando equipo'}), 500)
    
#-----------------------------------------------------------------------------------------------------------------------
#ENDPOINTS PARA TABLA SOLICITUDES

# Crear solicitud
@app.route('/solicitudes', methods=['POST'])
def create_solicitud():
    try:
        data = request.get_json()
        nueva = Solicitud(
            nombre=data['nombre'],
            correo=data['correo'],
            telefono=data.get('telefono', ''),
            equipo_id=data['equipo_id']
        )
        db.session.add(nueva)
        db.session.commit()
        return make_response(jsonify({'message': 'solicitud creada'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creando solicitud'}), 500)

# Obtener todas las solicitudes
@app.route('/solicitudes', methods=['GET'])
def get_solicitudes():
    try:
        solicitudes = Solicitud.query.all()
        return make_response(jsonify([s.json() for s in solicitudes]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo solicitudes'}), 500)

# Obtener una solicitud por ID
@app.route('/solicitudes/<int:id>', methods=['GET'])
def get_solicitud(id):
    try:
        solicitud = Solicitud.query.get(id)
        if solicitud:
            return make_response(jsonify(solicitud.json()), 200)
        return make_response(jsonify({'message': 'solicitud no encontrada'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo solicitud'}), 500)

# Actualizar una solicitud
@app.route('/solicitudes/<int:id>', methods=['PUT'])
def update_solicitud(id):
    try:
        solicitud = Solicitud.query.get(id)
        if solicitud:
            data = request.get_json()
            solicitud.nombre = data['nombre']
            solicitud.correo = data['correo']
            solicitud.telefono = data['telefono']
            solicitud.equipo_id = data['equipo_id']
            db.session.commit()
            return make_response(jsonify({'message': 'solicitud actualizada'}), 200)
        return make_response(jsonify({'message': 'solicitud no encontrada'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error actualizando solicitud'}), 500)

# Eliminar una solicitud
@app.route('/solicitudes/<int:id>', methods=['DELETE'])
def delete_solicitud(id):
    try:
        solicitud = Solicitud.query.get(id)
        if solicitud:
            db.session.delete(solicitud)
            db.session.commit()
            return make_response(jsonify({'message': 'solicitud eliminada'}), 200)
        return make_response(jsonify({'message': 'solicitud no encontrada'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error eliminando solicitud'}), 500)


#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
