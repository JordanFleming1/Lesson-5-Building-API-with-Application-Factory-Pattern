# Library Management API

A simple Flask REST API for managing library resources, including members, books, loans, mechanics, and service tickets.

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your database in `app/config.py`.
4. Run the app:
   ```
   python app.py
   ```

## Endpoints
- `/members` - Manage library members
- `/books` - Manage books
- `/loans` - Manage loans
- `/mechanics` - Manage mechanics
- `/service-tickets` - Manage service tickets

## Testing
Use Postman to test all endpoints. Export your Postman collection for submission.
