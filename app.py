from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Cake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    description = db.Column(db.Text, unique=False)
    featured = db.Column(db.Boolean)

    def __init__(self, title, description, featured):
        self.title = title
        self.description = description
        self.featured = featured



class CakeSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description', 'featured')


cake_schema = CakeSchema()
cakes_schema = CakeSchema(many=True)

# Endpoint to create a new cake
@app.route('/cake', methods=["POST"])
def add_cake():
    title = request.json['title']
    description = request.json['description']
    featured = request.json['featured']

    new_cake = Cake(title, description, featured)

    db.session.add(new_cake)
    db.session.commit()

    cake = Cake.query.get(new_cake.id)

    return cake_schema.jsonify(cake)

# Endpoint to query all guides
@app.route('/cakes', methods=["GET"])
def get_cakes():
    all_cakes = Cake.query.all()
    result = cakes_schema.dump(all_cakes)

    return jsonify(result.data)


# Endpoint to query a single guide
@app.route('/cake/<id>', methods=["GET"])
def get_cake(id):
    cake = Cake.query.get(id)
    return cake_schema.jsonify(cake)


# Endpoint to update a guide
@app.route('/cake/<id>', methods=["PUT"])
def update_cake(id):
    cake = Cake.query.get(id)
    title = request.json['title']
    description = request.json['description']
    featured = request.json['featured']

    cake.title = title
    cake.description = description
    cake.featured = featured

    db.session.commit()
    return cake_schema.jsonify(cake)


# Endpoint to delete a cake
@app.route('/cake/<id>', methods=["DELETE"])
def delete_cake(id):
    cake = Cake.query.get(id)
    db.session.delete(cake)
    db.session.commit()

    return cake_schema.jsonify(cake)


if __name__ == '__main__':
    app.run(debug=True)

