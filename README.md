# RecomAI
my-project/
├── frontend/
├── backend/
├── data-science/
├── infra/
├── docs/
└── README.md



my-project/
│
├── frontend/                    # React.js
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   └── ...
│
├── backend/                     # Python backend
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   │
│   │   ├── api/                 # HTTP/SSE endpoints
│   │   │   ├── routes/
│   │   │   └── deps.py
│   │   │
│   │   ├── agents/              # LangGraph / LangChain
│   │   │   ├── supervisors/
│   │   │   ├── specialists/
│   │   │   ├── graphs/
│   │   │   └── state.py
│   │   │
│   │   ├── tools/               # Tools agents can call
│   │   │   ├── fhir/
│   │   │   ├── coding/
│   │   │   └── search/
│   │   │
│   │   ├── services/            # Business logic
│   │   │   ├── patient_service.py
│   │   │   ├── coding_service.py
│   │   │   └── ...
│   │   │
│   │   ├── models/              # DB/domain models
│   │   ├── schemas/              # Pydantic request/response models
│   │   ├── memory/               # Working/episodic/etc.
│   │   ├── engines/              # ML / calculations
│   │   ├── core/                 # config, auth, logging
│   │   └── db/                   # DB connection/repositories
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
│
├── data-science/                # Experiments only
│   ├── notebooks/
│   ├── experiments/
│   ├── training/
│   └── scripts/
│
├── data/                         # DON'T commit real/private data
│   ├── raw/
│   ├── processed/
│   └── artifacts/
│
├── infra/                        # Deployment/infrastructure
│   ├── docker/
│   ├── nginx/
│   └── compose/
│
├── docs/
│   ├── architecture/
│   └── api/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── Makefile