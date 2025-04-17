# Task Management System

## Overview

A comprehensive task management system built with Django REST Framework that enables users to efficiently create, manage, and track tasks and projects. The system features robust user authentication, task organization, project management, and collaboration capabilities.

## Features

- **User Authentication**

  - Secure signup and login using JWT (JSON Web Tokens)
  - Email-based user accounts
  - Protected API endpoints

- **Task Management**

  - Create, read, update, and delete tasks
  - Task attributes: title, description, status, priority, due date
  - Filter tasks by status, priority, and due date
  - Task assignment capabilities

- **Project Management**

  - Create and manage projects
  - Associate multiple tasks with projects
  - Project ownership and collaboration

- **Collaboration**
  - Assign tasks to team members
  - Share projects across users
  - Track task ownership and updates

## Technology Stack

- **Backend**: Django & Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Version Control**: Git
- **Development Environment**: Linux/Windows

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd task-management-system
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL:

- Create a PostgreSQL database
- Update database settings in `config/settings.py`

5. Apply migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:

```bash
python manage.py runserver
```

2. Access the application:

- API: http://localhost:8000/api/
- Admin interface: http://localhost:8000/admin/

## Testing

The project includes comprehensive test coverage for all major components:

```bash
python manage.py test
```

Test suites include:

- User authentication tests
- Task management API tests
- Project management API tests
- Frontend integration tests

## API Endpoints

### Authentication

- POST `/api/users/` - Create new user
- POST `/api/token/` - Obtain JWT token

### Tasks

- GET `/api/tasks/` - List tasks
- POST `/api/tasks/` - Create task
- GET `/api/tasks/{id}/` - Retrieve task
- PUT `/api/tasks/{id}/` - Update task
- DELETE `/api/tasks/{id}/` - Delete task

### Projects

- GET `/api/projects/` - List projects
- POST `/api/projects/` - Create project
- GET `/api/projects/{id}/` - Retrieve project
- PUT `/api/projects/{id}/` - Update project
- DELETE `/api/projects/{id}/` - Delete project

## Deployment

1. Configure production settings:

- Update `config/settings.py` with production settings
- Configure environment variables
- Set `DEBUG=False`

2. Collect static files:

```bash
python manage.py collectstatic
```

3. Set up a production database

4. Configure web server (e.g., Nginx)

5. Set up WSGI server (e.g., Gunicorn)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
