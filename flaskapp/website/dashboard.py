from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import APIConfig
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import json

dboard = Blueprint('dashboard', __name__)

def validate_json_field(field):
    try:
        if field and field.strip():
            json.loads(field)
        return True
    except json.JSONDecodeError:
        return False

@dboard.route('/dashboard')
@login_required
def dashboard():
    configs = APIConfig.query.all()
    return render_template('dashboard.html', configs=configs)

@dboard.route('/add', methods=['GET', 'POST'])
@login_required
def add_config():
    if request.method == 'POST':
        data = request.form
        # Validate required fields
        if 'method' not in data or 'base_url' not in data:
            return render_template('form.html', action='Create', config=data, error='Missing required fields: method or base_url')

        # Validate method
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if data['method'] not in allowed_methods:
            return render_template('form.html', action='Create', config=data, error=f'Invalid HTTP method. Must be one of {allowed_methods}')

        # Validate JSON fields
        if not validate_json_field(data.get('headers', '{}')):
            return render_template('form.html', action='Create', config=data, error='Invalid JSON in headers')
        if not validate_json_field(data.get('parameters', '{}')):
            return render_template('form.html', action='Create', config=data, error='Invalid JSON in parameters')
        if not validate_json_field(data.get('body', '{}')):
            return render_template('form.html', action='Create', config=data, error='Invalid JSON in body')

        try:
            config = APIConfig(
                method=data['method'],
                base_url=data['base_url'].strip(),
                url_path=data.get('url_path', '').strip(),
                headers=data.get('headers', '{}'),
                parameters=data.get('parameters', '{}'),
                body=data.get('body', '{}'),
                retries=int(data.get('retries', 3)),
                delay_response=int(data.get('delay_response', 0)),
                created_by=data.get('created_by', current_user.email if current_user else ''),
                auth_type=data.get('auth_type', 'none'),
                basic_username=data.get('basic_username', '') if data.get('auth_type') == 'basic' else '',
                basic_password=data.get('basic_password', '') if data.get('auth_type') == 'basic' else '',
                bearer_token=data.get('bearer_token', '') if data.get('auth_type') == 'bearer' else '',
                api_key=data.get('api_key', '') if data.get('auth_type') == 'api_key' else '',
                api_key_value=data.get('api_key_value', '') if data.get('auth_type') == 'api_key' else ''
            )
            db.session.add(config)
            db.session.commit()
            flash('Configuration added successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except ValueError as e:
            return render_template('form.html', action='Create', config=data, error=f'Invalid value: {str(e)}')
    return render_template('form.html', action='Create', config=None)

@dboard.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_config(id):
    config = APIConfig.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        # Validate required fields
        if 'method' not in data or 'base_url' not in data:
            return render_template('form.html', action='Edit', config=config, error='Missing required fields: method or base_url')

        # Validate method
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if data['method'] not in allowed_methods:
            return render_template('form.html', action='Edit', config=config, error=f'Invalid HTTP method. Must be one of {allowed_methods}')

        # Validate JSON fields
        if not validate_json_field(data.get('headers', '{}')):
            return render_template('form.html', action='Edit', config=config, error='Invalid JSON in headers')
        if not validate_json_field(data.get('parameters', '{}')):
            return render_template('form.html', action='Edit', config=config, error='Invalid JSON in parameters')
        if not validate_json_field(data.get('body', '{}')):
            return render_template('form.html', action='Edit', config=config, error='Invalid JSON in body')

        try:
            config.method = data['method']
            config.base_url = data['base_url'].strip()
            config.url_path = data.get('url_path', '').strip()
            config.headers = data.get('headers', '{}')
            config.parameters = data.get('parameters', '{}')
            config.body = data.get('body', '{}')
            config.retries = int(data.get('retries', 3))
            config.delay_response = int(data.get('delay_response', 0))
            config.created_by = data.get('created_by', current_user.email if current_user else '')
            config.auth_type = data.get('auth_type', 'none')
            config.basic_username = data.get('basic_username', '') if data.get('auth_type') == 'basic' else ''
            config.basic_password = data.get('basic_password', '') if data.get('auth_type') == 'basic' else ''
            config.bearer_token = data.get('bearer_token', '') if data.get('auth_type') == 'bearer' else ''
            config.api_key = data.get('api_key', '') if data.get('auth_type') == 'api_key' else ''
            config.api_key_value = data.get('api_key_value', '') if data.get('auth_type') == 'api_key' else ''
            db.session.commit()
            flash('Configuration updated successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except ValueError as e:
            return render_template('form.html', action='Edit', config=config, error=f'Invalid value: {str(e)}')
    return render_template('form.html', action='Edit', config=config)

@dboard.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_config(id):
    config = APIConfig.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    flash('Configuration deleted successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@dboard.route('/generate_tool', methods=['POST'])
@login_required
def generate_tool():
    selected_ids = request.form.getlist('selected_ids')
    configs = APIConfig.query.filter(APIConfig.id.in_(selected_ids)).all()

    with open('tool.py', 'w') as f:
        f.write("import requests\nfrom typing import Any, Dict, List\n\n")  # Simplified header

        for config in configs:
            func_name = f"{config.method.lower()}_{config.url_path.strip('/').replace('/', '_')}"
            func_name = func_name.replace('-', '_')

            param_args = []
            param_dict = json.loads(config.parameters or '{}')
            for key, val in param_dict.items():
                default_val = f'"{val}"' if isinstance(val, str) else val
                param_args.append(f'{key}: str = {default_val}')
            args_signature = ", ".join(param_args) or ""
            args_dict = ",\n        ".join([f'"{k}": {k}' for k in param_dict]) if param_dict else ""

            headers_dict = json.loads(config.headers or '{}')
            if config.auth_type == 'basic' and config.basic_username and config.basic_password:
                headers_dict['Authorization'] = f"Basic {config.basic_username}:{config.basic_password}"
            elif config.auth_type == 'bearer' and config.bearer_token:
                headers_dict['Authorization'] = f"Bearer {config.bearer_token}"
            elif config.auth_type == 'api_key' and config.api_key and config.api_key_value:
                headers_dict[config.api_key] = config.api_key_value

            f.write(f"def {func_name}({args_signature}) -> Any:\n")
            f.write(f"    \"\"\"Auto-generated {config.method.upper()} method for {config.url_path}\"\"\"\n")
            f.write(f"    url = \"{config.base_url.rstrip('/') + '/' + config.url_path.lstrip('/')}\"\n")
            f.write(f"    headers = {json.dumps(headers_dict, indent=4)}\n")

            if config.method.upper() in ['GET', 'DELETE']:
                f.write(f"    params = {{\n        {args_dict}\n    }}\n")
            if config.method.upper() in ['POST', 'PUT']:
                f.write(f"    json_data = {json.dumps(json.loads(config.body or '{}'), indent=4)}\n")

            f.write("    try:\n")
            f.write(f"        response = requests.{config.method.lower()}(\n")
            f.write(f"            url,\n")
            f.write(f"            headers=headers,\n")
            if config.method.upper() in ['GET', 'DELETE']:
                f.write("            params=params,\n")
            elif config.method.upper() in ['POST', 'PUT']:
                f.write("            json=json_data,\n")
            f.write("        )\n")
            f.write("        response.raise_for_status()\n")
            f.write("        return response.json()\n")
            f.write("    except requests.exceptions.RequestException as e:\n")
            f.write("        return f\"Request failed: {e}\"\n\n")

    flash('tool.py generated successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))