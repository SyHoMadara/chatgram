# Chatgram

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Security](#security)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Messages](#messages)
  - [Users](#users)
- [Contributing](#contributing)
- [License](#license)

## Description

Chatgram is a live chat application that enables users to communicate securely in real-time. Utilizing the RSA algorithm for secure login tokens, it also plans to implement message encryption for enhanced privacy.

## Features

### Current Features
- **Real-time messaging** between users.
- **Secure login** with RSA algorithm tokens.

### Upcoming Features
- Sending **files and pictures** as messages.
- **Editing and deleting** messages.
- Viewing **all messages and unread messages** from other parties.

## Technology Stack

- **Python**
- **Django**
- **Django REST Framework**
- **RSA** for encryption

## Security

Chatgram uses the **RSA algorithm** to generate secure login tokens. Future updates will include **encryption for messages** to ensure that all communications are private and secure.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SyHoMadara/chatgram.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd chatgram
   ````
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Make migrations:
    ```bash
    python manage.py makemigrations
    ```
5. Make migrate:
    ```bash
    python manage.py migrate
    ```
6. Create superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Run the server:
    ```bash
    python manage.py runserver
    ```
## Usage

After installation, visit `http://localhost:8000` to start using the application. Login with your credentials, and you
can begin sending messages to other users.

## API Documentation

This section provides a detailed overview of the API endpoints available in the live chat application, including methods, request parameters, and example responses. The application uses JSON for request and response bodies.

You can access web base documentation by visiting `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`.

### Authentication

- **Login**
  - **Endpoint**: `/api/token/`
  - **Method**: POST
  - **Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
  - **Response**:
    ```json
    {
      "access": "ACCESS_TOKEN",
      "refresh": "REFRESH_TOKEN"
    }
    ```

- **Refresh Token**
  - **Endpoint**: `/api/token/refresh/`
  - **Method**: POST
  - **Body**:
    ```json
    {
      "refresh": "REFRESH_TOKEN"
    }
    ```
  - **Response**:
    ```json
    {
      "access": "NEW_ACCESS_TOKEN"
    }
    ```

### Messages

- **Send Message**
  - **Endpoint**: `/api/messages/send/`
  - **Method**: POST
  - **Authorization**: Bearer ACCESS_TOKEN
  - **Body**:
    ```json
    {
      "receiver": "user2@example.com",
      "message": "Hello, World!"
    }
    ```
  - **Response**:
    ```json
    {
      "id": 1,
      "sender": "user1@example.com",
      "receiver": "user2@example.com",
      "message": "Hello, World!",
      "timestamp": "2023-01-01T12:00:00Z"
    }
    ```

- **Reply to Message**
  - **Endpoint**: `/api/messages/reply/`
  - **Method**: POST
  - **Authorization**: Bearer ACCESS_TOKEN
  - **Body**:
    ```json
    {
      "message": "Reply message",
      "reply_to": 1
    }
    ```
  - **Response**:
    ```json
    {
      "id": 2,
      "sender": "user2@example.com",
      "receiver": "user1@example.com",
      "message": "Reply message",
      "reply_to": 1,
      "timestamp": "2023-01-01T12:05:00Z"
    }
    ```

### Users

- **Register User**
  - **Endpoint**: `/api/users/register/`
  - **Method**: POST
  - **Body**:
    ```json
    {
      "email": "newuser@example.com",
      "password": "password123",
      "first_name": "New",
      "last_name": "User"
    }
    ```
  - **Response**:
    ```json
    {
      "email": "newuser@example.com",
      "first_name": "New",
      "last_name": "User"
    }
    ```

This documentation should be updated as new endpoints are added or existing ones are modified.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.