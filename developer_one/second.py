import os

def read_text_file(file_path):
    """Read and return the contents of a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path, data):
    """Write data to a text file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)