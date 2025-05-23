from flask import Blueprint, jsonify, request
from models.db import db
from models.category import Category
from models.product import Product

category_db = Blueprint ("category", __name__)

@category_db.route('/api/get_category')
def get_category():
    categories=Category.query.all() 
    if not categories:
        return jsonify({"message" : "unregistered category"}),404
    return jsonify([category.serialize() for category in categories]),200

@category_db.route("/api/category/<int:id>")
def get_id_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify ({"message" : "Category not found" }),404
    return jsonify (category.serialize()),200

@category_db.route("/api/create_category", methods=["POST"])
def add_category():
    data = request.get_json()

    required_fields = ("name", "description")
    if not data or not all(key in data for key in required_fields):
        return jsonify({"error": "Required data is missing"}), 400

    for field in required_fields:
        if not str(data.get(field, " ")).strip():
            return jsonify({"error": f"{field.title()} is required and cannot be empty"}), 400

    try:
        print(f"Data received: {data}")

        new_category = Category(
            name=data["name"],
            description=data["description"]
        )

        print(f"Creating Category: {new_category.name}, {new_category.description}")

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "Category created successfully",
            "category": new_category.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@category_db.route("/api/category/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({"message": "Category not found"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@category_db.route("/api/up_category/<int:id>", methods=["PUT"])
def update_category(id):
    data= request.get_json()

    if not data:
        return jsonify ({"message":"no data recived"}), 400
    
    category = Category.query.get(id)
    
    if not category:
        return jsonify ({"error": "Category not found"}), 404
    try:
        if "name" in data:
            category.name= data["name"]
        if "description" in data:
            category.description= data["description"]
    
        db.session.commit()

        return jsonify ({"message":"Update category", "category": category.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@category_db.route("/api/up_category/<int:id>", methods=["PATCH"])
def edit_category(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400


    category = Category.query.get(id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    try:

        if "name" in data:
            name = data["name"]
            if isinstance(name, str) and name.strip():
                category.name = name.strip()
            else:
                return jsonify({"error": "The 'name' field cannot be empty"}), 400

        if "description" in data:
            description = data["description"]
            if isinstance(description, str) and description.strip():
                category.description = description.strip()
            else:
                return jsonify({"error": "The 'description' field cannot be empty"}), 400

        db.session.commit()

        return jsonify({
            "message": "Category updated successfully",
            "category": category.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# @category_db.route("/api/up_category/<int:id>", methods=["PATCH"])
# def edit_category(id):
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "No data received"}), 400
    
#     category = Category.query.get(id)

#     if not category:
#         return jsonify({"error": "Category not found"}), 404

#     try:
#         if "name" in data:
#             category.name = data["name"]
#         if "description" in data:
#             category.description = data["description"]
    
#         db.session.commit()

#         return jsonify({"message": "Category updated successfully", "category": category.serialize()}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": f"Internal error: {str(e)}"}), 500






    

    
        




