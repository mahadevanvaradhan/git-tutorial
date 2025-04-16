from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import HTTPConnector
from . import db
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

hconnector = Blueprint('httpconnector', __name__)

class HTTPConnectorService:
    @staticmethod
    def create(data):
        if not data or "name" not in data or "category" not in data:
            return None, "Invalid input"
        connector = HTTPConnector(
            name=data["name"],
            category=data["category"],
            base_url=data.get("base_url", ""),
            auth_type=data.get("auth_type", "none"),
            auth_config=json.dumps(data.get("auth_config")) if data.get("auth_config") else None,
            created_by=data.get("created_by", current_user.email if current_user.is_authenticated else None)
        )
        try:
            db.session.add(connector)
            db.session.commit()
            return connector, None
        except Exception as e:
            db.session.rollback()
            return None, f"Database error: {str(e)}"

    @staticmethod
    def get_all():
        return HTTPConnector.query.all()

    @staticmethod
    def get_by_id(connector_id):
        return HTTPConnector.query.get(connector_id)

    @staticmethod
    def update(connector_id, data):
        connector = HTTPConnector.query.get(connector_id)
        if not connector:
            return None
        connector.name = data.get("name", connector.name)
        connector.category = data.get("category", connector.category)
        connector.base_url = data.get("base_url", connector.base_url)
        connector.auth_type = data.get("auth_type", connector.auth_type)
        connector.auth_config = json.dumps(data.get("auth_config")) if data.get("auth_config") else connector.auth_config
        connector.created_by = data.get("created_by", connector.created_by)
        db.session.commit()
        return connector

    @staticmethod
    def delete(connector_id):
        connector = HTTPConnector.query.get(connector_id)
        if not connector:
            return False
        db.session.delete(connector)
        db.session.commit()
        return True

# Assume HTTPConnector has an as_dict method; if not, define it
if not hasattr(HTTPConnector, 'as_dict'):
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "base_url": self.base_url,
            "auth_type": self.auth_type,
            "auth_config": self.auth_config,
            "created_by": self.created_by
        }
    HTTPConnector.as_dict = as_dict

@hconnector.route('/connectors/page', methods=['GET'])
@login_required
def connectors_page():
    return render_template('connector.html')

@hconnector.route('/connectors', methods=['GET'])
@login_required
def list_connectors():
    connectors = HTTPConnectorService.get_all()
    return jsonify([connector.as_dict() for connector in connectors]), 200

@hconnector.route('/connectors', methods=['POST'])
@login_required
def create_connector():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            # Convert auth_config to JSON if it's a string
            if "auth_config" in data and isinstance(data["auth_config"], str):
                data["auth_config"] = json.loads(data["auth_config"]) if data["auth_config"] else {}

        logger.debug(f"Received data: {data}")
        if not data or "name" not in data or "category" not in data:
            return jsonify({"error": "Missing required fields: name or category"}), 400

        data["created_by"] = current_user.email
        connector, error = HTTPConnectorService.create(data)
        if error:
            logger.error(f"Error creating connector: {error}")
            return jsonify({"error": error}), 400
        flash("Connector created successfully", "success")
        return jsonify(connector.as_dict()), 201
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@hconnector.route('/connectors/<int:connector_id>', methods=['GET'])
@login_required
def get_connector(connector_id):
    connector = HTTPConnectorService.get_by_id(connector_id)
    if not connector:
        return jsonify({"error": "Connector not found"}), 404
    return jsonify(connector.as_dict()), 200

@hconnector.route('/connectors/<int:connector_id>', methods=['PUT'])
@login_required
def update_connector(connector_id):
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            if "auth_config" in data and isinstance(data["auth_config"], str):
                data["auth_config"] = json.loads(data["auth_config"]) if data["auth_config"] else {}

        logger.debug(f"Received data for update: {data}")
        if not data:
            return jsonify({"error": "No data provided"}), 400
        data["created_by"] = current_user.email
        connector = HTTPConnectorService.update(connector_id, data)
        if not connector:
            return jsonify({"error": "Connector not found"}), 404
        flash("Connector updated successfully", "success")
        return jsonify(connector.as_dict()), 200
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@hconnector.route('/connectors/<int:connector_id>', methods=['DELETE'])
@login_required
def delete_connector(connector_id):
    success = HTTPConnectorService.delete(connector_id)
    if not success:
        return jsonify({"error": "Connector not found"}), 404
    flash("Connector deleted successfully", "success")
    return jsonify({"message": "Connector deleted successfully"}), 200