from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost:3306/db_facturas'
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    codigo_usuario = db.Column(db.String(50), primary_key=True)
    nit_usuario = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    clasificacion = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    ultima_lectura = db.Column(db.Float)
    ultimo_consumo = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consulta', methods=['POST'])
def consulta():
    data = request.json
    nit_usuario = data.get('nitUsuario')

    usuario = Usuario.query.filter_by(nit_usuario=nit_usuario).first()

    if usuario:
        return jsonify({
            'success': True,
            'usuario': {
                'nombre': usuario.nombre,
                'clasificacion': usuario.clasificacion,
                'direccion': usuario.direccion,
                'ultima_lectura': usuario.ultima_lectura,
                'ultimo_consumo': usuario.ultimo_consumo
            }
        })
    else:
        return jsonify({'success': False}), 404

@app.route('/resultado.html')
def resultado():
    return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)