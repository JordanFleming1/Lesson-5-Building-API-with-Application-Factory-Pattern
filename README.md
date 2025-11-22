# Library & Service Management API

A robust Flask REST API for managing library and service resources, including members, books, loans, mechanics, service tickets, inventory, and user authentication. Features advanced endpoints, modular blueprints, token authentication, rate limiting, and caching.

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

## Main Endpoints
- `/api/members` - Manage library members (CRUD, search, pagination)
- `/api/books` - Manage books (CRUD, search, pagination)
- `/api/loans` - Manage loans (CRUD)
- `/api/mechanics` - Manage mechanics (CRUD, most active mechanics)
- `/api/service_tickets` - Manage service tickets (CRUD, assign mechanics/inventory)
- `/api/inventory` - Manage inventory items (CRUD, assign to tickets)
- `/api/user/login` - User authentication (JWT)

## Features Added
- **User authentication** with JWT (login at `/api/user/login`)
- **Inventory management** and assignment to service tickets
- **Advanced endpoints**: search, sorting, pagination, bulk edit
- **Rate limiting** and **caching** for key endpoints
- **Modular blueprints** for all resources
- **Error handling** for invalid data and unauthorized access

## Testing with Postman
- Use `http://localhost:5000/api/...` for all endpoints
- For protected endpoints, add `Authorization: Bearer <token>` header
- Test CRUD for all resources, login, and advanced features (pagination, search, etc.)

## Example Postman Requests
- **Login:** `POST /api/user/login` (body: `{ "email": "...", "password": "..." }`)
- **Create Member:** `POST /api/members` (body: member JSON)
- **List Books:** `GET /api/books`
- **Create Service Ticket:** `POST /api/service_tickets` (body: ticket JSON)
- **Assign Inventory:** `PUT /api/service_tickets/<id>/add_inventory` (if implemented)

---

For more details, see the code and blueprints in the `app/` directory.

