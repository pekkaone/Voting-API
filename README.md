This project is a REST API for creating polls, voting, and viewing results. It includes JWT-based authentication and user management.

## 🚀 Technologies Used

- **Python 3.10+**
- **FastAPI**
- **SQLModel**
- **SQLite**
- **JWT (via `python-jose`)**
- **Uvicorn**

---

## 📁 Project Structure

Voting-API/
│
├── main.py # Entry point
├── db/
│ ├── database.py # Database engine and session management
│ └── models.py # SQLModel data models
│
├── Authentefication.py # Registration, login, token creation
├── Polls.py # Poll creation, voting, and result handling
---

## ⚙️ Setup Instructions
   
Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  
Install dependencies:
  pip install -r requirements.txt
  Run the app:
  uvicorn main:app --reload
  
🔐 Authentication:
  Uses JWT for user authentication.
  Protected endpoints require the token.
  Use the /authentefication endpoint to register.
  Use the /login endpoint to log in and receive a token.

📌 Available Endpoints:
  Method	Endpoint	Description
  POST	/authentefication	Register a new user
  POST	/login	Login and get JWT token
  POST	/poll/create-new-poll	Create a poll with a choice
  POST	/poll/add-new-choice/{id}	Add choice to a poll
  DELETE	/poll/delete-post/{id}	Delete a poll
  DELETE	/poll/delete-choice/{id}	Delete a choice
  GET	/poll/vote/{choice_id}	Vote for a choice
  GET	/poll/show-votes/{choice_id}	View number of votes
  GET	/poll/me	View your profile info

🧪 Testing:
  You can test the endpoints using:

  Swagger UI: http://localhost:8000/docs

  Postman, curl, or any HTTP client
