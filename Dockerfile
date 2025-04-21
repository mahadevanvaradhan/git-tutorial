from ubuntu:latest

apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git

RUN pip3 install --upgrade pip

RUN pip3 install \
    PyYAML