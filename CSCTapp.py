import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
from pyproj import Transformer

st.set_page_config(page_title="Flood Risk App", layout="centered")
st.title("🌊 Flood Risk Prediction App")

# Model Selection
model_files = {
    "RF (All Features)": "model.pkl",
    "RF (T10 Features)": "model_rf_top10.pkl",
}
selected_model_name = st.selectbox("Select Model to Use", list(model_files.keys()))
model_path = model_files[selected_model_name]
model = joblib.load(model_path)
st.success(f"✅ Loaded: {selected_model_name}")

# Initialize session state
if "prediction_made" not in st.session_state:
    st.session_state["prediction_made"] = False

if "pred_label" not in st.session_state:
    st.session_state["pred_label"] = None

if "easting" not in st.session_state:
    st.session_state["easting"] = 0

if "northing" not in st.session_state:
    st.session_state["northing"] = 0

if "confidence" not in st.session_state:
    st.session_state["confidence"] = 1.0

if "certainty_quite" not in st.session_state:
    st.session_state["certainty_quite"] = False

if "certainty_uncertain" not in st.session_state:
    st.session_state["certainty_uncertain"] = False
st.subheader("Enter Key Features")

st.session_state["confidence"] = st.number_input("Confidence", min_value=0.0, max_value=10.0, value=st.session_state["confidence"], step=0.1)
st.session_state["easting"] = st.number_input("Easting", value=st.session_state["easting"])
st.session_state["northing"] = st.number_input("Northing", value=st.session_state["northing"])
st.session_state["certainty_quite"] = st.checkbox("Certainty: Quite Certain", value=st.session_state["certainty_quite"])
st.session_state["certainty_uncertain"] = st.checkbox("Certainty: Uncertain", value=st.session_state["certainty_uncertain"])

if st.button("Predict FRL"):
    # Build the input array
    input_array = np.zeros(len(model.feature_names_in_))
    feature_names = model.feature_names_in_

    for i, name in enumerate(feature_names):
        if name == 'Confidence':
            input_array[i] = st.session_state["confidence"]
        elif name == 'Easting':
            input_array[i] = st.session_state["easting"]
        elif name == 'Northing':
            input_array[i] = st.session_state["northing"]
        elif name == 'Certainty_Quite Certain':
            input_array[i] = int(st.session_state["certainty_quite"])
        elif name == 'Certainty_Uncertain':
            input_array[i] = int(st.session_state["certainty_uncertain"])

    prediction = model.predict([input_array])
    st.session_state["pred_label"] = prediction[0]
    st.session_state["prediction_made"] = True

# Risk label map
label_map = {
    0: ("Low Risk", "green"),
    1: ("Medium Risk", "orange"),
    2: ("High Risk", "red")
}

if st.session_state["prediction_made"]:
    pred_label = st.session_state["pred_label"]
    risk_text, color = label_map.get(pred_label, ("Unknown", "gray"))

    st.markdown(
        f"<div style='padding:10px; border-radius:10px; background-color:{color}; color:white; font-size:20px; text-align:center;'>"
        f"{risk_text}</div>",
        unsafe_allow_html=True
    )

    # Convert to Lat/Lon
    transformer = Transformer.from_crs("epsg:27700", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(st.session_state["easting"], st.session_state["northing"])

    # Build map
    m = folium.Map(location=[lat, lon], zoom_start=13)

    # Add current marker
    folium.Marker([lat, lon], popup=f"Current: {risk_text}", tooltip="Predicted Location").add_to(m)

    st.subheader("📍 Location on Map")
    st_folium(m, width=700, height=450)

    # Save prediction
    new_record = {
        "Model": selected_model_name,
        "Confidence": st.session_state["confidence"],
        "Easting": st.session_state["easting"],
        "Northing": st.session_state["northing"],
        "Certainty_Quite Certain": int(st.session_state["certainty_quite"]),
        "Certainty_Uncertain": int(st.session_state["certainty_uncertain"]),
        "Predicted Risk Level": pred_label
    }

    df_new = pd.DataFrame([new_record])
    csv_file = "predictions.csv"

    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_file, index=False)
    else:
        df_new.to_csv(csv_file, index=False)
       # EWS Trigger (Simple Alert for High Risk)
    if pred_label == 2:
        st.markdown(
            """
            <div style='padding:15px; border-radius:10px; background-color:#ff4d4d; color:white; font-size:18px; text-align:center;'>
                🚨 <strong>Early Warning:</strong> High flood risk detected! Alert your local emergency management team.
            </div>
            """,
            unsafe_allow_html=True
        )
    
        # Email Notification
        admin_email = "admin@example.com" 
        email_subject = "🚨 Flood Risk Alert - High Risk Detected"
        email_body = f"""
        ALERT: High flood risk has been predicted.
    
        Details:
        - Risk Level: High (2)
        - Confidence: {st.session_state["confidence"]}
        - Easting: {st.session_state["easting"]}
        - Northing: {st.session_state["northing"]}
        - Certainty: Quite Certain={st.session_state["certainty_quite"]}, Uncertain={st.session_state["certainty_uncertain"]}
        - Model Used: {selected_model_name}
    
        Immediate action is advised for the predicted location.
        """
    
        with st.expander("📧 Email Notification"):
            st.write(f"**To:** {admin_email}")
            st.write(f"**Subject:** {email_subject}")
            st.code(email_body.strip(), language="text")
    
    # Download button
    with open(csv_file, "rb") as f:
        st.download_button(
            label="📥 Download Predictions CSV",
            data=f,
            file_name="predictions.csv",
            mime="text/csv"
        )
