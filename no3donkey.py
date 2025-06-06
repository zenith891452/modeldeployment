# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1stZriG8guhuMQIfPZlFVXaqPv2214SOA
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Upload model dan encoder
model_file = st.file_uploader("Upload Model", type=["pkl"])
encoder_file = st.file_uploader("Upload Label Encoder", type=["pkl"])

if model_file is not None and encoder_file is not None:
    try:
        # Membaca file model dan encoder menggunakan joblib
        model = pickle.load(model_file)
        label_encoders = pickle.load(encoder_file)

        st.success("✅ Model dan encoder berhasil dimuat!")
    except Exception as e:
        st.error(f"❌ Gagal memuat model atau encoder. Error: {str(e)}")
        st.stop()
else:
    st.write("Harap upload file model dan label encoder.")

# Fungsi prediksi status booking
def predict_booking_status(no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights,
                            type_of_meal_plan, required_car_parking_space, room_type_reserved, lead_time,
                            arrival_year, arrival_month, arrival_date, market_segment_type, repeated_guest,
                            no_of_previous_cancellations, no_of_previous_bookings_not_canceled,
                            avg_price_per_room, no_of_special_requests):

    input_data = pd.DataFrame({
        'no_of_adults': [no_of_adults],
        'no_of_children': [no_of_children],
        'no_of_weekend_nights': [no_of_weekend_nights],
        'no_of_week_nights': [no_of_week_nights],
        'required_car_parking_space': [required_car_parking_space],
        'lead_time': [lead_time],
        'arrival_year': [arrival_year],
        'arrival_month': [arrival_month],
        'arrival_date': [arrival_date],
        'repeated_guest': [repeated_guest],
        'no_of_previous_cancellations': [no_of_previous_cancellations],
        'no_of_previous_bookings_not_canceled': [no_of_previous_bookings_not_canceled],
        'avg_price_per_room': [avg_price_per_room],
        'no_of_special_requests': [no_of_special_requests]
    })

    # Pastikan hasil encoding memiliki dimensi yang benar (ubah menjadi array 1D)
    meal_encoded = label_encoders['type_of_meal_plan'].transform([[type_of_meal_plan]]).flatten()
    room_encoded = label_encoders['room_type_reserved'].transform([[room_type_reserved]]).flatten()
    market_encoded = label_encoders['market_segment_type'].transform([[market_segment_type]]).flatten()

    # Gabungkan input data dengan hasil encoding
    full_input = np.hstack([input_data.values.flatten(), meal_encoded, room_encoded, market_encoded])
    prediction = model.predict(full_input.reshape(1, -1))  # Reshape untuk memastikan input sesuai
    output = "Not Canceled" if prediction == 0 else "Canceled"
    return output

# Input form untuk data prediksi
st.subheader("Input Data untuk Prediksi")
with st.form("booking_form"):
    no_of_adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=2)
    no_of_children = st.number_input("Number of Children", min_value=0, max_value=10, value=1)
    no_of_weekend_nights = st.number_input('Weekend Nights', min_value=0, max_value=10, value=2)
    no_of_week_nights = st.number_input('Week Nights', min_value=0, max_value=10, value=3)
    type_of_meal_plan = st.selectbox('Meal Plan', ['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected'])
    required_car_parking_space = st.radio('Required Car Parking Space', [0, 1])
    room_type_reserved = st.selectbox('Room Type Reserved', ['Room_Type 1', 'Room_Type 2', 'Room_Type 3',
                                                            'Room_Type 4', 'Room_Type 5', 'Room_Type 6', 'Room_Type 7'])
    lead_time = st.number_input("Lead Time (days)", min_value=0, max_value=500, value=224)
    arrival_year = st.selectbox("Arrival Year", [2017, 2018])
    arrival_month = st.selectbox('Arrival Month', list(range(1,13)))
    arrival_date = st.selectbox("Arrival Date", list(range(1, 32)))
    market_segment_type = st.selectbox('Market Segment', ['Offline', 'Online', 'Corporate', 'Complementary', 'Aviation'])
    repeated_guest = st.radio('Repeated Guest?', [0, 1])
    no_of_previous_cancellations = st.number_input('Previous Cancellations', min_value=0, max_value=20, value=0)
    no_of_previous_bookings_not_canceled = st.number_input('Previous Bookings Not Canceled', min_value=0, max_value=20, value=0)
    avg_price_per_room = st.number_input('Average Price per Room', min_value=0.0, max_value=1000.0, value=65.0)
    no_of_special_requests = st.number_input('Number of Special Requests', min_value=0, max_value=5, value=0)

    submitted = st.form_submit_button("Predict")

# Proses prediksi jika form disubmit
if submitted:
    result = predict_booking_status(
        no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights,
        type_of_meal_plan, required_car_parking_space, room_type_reserved,
        lead_time, arrival_year, arrival_month, arrival_date, market_segment_type,
        repeated_guest, no_of_previous_cancellations, no_of_previous_bookings_not_canceled,
        avg_price_per_room, no_of_special_requests
    )
    st.write(f"Prediction Result: {result}")

# **Test Case 1**
st.subheader("Test Case 1")
st.markdown("""
<b>Input:</b><br>
- Adults: 2<br>
- Children: 0<br>
- Weekend Nights: 1<br>
- Week Nights: 2<br>
- Meal Plan: Meal Plan 1<br>
- Parking: Yes<br>
- Room Type: Room_Type 1<br>
- Lead Time: 10<br>
- Arrival: 2018-5-15<br>
- Market Segment: Offline<br>
- Repeated Guest: Yes<br>
- Prev Cancel: 0<br>
- Prev Not Cancel: 3<br>
- Price: 75.0<br>
- Special Requests: 2<br>
""", unsafe_allow_html=True)

if st.button("Run Test Case 1"):
    result = predict_booking_status(
        no_of_adults=2,
        no_of_children=0,
        no_of_weekend_nights=1,
        no_of_week_nights=2,
        type_of_meal_plan='Meal Plan 1',
        required_car_parking_space=1,
        room_type_reserved='Room_Type 1',
        lead_time=10,
        arrival_year=2018,
        arrival_month=5,
        arrival_date=15,
        market_segment_type='Offline',
        repeated_guest=1,
        no_of_previous_cancellations=0,
        no_of_previous_bookings_not_canceled=3,
        avg_price_per_room=75.0,
        no_of_special_requests=2
    )
    st.write(f"Test Case 1 Result: {result}")

# **Test Case 2**
st.subheader("Test Case 2")
st.markdown("""
<b>Input:</b><br>
- Adults: 1<br>
- Children: 2<br>
- Weekend Nights: 2<br>
- Week Nights: 3<br>
- Meal Plan: Not Selected<br>
- Parking: No<br>
- Room Type: Room_Type 6<br>
- Lead Time: 200<br>
- Arrival: 2017-12-31<br>
- Market Segment: Online<br>
- Repeated Guest: No<br>
- Prev Cancel: 3<br>
- Prev Not Cancel: 0<br>
- Price: 300.0<br>
- Special Requests: 0<br>
""", unsafe_allow_html=True)

if st.button("Run Test Case 2"):
    result = predict_booking_status(
        no_of_adults=1,
        no_of_children=2,
        no_of_weekend_nights=2,
        no_of_week_nights=3,
        type_of_meal_plan='Not Selected',
        required_car_parking_space=0,
        room_type_reserved='Room_Type 6',
        lead_time=200,
        arrival_year=2017,
        arrival_month=12,
        arrival_date=31,
        market_segment_type='Online',
        repeated_guest=0,
        no_of_previous_cancellations=3,
        no_of_previous_bookings_not_canceled=0,
        avg_price_per_room=300.0,
        no_of_special_requests=0
    )
    st.write(f"Test Case 2 Result: {result}")