# RecomAI – AI-Powered Movie Recommendation System

RecomAI is an AI-powered movie recommendation application that helps users discover movies through natural-language queries and personalized recommendations.

## Features

- **AI Movie Search:** Search for movies using natural language.
- **Movie Recommendations:** Get recommendations using content-based filtering and TF-IDF.
- **AI Movie Insights:** Generate AI-powered summaries and insights about movies.
- **Real-time Interaction:** WebSocket-based communication for live AI responses.
- **Movie Discovery:** Browse popular movies and explore movie details.
- **Favorites:** Save your favorite movies.

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- LangGraph
- LangChain
- Scikit-learn
- NumPy
- Pandas

**AI & Data**
- Google Gemini
- TF-IDF
- TMDB API

**Deployment & Infrastructure**
- Vercel
- Cloudflare Quick Tunnel
- Uvicorn
- WebSockets

## Architecture

```text
                 User
                   |
                   v
             React + Vite
                   |
          +--------+--------+
          |                 |
          v                 v
       REST API          WebSocket
          |                 |
          +--------+--------+
                   |
                   v
             FastAPI Backend
                   |
          +--------+--------+
          |                 |
          v                 v
     LangGraph          TF-IDF Engine
     Workflows          Recommendations
          |
          v
       Gemini API

       TMDB API
          |
          v
     Movie Metadata
```

## Project Structure

```text
RecomAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── workflows/
│   │   ├── services/
│   │   └── main.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── setup.sh
├── start.sh
└── README.md
```

*Directory names may vary depending on the current project structure.*

## Prerequisites

Install the following:

- Git
- Node.js and npm
- Python
- [uv](https://docs.astral.sh/uv/)
- [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- jq
- [Vercel CLI](https://vercel.com/docs/cli)

### Arch Linux / EndeavourOS

```bash
sudo pacman -S --needed git nodejs npm python cloudflared jq
```

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Vercel CLI:

```bash
npm install -g vercel
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Tesserxt/RecomAI.git
cd RecomAI
```

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

The setup script installs backend and frontend project dependencies.

Alternatively, install dependencies manually:

**Backend**

```bash
cd backend
uv sync
```

**Frontend**

```bash
cd frontend
npm install
```

## Environment Variables

Configure the required environment variables before running the application.

**Backend**

Create `backend/.env` and configure:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TMDB_API_KEY=your_tmdb_api_key
```

Use the variable names expected by your backend configuration.

**Frontend**

The startup script updates `frontend/.env.production` with the Cloudflare WebSocket URL.

Do not commit API keys or other secrets to GitHub.

## Vercel Setup

Authenticate with Vercel:

```bash
vercel login
```

Link the frontend to your Vercel project:

```bash
cd frontend
vercel link
```

Select the existing `recom-ai` project when prompted.

Make sure the Vercel project is configured with the correct frontend root directory and build settings.

## Running the Application

From the repository root:

```bash
chmod +x start.sh
./start.sh
```

The script automatically:

1. Starts the FastAPI backend.
2. Creates a Cloudflare Quick Tunnel.
3. Updates the Vercel API rewrite configuration.
4. Updates the production WebSocket URL.
5. Commits and pushes configuration changes when required.
6. Waits for the corresponding Vercel deployment.
7. Promotes the deployment to Production.
8. Cleans up eligible older deployments.

Keep the terminal running while using the application.

Press `Ctrl+C` to stop the backend and Cloudflare Tunnel.

## Deployment

**Frontend:** Vercel

**Backend:** Runs locally and is exposed through Cloudflare Quick Tunnel.

The Quick Tunnel URL changes when the tunnel restarts. The startup script updates the frontend configuration and triggers a new Vercel deployment accordingly.

For a permanent deployment, consider hosting the backend on a VPS or cloud platform and using a named Cloudflare Tunnel.

## Links

- **Live Demo:** https://recom-ai-git-deployv1-tesserxt.vercel.app/
- **GitHub Repository:** https://github.com/Tesserxt/RecomAI

## License

This project is available for educational and personal use. Add a LICENSE file if you intend to distribute it under a specific open-source license.