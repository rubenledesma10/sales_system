from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.phone import phone
from models.client import Client
import re

phone_tel = Blueprint("phone", __name__)

@phone_tel.route('/api/get_phones')
def get_phones():
    phones = phone.query.all()
    if not phones:
        return jsonify({"message": "No phones found"}), 200
    return jsonify([phone.serialize() for phone in phones])

@phone_tel.route("/api/phone", methods=["POST"])
def add_phone():
    data = request.get_json()

    required_fields = ("id_client", "phone")
    if not data or not all(key in data for key in required_fields):
        return jsonify({"error": "Required data is missing"}), 400

    for field in required_fields:
        if not str(data.get(field, " ")).strip():
            return jsonify({"error": f"{field.title()} is required and cannot be empty"}), 400

    client = Client.query.get(data["id_client"])
    
    if not client:
        return jsonify({"error": "Client ID not found"}), 404
 
    phone_number = data["phone"]
    if not re.match(r"^\+?\d{7,15}$", phone_number):
        return jsonify({"error": "Phone number format is invalid"}), 400

    existing = phone.query.filter_by(id_client=data["id_client"], phone=phone_number).first()
    if existing:
        return jsonify({"error": "Phone number already registered for this client"}), 409

    try:
        new_phone = phone(
            id_client=data["id_client"],
            phone=phone_number
        )

        db.session.add(new_phone)
        db.session.commit()

        return jsonify({"message": "Phone added successfully", "phone": new_phone.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@phone_tel.route("/api/phone/<int:id_phone>", methods=["DELETE"])
def delete_phone(id_phone):
    phone = phone.query.get(id_phone)

    if not phone:
        return jsonify({"message": "Phone not found"}), 404
    
    try:
        db.session.delete(phone)
        db.session.commit()
        return jsonify({"message": "Phone deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@phone_tel.route("/api/phone/<int:id_phone>", methods=["PUT"])
def update_phone(id_phone):
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400
    
    phone = phone.query.get(id_phone)
    
    if not phone:
        return jsonify({"error": "Phone not found"}), 404
    
    try:
        if "id_client" in data:
            phone.id_client = data["id_client"]
        if "phone" in data:
            phone.phone = data["phone"]
    
        db.session.commit()

        return jsonify({"message": "Phone updated", "phone": phone.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@phone_tel.route("/api/phone/<int:id_phone>", methods=["PATCH"])
def patch_phone(id_phone):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400
    
    phone = phone.query.get(id_phone)

    if not phone:
        return jsonify({"error": "Phone not found"}), 404

    try:
        if "id_client" in data:
            phone.id_client = data["id_client"]
        if "phone" in data:
            phone.phone = data["phone"]
    
        db.session.commit()

        return jsonify({"message": "Phone updated successfully", "phone": phone.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

