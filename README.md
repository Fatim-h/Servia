# Servia
A centralized online platform that showcases and organizes NGOs and foundations in a city. Verified admins an NGOs can add, update or delete details, while visitors can browse a searchable, filterable gallery or explore NGOs.
---

## Features

- **User Roles:**
  - **Admin:** Manage users, causes, and content.
  - **NGO\Event:** Add and manage cause details, events, locations, donations, and volunteers.
  - **Visitor:** Browse causes, view NGO information, and explore events.
  
- **Authentication:** Secure login and password hashing with `Flask-Login` and `Werkzeug`.

- **Causes:** Detailed cause information with social links, contact info, feedback, donations, and volunteer opportunities.

- **NGOs:** NGOs can create events associated with causes and specify locations.

- **Events:** Can be linked to NGOs and specify locations.

- **Locations:** Linked to NGOs and Events and   stored the map needed info.

- **Feedback & Donations & Volunteer:** Visitors can provide feedback, volunteer and donate to causes.

- **Responsive Frontend:** React app with CSS styling for a clean, modern interface.

- **API Backend:** Flask + Flask-CORS + SQLAlchemy + JWT for a RESTful backend.

---
## Tech Stack

- **Frontend:** React, CSS  
- **Backend:** Flask, Flask-CORS, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-Login  
- **Database:** PostgreSQL (or SQLite for local testing)  
- **Environment Variables:** `python-dotenv`  

---
## How to Run (Frontend Only)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Fatim-h/Servia
   
2. open venv:
   ```bash
   cd frontend
   
3. Install requirements:
   ```bash
   pip install -r requirements.txt

4. Configure environment variables:
   ```bash
   FLASK_APP=server.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/servia
   JWT_SECRET_KEY=your_secret_key

5. Initialize database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade

6. Run the backend server:
   ```bash
   flask run

### Frontend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Fatim-h/Servia
   
2. Change to frontend directory:
   ```bash
   cd frontend
   
3. Install dependencies:
   ```bash
   npm install

4. Start build:
   ```bash
   npm start

## Project Directory Structure
   ```
   Servia/
├─server.py
├─ backend/
│ ├─ init.py
│ ├─ config.py
│ ├─ models.py
│ ├─ routes.py
│ └─ requirements.txt
└─ frontend/
| ├─ package.json
| ├─ package-lock.json
| ├─src/
| | ├─ pages/
│ | |  ├─HomePage.js
│ | |  ├─CausePage.js
│ | |  ├─UserPage.js
│ | |  ├─LoginPage.js
│ | |  ├─SignPage.js
│ | |  ├─AdminDashboard.js
| | |  └─ ...css
├─ components/
│ └─ Header.js
├─ services/
│ └─ api.js
│ └─ authServices.js
├─ App.js
├─ index.js
└─ server.py

```
## Contributors:
- Fatimah
- Safia
- Meghna
