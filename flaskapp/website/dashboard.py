from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import APIConfig, HTTPConnector
from . import db
from flask_login import login_required, current_user
import json
import base64

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
        if 'method' not in data or 'base_url' not in data or 'name' not in data:
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error='Missing required fields: name, method or base_url')

        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if data['method'] not in allowed_methods:
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error=f'Invalid HTTP method. Must be one of {allowed_methods}')

        if not validate_json_field(data.get('headers', '{}')):
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error='Invalid JSON in headers')
        if not validate_json_field(data.get('parameters', '{}')):
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error='Invalid JSON in parameters')
        if not validate_json_field(data.get('body', '{}')):
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error='Invalid JSON in body')

        try:
            config = APIConfig(
                name=data['name'].strip(),
                description=data.get('description', ''),  # Added description
                method=data['method'],
                base_url=data['base_url'].strip(),
                url_path=data.get('url_path', '').strip(),
                headers=data.get('headers', '{}'),
                parameters=data.get('parameters', '{}'),
                body=data.get('body', '{}'),
                retries=int(data.get('retries', 3)),
                delay_response=int(data.get('delay_response', 0)),
                created_by=current_user.email,
                authorization_name=data.get('authorization_name', '')
            )
            db.session.add(config)
            db.session.commit()
            flash('Configuration added successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except ValueError as e:
            return render_template('form.html', action='Create', config=data, connectors=HTTPConnector.query.all(), error=f'Invalid value: {str(e)}')
    return render_template('form.html', action='Create', config=None, connectors=HTTPConnector.query.all())

@dboard.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_config(id):
    config = APIConfig.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        if 'method' not in data or 'base_url' not in data or 'name' not in data:
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error='Missing required fields: name, method or base_url')

        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if data['method'] not in allowed_methods:
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error=f'Invalid HTTP method. Must be one of {allowed_methods}')

        if not validate_json_field(data.get('headers', '{}')):
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error='Invalid JSON in headers')
        if not validate_json_field(data.get('parameters', '{}')):
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error='Invalid JSON in parameters')
        if not validate_json_field(data.get('body', '{}')):
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error='Invalid JSON in body')

        try:
            config.name = data['name'].strip()
            config.description = data.get('description', '')  # Added description
            config.method = data['method']
            config.base_url = data['base_url'].strip()
            config.url_path = data.get('url_path', '').strip()
            config.headers = data.get('headers', '{}')
            config.parameters = data.get('parameters', '{}')
            config.body = data.get('body', '{}')
            config.retries = int(data.get('retries', 3))
            config.delay_response = int(data.get('delay_response', 0))
            config.created_by = current_user.email
            config.authorization_name = data.get('authorization_name', '')
            db.session.commit()
            flash('Configuration updated successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except ValueError as e:
            return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all(), error=f'Invalid value: {str(e)}')
    return render_template('form.html', action='Edit', config=config, connectors=HTTPConnector.query.all())

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
        f.write("import os\n")
        f.write("import platform\n")
        f.write("import requests\n")
        f.write("import re\n")
        f.write("import json\n")
        f.write("import datetime\n")
        f.write("import tiktoken\n")
        f.write("import random\n")
        f.write("from typing import Dict, List, Any, Optional\n")
        f.write("from dotenv import load_dotenv\n")
        f.write("from mcp.server.fastmcp import FastMCP\n\n")

        f.write("MCP_SERVER_URL = 'http://localhost:9001'\n\n\n")

        f.write("mcp = FastMCP(\n")
        f.write("    \"Dynamic API Tools\",\n")
        f.write("    instructions=\"Used within MCP Custom Tool calling\",\n")
        f.write("    debug=False,\n")
        f.write("    log_level=\"INFO\",\n")
        f.write("    host=\"0.0.0.0\",\n")
        f.write("    port=9001\n")
        f.write(")\n\n\n")

        for config in configs:
            func_name = config.name.lower().replace(' ', '_').replace('-', '_')
            if not func_name[0].isalpha() and func_name[0] != '_':
                func_name = '_' + func_name

            param_args = []
            param_dict = json.loads(config.parameters or '{}')
            for key, val in param_dict.items():
                default_val = f'"{val}"' if isinstance(val, str) else val
                param_args.append(f'{key}: str = {default_val}')
            args_signature = ", ".join(param_args) or ""
            args_dict = ",\n        ".join([f'"{k}": {k}' for k in param_dict]) if param_dict else ""

            headers_dict = json.loads(config.headers or '{}')
            auth_header = {}
            if config.authorization_name:
                connector = HTTPConnector.query.filter_by(name=config.authorization_name).first()
                if connector and connector.auth_type != 'none':
                    auth_config = json.loads(connector.auth_config) if connector.auth_config else {}
                    if connector.auth_type == 'basic':
                        username = auth_config.get('username', '')
                        password = auth_config.get('password', '')
                        if username and password:
                            encoded = base64.b64encode(f"{username}:{password}".encode()).decode()
                            auth_header['Authorization'] = f"Basic {encoded}"
                    elif connector.auth_type == 'bearer':
                        token = auth_config.get('token', '')
                        if token:
                            auth_header['Authorization'] = f"Bearer {token}"
                    elif connector.auth_type == 'api_key':
                        header = auth_config.get('header', '')
                        value = auth_config.get('value', '')
                        if header and value:
                            auth_header[header] = value

            # Add description as a comment
            if config.description:
                f.write(f"# {config.description}\n")
            f.write("@mcp.tool()\n")
            f.write(f"def {func_name}({args_signature}) -> Any:\n")
            f.write(f'    """description: {config.description} using {config.method.upper()} method for {config.url_path or config.base_url}"""\n')
            f.write(f"    url = \"{config.base_url.rstrip('/') + '/' + config.url_path.lstrip('/')}\"\n")
            f.write(f"    headers = {json.dumps(headers_dict, indent=4)}\n")
            if auth_header:
                f.write(f"    headers.update({json.dumps(auth_header, indent=4)})\n")

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
            f.write("        return f\"Request failed: {{e}}\"\n\n\n")

        f.write("if __name__ == '__main__':\n")
        f.write("    mcp.run(transport='sse')\n")


    flash('tool.py generated successfully!', 'success')
    return redirect(url_for('dashboard.dashboard'))