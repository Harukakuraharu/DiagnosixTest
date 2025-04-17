#!/bin/bash

# Registation
curl -X POST "http://localhost:80/user/registration/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com", "password": "qwerty123", "role": "patient"}'

# Auth
curl -X POST "http://localhost:80/user/auth/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "qwerty123"}'

# Successful auth
curl -X POST "http://localhost:8000/user/auth/" \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "password": "string123"}'

# Incorrect password
curl -X POST "http://localhost:8000/user/auth/" \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "password": "wrongpassword"}'  

# Successful request
curl -X GET "http://localhost:8000/user/me/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Not successful request
curl -X GET "http://localhost:8000/user/me/"

# Request with invalid token
curl -X GET "http://localhost:8000/user/me/" \
-H "Authorization: Bearer invalid_token"