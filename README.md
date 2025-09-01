# Flask_CRUD

# Flask CRUD Application

A basic setup for a Flask CRUD (Create, Read, Update, Delete) application.

## Features
- Built with Python and Flask
- CRUD operations on database records using SQLAlchemy
- Template rendering with Jinja2
- Static files for CSS and JS support
- Simple and easy to extend

## Prerequisites
- Python 3.x
- Flask
- Flask SQLAlchemy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Flask_CRUD.git
   cd Flask_CRUD
2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate    # On Windows: env\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirement.txt
    ```

## Usage

1. Run the Flask app:
    ```bash
    python app.py
2. Open your browser and go to:
    ```cpp
    http://127.0.0.1:5000/
    ```

## Folder Structure
    
    Flask_CRUD/
    ├── app.py                # Main Flask application
    ├── requirement.txt       # Python dependencies
    ├── static/               # Static files (CSS, JS)
    ├── templates/            # HTML templates
    ├── instance/             # Database file
    └── .gitignore            # Git ignore file