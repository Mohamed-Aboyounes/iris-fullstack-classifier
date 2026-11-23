import os

import requests
import streamlit as st

# Inside Docker Compose the API is reached by its service name, not localhost.
API_URL = os.getenv("API_URL", "http://api:8000").rstrip("/")

st.set_page_config(page_title="Iris Classifier")

st.title("Iris Classifier")
st.write("Enter the four flower measurements in centimetres, then press Predict.")

with st.form("measurements"):
    left, right = st.columns(2)
    with left:
        sepal_length = st.number_input(
            "Sepal length (cm)", min_value=0.0, max_value=10.0, value=5.1, step=0.1, format="%.1f"
        )
        sepal_width = st.number_input(
            "Sepal width (cm)", min_value=0.0, max_value=10.0, value=3.5, step=0.1, format="%.1f"
        )
    with right:
        petal_length = st.number_input(
            "Petal length (cm)", min_value=0.0, max_value=10.0, value=1.4, step=0.1, format="%.1f"
        )
        petal_width = st.number_input(
            "Petal width (cm)", min_value=0.0, max_value=10.0, value=0.2, step=0.1, format="%.1f"
        )
    submitted = st.form_submit_button("Predict")

if submitted:
    # Order matters: the model expects [sepal length, sepal width, petal length, petal width]
    features = [sepal_length, sepal_width, petal_length, petal_width]

    try:
        response = requests.post(
            f"{API_URL}/predict", json={"feature_array": features}, timeout=10
        )
        response.raise_for_status()
        prediction = response.json()["prediction"]
        species = prediction["class_name"]
        # The API currently sends the id under "class_id " (with a trailing space)
        class_id = prediction.get("class_id", prediction.get("class_id "))
    except requests.ConnectionError:
        st.error(f"Could not connect to the API at {API_URL}. Check that the api service is running.")
    except requests.Timeout:
        st.error("The API took too long to respond. Try again.")
    except requests.HTTPError:
        st.error(f"The API returned an error ({response.status_code}): {response.text}")
    except (ValueError, KeyError, TypeError):
        st.error("The API response was not in the expected format.")
    except requests.RequestException as exc:
        st.error(f"Request to the API failed: {exc}")
    else:
        st.success(f"Predicted species: Iris {species}")
        st.caption(f"Class id: {class_id}. Measurements sent: {features}")
