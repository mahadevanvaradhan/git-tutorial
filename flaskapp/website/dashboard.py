from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import APIConfig
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import uuid
import json

dboard = Blueprint('dashboard', __name__)

@dboard.route('/dashboard')
def dashboard():
    configs = APIConfig.query.all()
    return render_template('dashboard.html', configs=configs)

@dboard.route('/add', methods=['GET', 'POST'])
def add_config():
    if request.method == 'POST':
        config = APIConfig(
            method=request.form['method'],
            base_url=request.form['base_url'],
            url_path=request.form['url_path'],
            parameters=json.loads(request.form['parameters'] or '{}'),
            body=json.loads(request.form['body'] or '{}'),
            retries=int(request.form['retries'] or 3),
            delay_response=int(request.form['delay_response'] or 0),
            created_by=int(request.form['created_by'])
        )
        db.session.add(config)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return render_template('form.html', action='Add', config=None)

@dboard.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_config(id):
    config = APIConfig.query.get_or_404(id)
    if request.method == 'POST':
        config.method = request.form['method']
        config.base_url = request.form['base_url']
        config.url_path = request.form['url_path']
        config.parameters = json.loads(request.form['parameters'] or '{}')
        config.body = json.loads(request.form['body'] or '{}')
        config.retries = int(request.form['retries'] or 3)
        config.delay_response = int(request.form['delay_response'] or 0)
        config.created_by = int(request.form['created_by'])
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return render_template('form.html', action='Edit', config=config)

@dboard.route('/delete/<int:id>', methods=['POST'])
def delete_config(id):
    config = APIConfig.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    return redirect(url_for('dashboard'))

# @dboard.route('/generate_tool', methods=['POST'])
# def generate_tool():
#     selected_ids = request.form.getlist('selected_ids')
#     configs = APIConfig.query.filter(APIConfig.id.in_(selected_ids)).all()
#     with open('tool.py', 'w') as f:
#         for config in configs:
#             f.write(f"# API ID: {config.api_id}\n")
#             f.write(f"import requests\n")
#             f.write(f"response = requests.{config.method.lower()}(\"{config.base_url}{config.url_path}\",\n")
#             f.write(f"    params={json.dumps(config.parameters)},\n")
#             f.write(f"    json={json.dumps(config.body)}\n")
#             f.write(f")\nprint(response.status_code, response.text)\n\n")
#     return redirect(url_for('dashboard.dashboard'))

@dboard.route('/generate_tool', methods=['POST'])
def generate_tool():
    selected_ids = request.form.getlist('selected_ids')
    configs = APIConfig.query.filter(APIConfig.id.in_(selected_ids)).all()

    with open('tool.py', 'w') as f:
        f.write("import requests\nfrom typing import Any, Dict, List\nfrom mcp import tool\n\n")  # Header

        for config in configs:
            func_name = f"{config.method.lower()}_{config.url_path.strip('/').replace('/', '_')}"
            func_name = func_name.replace('-', '_')

            param_args = []
            param_dict = config.parameters or {}
            for key, val in param_dict.items():
                default_val = f'"{val}"' if isinstance(val, str) else val
                param_args.append(f'{key}: str = {default_val}')
            args_signature = ", ".join(param_args) or ""
            args_dict = ",\n        ".join([f'"{k}": {k}' for k in param_dict]) if param_dict else ""

            f.write(f"@tool()\n")
            f.write(f"def {func_name}({args_signature}) -> Any:\n")
            f.write(f"    \"\"\"\n    Auto-generated {config.method.upper()} method for {config.url_path}\n    \"\"\"\n")
            f.write(f"    url = \"{config.base_url.rstrip('/') + '/' + config.url_path.lstrip('/')}\"\n")

            if config.method.upper() in ['GET', 'DELETE']:
                f.write(f"    params = {{\n        {args_dict}\n    }}\n")
            if config.method.upper() in ['POST', 'PUT']:
                f.write(f"    json_data = {json.dumps(config.body or {}, indent=4)}\n")

            f.write("    try:\n")
            f.write(f"        response = requests.{config.method.lower()}(\n")
            f.write(f"            url,\n")
            if config.method.upper() in ['GET', 'DELETE']:
                f.write("            params=params\n")
            elif config.method.upper() in ['POST', 'PUT']:
                f.write("            json=json_data\n")
            f.write("        )\n")
            f.write("        response.raise_for_status()\n")
            f.write("        return response.json()\n")
            f.write("    except requests.exceptions.RequestException as e:\n")
            f.write("        return f\"Request failed: {e}\"\n\n")

    return redirect(url_for('dashboard.dashboard'))
