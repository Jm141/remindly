# Task Manager API

A Flask-based REST API for task management built with SOLID principles and clean architecture.

## 🚀 Live Demo

**API URL**: https://remindly.onrender.com

## 📋 Features

- User authentication with JWT tokens
- Task management (CRUD operations)
- Subtask support
- Due date notifications
- SOLID architecture principles
- Clean code structure

## 🏗️ Architecture

```
├── config.py (Configuration)
├── models/ (Data Models)
├── repositories/ (Data Access)
├── services/ (Business Logic)
├── controllers/ (Request Handling)
└── dependency_injection.py (DI Container)
```

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `POST /api/refresh` - Refresh JWT token

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Subtasks
- `GET /api/tasks/<id>/subtasks` - Get subtasks
- `POST /api/tasks/<id>/subtasks` - Create subtask
- `PUT /api/tasks/<id>/subtasks/<subtask_id>` - Update subtask
- `DELETE /api/tasks/<id>/subtasks/<subtask_id>` - Delete subtask

### Notifications
- `GET /api/notifications/due` - Get due notifications

## 🛠️ Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## 🌐 Deployment

This API is deployed on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Database

Currently using SQLite. For production, consider PostgreSQL.

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS enabled
- Environment variable configuration

## 🧪 Testing

Run tests with: `python test_api.py`

## 📝 License

MIT License 