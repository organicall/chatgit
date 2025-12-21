# ChatGit React Version

This is a React rewriten version of the ChatGit frontend, powered by a FastAPI backend.

## Prerequisites

- Node.js (v18+)
- Python 3.10+
- `venv` created and requirements installed.

## Setup

1. **Install Python Dependencies**:
   Ensure you are in the root `ChatGit 2 rework` directory.
   ```bash
   source venv/bin/activate
   pip install -r requirements_react.txt
   ```

2. **Install Frontend Dependencies**:
   ```bash
   cd chatgit-react/frontend
   npm install
   ```

## Running

You can use the helper script:

```bash
cd chatgit-react
chmod +x start.sh
./start.sh
```

Or run them manually:

**Backend:**
```bash
# In root directory
source venv/bin/activate
uvicorn api:app --reload --port 8000
```

**Frontend:**
```bash
# In chatgit-react/frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) (or the port shown by Vite) to view the app.
