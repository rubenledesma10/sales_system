from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.phone import Phone
from models.client import Client
import re

phone_tel = Blueprint("phone", __name__)

@phone_tel.route('/api/get_phones')
def get_phones():
    phones = Phone.query.all()
    if not phones:
        return jsonify({"message": "No phones found"}), 404
    return jsonify([Phone.serialize() for Phone in phones]),200

@phone_tel.route('/api/phone/get/<int:id_phone>')
def get_phone(id_phone):
    phone = Phone.query.get(id_phone)
    if not phone:
        return jsonify({'message': 'phone not found'}), 404
    return jsonify(phone.serialize()), 200

@phone_tel.route("/api/clients/<int:id_client>/phones", methods=["POST"])
def add_phone(id_client):
    data = request.get_json()

    required_fields = ("phone",)
    if not data or not all(key in data for key in required_fields):
        return jsonify({"error": "Required data (phone) is missing"}), 400

    for field in required_fields:
        if not str(data.get(field, " ")).strip():
            return jsonify({"error": f"{field.title()} is required and cannot be empty"}), 400

    client = Client.query.get(id_client)

    if not client:
        return jsonify({"error": "Client ID not found"}), 404

    phone_number = data.get("phone")
    if not phone_number or not re.match(r"^\+?\d{7,15}$", phone_number):
        return jsonify({"error": "Phone number format is invalid"}), 400

    existing = Phone.query.filter_by(id_client=id_client, phone=phone_number).first()
    if existing:
        return jsonify({"error": "Phone number already registered for this client"}), 409

    try:
        new_phone = Phone(
            id_client=id_client,
            phone=phone_number
        )

        db.session.add(new_phone)
        db.session.commit()

        return jsonify({"message": "Phone added successfully", "phone": new_phone.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@phone_tel.route("/api/phone_delete/<int:id_phone>", methods=["DELETE"])
def delete_phone(id_phone):
    phone_to_delete = Phone.query.get(id_phone) 

    if not phone_to_delete:
        return jsonify({"message": "Phone not found"}), 404

    try:
        db.session.delete(phone_to_delete)
        db.session.commit()
        return jsonify({"message": "Phone deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@phone_tel.route("/api/phone/<int:id_phone>", methods=["PUT"])
def update_phone(id_phone):
    data = request.get_json()

    if not data and phone:
        return jsonify({"message": "No data received"}), 400

    phone = Phone.query.get(id_phone)

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
    
    phone = Phone.query.get(id_phone)

    if not phone:
        return jsonify({"error": "Phone not found"}), 404

    try:
        if "id_client" in data:
            phone.id_client = data["id_client"]
        if "phone" in data:
            phone.phone = data["phone"]
    
        db.session.commit()

        return jsonify({"message": "Phone updated successfully", "phone": Phone.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

