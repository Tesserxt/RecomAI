recomai/
│
├── frontend/                 # React + Vite
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── movies.py
│   │   │       ├── recommendations.py
│   │   │       ├── auth.py
│   │   │       └── favorites.py
│   │   │
│   │   ├── schemas/          # Pydantic request/response shapes
│   │   │   ├── movie.py
│   │   │   ├── user.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── models/           # Database models
│   │   │   ├── user.py
│   │   │   ├── movie.py
│   │   │   └── favorite.py
│   │   │
│   │   ├── services/         # Actual business logic
│   │   │   ├── tmdb.py
│   │   │   └── recommender.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── session.py
│   │   │
│   │   └── core/
│   │       ├── config.py
│   │       └── security.py
│   │
│   ├── tests/
│   │
│   ├── .env
│   ├── .env.example
│   ├── pyproject.toml
│   └── README.md
│
├── .gitignore
└── README.md