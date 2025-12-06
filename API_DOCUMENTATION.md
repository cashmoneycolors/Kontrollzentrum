# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Modules
```
GET /modules - List all modules
GET /modules/{name} - Get module details
POST /modules/{name}/run - Execute module
```

### Health
```
GET /health - System health status
GET /health/modules - Module health status
```

### Logs
```
GET /logs - Get system logs
GET /logs/{module} - Get module logs
```

### AI Assistant
```
POST /ai/chat - Chat with AI
GET /ai/model - Get model info
POST /ai/feedback - Submit feedback
```

### Authentication
```
POST /auth/login - Login
POST /auth/token - Get JWT token
```

## Response Format
```json
{
  "status": "success",
  "data": {},
  "timestamp": "2025-01-15T10:00:00Z"
}
```

## Error Handling
```json
{
  "status": "error",
  "message": "Error description",
  "code": 400
}
```
