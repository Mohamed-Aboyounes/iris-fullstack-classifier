# Iris Classifier UI

Streamlit app for the Iris classifier. It shows a form for the four measurements in centimetres, sends them to the API's `POST /predict` endpoint as `{"feature_array": [...]}`, and displays the predicted species.

The API address comes from the `API_URL` environment variable. Its default is `http://api:8000`, the API's service name inside Docker Compose, and `compose.yaml` sets the same value explicitly.

## Run with Docker Compose

From the project root:

```bash
docker compose up --build
```

Then open <http://localhost:8501>.

## Run locally without Docker

Start the API first (see `api/README.md`), then from this directory:

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
API_URL=http://localhost:8000 streamlit run app.py
```

On Windows PowerShell set the variable with `$env:API_URL = "http://localhost:8000"` before running `streamlit run app.py`.
