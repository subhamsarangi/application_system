# Student Application System

## Project Overview
The Student Application System is a web-based application built with Flask that allows students to submit applications and enables administrators to review and approve them. The system supports user authentication and role-based access control.

## Installation Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (optional but recommended)
- PostgreSQL database

### Setup
1. Clone the repository:
   
```sh
   git clone https://github.com/subhamsarangi/application_system.git
   cd application_system
```

2. Create and activate a virtual environment:
   
```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
   
```sh
   pip install -r requirements.txt
```

4. Configure environment variables:
   - Create a .env file and set the following variables:
     
```env
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/db_name
SECRET_KEY=your_secret_key
```

5. Testing:
    To run tests, use the following command:
    
```sh
    pytest
```

6. Initialize and apply database migrations:
   
```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
```

7. Run create_admin.py:
    
```sh
    python create_admin.py
```

8. Run the application:
   
```sh
   flask run
```

9. Access the application at http://127.0.0.1:5000/.

## Usage Instructions

### Student
- Register and log in.
- Fill out and submit an application.
- View application status.

### Admin
- Log in as an admin.
- View submitted applications.
- Approve or reject applications.
- Manage user accounts.

## Technology Stack
- Flask (Python Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Flask-WTF (Forms Handling)
- Flask-Login (Authentication)
- Flask-Migrate (Database Migrations)
- PDFkit using wkhtmltopdf (PDF Generation)

## Assumptions
- Admins are manually added to the database using create_admin.py
- Applications follow a predefined format.
- Users can submit only one application at a time.
- wkhtmltopdf.exe is installed in the system in the default location such as C:\Program Files\wkhtmltopdf\bin\

## Screenshots
Below are some screenshots of the application:

![Screen 1](screenshots/screen%20(1).png)
![Screen 2](screenshots/screen%20(2).png)
![Screen 3](screenshots/screen%20(3).png)
![Screen 4](screenshots/screen%20(4).png)
![Screen 5](screenshots/screen%20(5).png)
![Screen 6](screenshots/screen%20(6).png)
![Screen 7](screenshots/screen%20(7).png)
![Screen 8](screenshots/screen%20(8).png)
![Screen 9](screenshots/screen%20(9).png)
![Screen 10](screenshots/screen%20(10).png)
![Screen 11](screenshots/screen%20(11).png)
![Screen 12](screenshots/screen%20(12).png)
![Screen 13](screenshots/screen%20(13).png)
![Screen 14](screenshots/screen%20(14).png)
![Screen 15](screenshots/screen%20(15).png)