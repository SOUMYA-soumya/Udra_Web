🏗 System Architecture
The application enforces a strict "Middleware-First" security model. Every user action is gated by RBAC module checks and logged via automated audit trails.

(Note: Upload the attached architecture image to the root of your repository so it displays here.)

Architecture Zones
Administrative Workflows: Security Admins provision users with mandatory KYC data (Govt ID type/number). Users remain inactive until explicit CRUD permissions are mapped to specific modules.

Access Control & Session Management: Every login attempt (success or failure) is permanently recorded in a dedicated login_audit table, capturing IP addresses and timestamps before a secure session is established.

Permission-Gated Transaction Flow: Transactions (e.g., updating a Challan) pass through an RBAC middleware layer. Upon successful execution, the database ORM automatically stamps created_by/updated_by columns without requiring manual developer intervention.

✨ Key Features
Module-Driven RBAC: Permissions are granted on a per-module basis (Challan Entry, Transporter Directory, Financial Redemption, User Admin) with granular Create, Read, Update, and Delete (CRUD) toggles.

Mandatory Table Auditing: Every database table inherits from a universal BaseModel that enforces created_by, created_date, updated_by, and update_date tracking.

Strict Authentication: Accounts require an explicit "Active" status to log in. Deactivated accounts immediately lose API access.

Cross-Platform Readiness: The frontend is built in Flutter, ensuring the UI components can compile seamlessly to Web, Desktop, or Mobile as the ecosystem expands.

🛠 Tech Stack
Backend (RESTful API):

Python 3.x

Flask (API Framework)

Flask-SQLAlchemy (ORM & Database Management)

SQLite (Development) / PostgreSQL (Production ready)

Frontend (Web Client):

Flutter (Dart)

Material Design 3

HTTP package (for API integration)

📂 Repository Structure
Plaintext
udra-challan-platform/
│
├── backend/                  # Flask API & Database Architecture
│   ├── app.py                # Application factory & initialization
│   ├── auth.py               # Authentication API blueprint
│   ├── models.py             # SQLAlchemy models & mandatory audit schema
│   ├── seed.py               # Database seeder (Super Admin generation)
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # Flutter Web Application
│   ├── lib/
│   │   ├── main.dart         # Flutter entry point & Login UI
│   │   └── dashboard.dart    # Web Dashboard & Navigation Rail
│   ├── pubspec.yaml          # Flutter dependencies
│   └── web/                  # Web-specific compilation files
│
└── README.md                 # Project documentation
