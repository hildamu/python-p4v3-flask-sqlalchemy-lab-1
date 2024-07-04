# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    with Session(db.engine) as session:
        earthquake = session.get(Earthquake, id)
    
    if earthquake is None:
        return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)
    
    response = {
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    }
    return make_response(jsonify(response), 200)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    with Session(db.engine) as session:
        earthquakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
    
    response = {
        'count': len(earthquakes),
        'quakes': [
            {
                'id': eq.id,
                'location': eq.location,
                'magnitude': eq.magnitude,
                'year': eq.year
            }
            for eq in earthquakes
        ]
    }

    print(f"Response for magnitude {magnitude}: {response}")

    return make_response(jsonify(response), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
