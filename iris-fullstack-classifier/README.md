# Iris Full-Stack Classifier

- **Description:** Extend the FastAPI Iris classifier with a web UI and PostgreSQL inference logging, all runnable with Docker Compose.
- **Inputs:** Sepal length, sepal width, petal length, and petal width in centimetres.
- **Classes:** Setosa, versicolor, and virginica.

## Assignment

- Create a `ui/` directory with a Streamlit app for entering the four measurements.
- Send the measurements from the UI to the API's `POST /predict` endpoint and display the predicted species.
- Add a `ui/Dockerfile` to build and run the Streamlit app.
- Add a root-level `compose.yaml` with services for the API, UI, and PostgreSQL.
- Use the lightweight official PostgreSQL image `postgres:16-alpine` and configure a persistent data volume.
- Create `api/.env` with a `DATABASE_URL` for the Compose PostgreSQL service, for example:
  `DATABASE_URL=postgresql://postgres:postgres@db:5432/iris`
- Keep the database name, user, and password consistent between `api/.env` and the Compose PostgreSQL settings.
- Configure the UI to call the API at `http://api:8000` from inside Compose; use the Compose service name, not `localhost`.
- Start the full stack from the project root with `docker compose up --build`.
- Verify the UI prediction, API docs at `http://localhost:8000/docs`, and inference records in PostgreSQL.

## Project structure

```text
.
|-- compose.yaml        db, api and ui services
|-- api/
|   |-- .env            DATABASE_URL for the Compose database
|   |-- Dockerfile
|   |-- main.py         FastAPI app, logs every prediction to PostgreSQL
|   |-- model/iris_model.pkl
|   `-- requirements.txt
|-- ui/
|   |-- Dockerfile
|   |-- app.py          Streamlit form that calls POST /predict
|   `-- requirements.txt
`-- notebooks/Iris_model.ipynb
```

## Run the stack

From the project root:

```bash
docker compose up --build
```

Compose starts PostgreSQL first, waits for it to pass its health check, then starts the API, and starts the UI once the API is healthy.

| Service | URL |
|---|---|
| Streamlit UI | <http://localhost:8501> |
| API docs | <http://localhost:8000/docs> |

The database port is not published to the host. The API reaches it as `db:5432` and the UI reaches the API as `http://api:8000`, both by Compose service name.

## Verify

1. Open <http://localhost:8501>, enter the four measurements and press **Predict**. These rows from the Iris dataset give one result per class:

   | Sepal length | Sepal width | Petal length | Petal width | Prediction |
   |---:|---:|---:|---:|---|
   | 5.1 | 3.5 | 1.4 | 0.2 | setosa |
   | 7.0 | 3.2 | 4.7 | 1.4 | versicolor |
   | 6.7 | 3.0 | 5.2 | 2.3 | virginica |

2. Open <http://localhost:8000/docs> and run `POST /predict` with:

   ```json
   {"feature_array": [5.1, 3.5, 1.4, 0.2]}
   ```

3. Check the inference records in PostgreSQL:

   ```bash
   docker compose exec db psql -U postgres -d iris -c "SELECT id, features, prediction, created_at FROM inferences ORDER BY id DESC LIMIT 10;"
   ```

   Each prediction from the UI or the docs page adds one row.

## Stop

```bash
docker compose down      # stops the containers, keeps the pgdata volume
docker compose down -v   # also deletes the pgdata volume and all records
```

Records survive `docker compose down` and a later `docker compose up` because PostgreSQL stores its data in the named volume `pgdata`.

## Notes

- `api/.env` is committed because the assignment requires it. It only holds the local Compose credentials (`postgres` / `postgres`, database `iris`), which match the `db` service in `compose.yaml`. The file is excluded from the API image by `api/.dockerignore` and passed to the container through `env_file`.
- `scikit-learn` is pinned to 1.7.2 in `api/requirements.txt`, the version that saved `model/iris_model.pkl`. With the old 1.5.2 pin the API printed an `InconsistentVersionWarning` at startup. Predictions on the full Iris dataset are identical under both versions.
- `python-dotenv` is now listed in `api/requirements.txt` because `main.py` imports it. It was only installed before as a side effect of `uvicorn[standard]`.
- The API response keeps its original `class_id ` key (with a trailing space). The UI reads `class_name` for the species and accepts either spelling for the id.
