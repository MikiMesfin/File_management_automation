# File Organizer

A Django-based file organization system that automatically categorizes and organizes uploaded files based on their types.

## Features
- Automatic file categorization
- Date-based organization
- Duplicate file handling
- Web interface for file upload and management

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`
7. Create required directories: `mkdir -p media/temp`

## Usage
Access the application at http://localhost:8000
- Upload files at /upload/
- View organized files at /files/
