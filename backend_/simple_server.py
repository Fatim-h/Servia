# simple_server.py
from flask import Flask, jsonify
from app import db
from app.models import NGO, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpassword@localhost/ngodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Servia API is running!", "status": "success"})

@app.route('/api/test')
def test():
    return jsonify({"message": "Test endpoint working!"})

@app.route('/api/ngos')
def get_ngos():
    with app.app_context():
        ngos = NGO.query.all()
        result = []
        for ngo in ngos:
            result.append({
                'id': ngo.ngo_id,
                'name': ngo.name,
                'description': ngo.description,
                'city': ngo.location.city if ngo.location else 'Unknown'
            })
        return jsonify({"data": result, "count": len(result)})

@app.route('/api/categories')
def get_categories():
    with app.app_context():
        categories = Category.query.all()
        result = [{'id': c.category_id, 'name': c.name} for c in categories]
        return jsonify({"data": result})

if __name__ == '__main__':
    print("Starting Simple Server...")
    print("Available at: http://localhost:5000")
    print("Testing endpoints:")
    print("   GET /")
    print("   GET /api/test") 
    print("   GET /api/ngos")
    print("   GET /api/categories")
    app.run(debug=True, port=5000)