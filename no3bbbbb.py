# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1stZriG8guhuMQIfPZlFVXaqPv2214SOA
"""

import streamlit as st
import pandas as pd
import joblib

st.title("🧠 Hotel Booking Cancellation Prediction")

# Load model dan encoder
try:
    best_model = joblib.load('/content/best_model_oop.pkl')
    label_encoder = joblib.load('/content/label_encoders.pkl')
    st.success("✅ Model dan encoder berhasil dimuat!")
except:
    st.error("❌ Gagal memuat model atau encoder. Pastikan file tersedia.")
    st.stop()

# Urutan fitur untuk model
feature_order = [
    'no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights', 'lead_time',
    'arrival_year', 'arrival_month', 'arrival_date', 'repeated_guest', 'no_of_previous_cancellations',
    'no_of_previous_bookings_not_canceled', 'avg_price_per_room', 'no_of_special_requests',
    'type_of_meal_plan_Meal Plan 1', 'type_of_meal_plan_Meal Plan 2', 'type_of_meal_plan_Meal Plan 3',
    'type_of_meal_plan_Not Selected',
    'room_type_reserved_Room_Type 1', 'room_type_reserved_Room_Type 2', 'room_type_reserved_Room_Type 3',
    'room_type_reserved_Room_Type 4', 'room_type_reserved_Room_Type 5', 'room_type_reserved_Room_Type 6',
    'room_type_reserved_Room_Type 7',
    'market_segment_type_Aviation', 'market_segment_type_Complementary', 'market_segment_type_Corporate',
    'market_segment_type_Offline', 'market_segment_type_Online'
]

# Fungsi untuk prediksi
def prediksi_booking(data_dict):
    df_input = pd.DataFrame([data_dict])
    df_input = df_input[feature_order]
    prediction = best_model.predict(df_input)[0]
    probability = best_model.predict_proba(df_input)[:, 1][0]

    st.subheader("🎯 Hasil Prediksi:")
    st.success(f"Prediksi: {prediction} (0 = Tidak Dibatalkan, 1 = Dibatalkan)")
    st.info(f"🔢 Probabilitas Pembatalan: {probability:.2%}")

# =======================
# Input manual dari user
# =======================
st.subheader("✍️ Input Data Manual")

with st.form("input_form"):
    input_data = {
        'no_of_adults': st.number_input("Jumlah Dewasa", min_value=1, value=2),
        'no_of_children': st.number_input("Jumlah Anak", min_value=0, value=0),
        'no_of_weekend_nights': st.number_input("Weekend Nights", min_value=0, value=1),
        'no_of_week_nights': st.number_input("Week Nights", min_value=0, value=2),
        'lead_time': st.number_input("Lead Time", min_value=0, value=30),
        'arrival_year': st.selectbox("Tahun Kedatangan", [2017, 2018]),
        'arrival_month': st.slider("Bulan Kedatangan", 1, 12, 5),
        'arrival_date': st.slider("Tanggal Kedatangan", 1, 31, 15),
        'repeated_guest': st.selectbox("Tamu Berulang", [0, 1]),
        'no_of_previous_cancellations': st.number_input("Cancel Sebelumnya", min_value=0, value=0),
        'no_of_previous_bookings_not_canceled': st.number_input("Booking Aman Sebelumnya", min_value=0, value=0),
        'avg_price_per_room': st.number_input("Harga Rata-rata per Kamar", min_value=0.0, value=100.0),
        'no_of_special_requests': st.number_input("Permintaan Khusus", min_value=0, value=0),
    }

    meal_plan = st.selectbox("Meal Plan", ['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected'])
    room_type = st.selectbox("Tipe Kamar", [f"Room_Type {i}" for i in range(1, 8)])
    market_segment = st.selectbox("Segment Pasar", ['Aviation', 'Complementary', 'Corporate', 'Offline', 'Online'])

    for plan in ['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected']:
        input_data[f'type_of_meal_plan_{plan}'] = 1 if plan == meal_plan else 0
    for rt in range(1, 8):
        input_data[f'room_type_reserved_Room_Type {rt}'] = 1 if f'Room_Type {rt}' == room_type else 0
    for seg in ['Aviation', 'Complementary', 'Corporate', 'Offline', 'Online']:
        input_data[f'market_segment_type_{seg}'] = 1 if seg == market_segment else 0

    submitted = st.form_submit_button("🔍 Prediksi")
    if submitted:
        prediksi_booking(input_data)

# ======================
# Test Case 1 dan 2
# ======================
st.subheader("🧪 Contoh Test Case")

if st.button("📦 Jalankan Testcase 1"):
    testcase1 = {
        'no_of_adults': 2, 'no_of_children': 0, 'no_of_weekend_nights': 1, 'no_of_week_nights': 2,
        'lead_time': 10, 'arrival_year': 2018, 'arrival_month': 5, 'arrival_date': 15,
        'repeated_guest': 1, 'no_of_previous_cancellations': 0, 'no_of_previous_bookings_not_canceled': 3,
        'avg_price_per_room': 75.0, 'no_of_special_requests': 2,
        'type_of_meal_plan_Meal Plan 1': 1, 'type_of_meal_plan_Meal Plan 2': 0,
        'type_of_meal_plan_Meal Plan 3': 0, 'type_of_meal_plan_Not Selected': 0,
        'room_type_reserved_Room_Type 1': 1, 'room_type_reserved_Room_Type 2': 0,
        'room_type_reserved_Room_Type 3': 0, 'room_type_reserved_Room_Type 4': 0,
        'room_type_reserved_Room_Type 5': 0, 'room_type_reserved_Room_Type 6': 0,
        'room_type_reserved_Room_Type 7': 0,
        'market_segment_type_Aviation': 0, 'market_segment_type_Complementary': 0,
        'market_segment_type_Corporate': 0, 'market_segment_type_Offline': 1,
        'market_segment_type_Online': 0
    }
    prediksi_booking(testcase1)

if st.button("📦 Jalankan Testcase 2"):
    testcase2 = {
        'no_of_adults': 1, 'no_of_children': 2, 'no_of_weekend_nights': 2, 'no_of_week_nights': 3,
        'lead_time': 200, 'arrival_year': 2017, 'arrival_month': 12, 'arrival_date': 31,
        'repeated_guest': 0, 'no_of_previous_cancellations': 3, 'no_of_previous_bookings_not_canceled': 0,
        'avg_price_per_room': 300.0, 'no_of_special_requests': 0,
        'type_of_meal_plan_Meal Plan 1': 0, 'type_of_meal_plan_Meal Plan 2': 0,
        'type_of_meal_plan_Meal Plan 3': 0, 'type_of_meal_plan_Not Selected': 1,
        'room_type_reserved_Room_Type 1': 0, 'room_type_reserved_Room_Type 2': 0,
        'room_type_reserved_Room_Type 3': 0, 'room_type_reserved_Room_Type 4': 0,
        'room_type_reserved_Room_Type 5': 0, 'room_type_reserved_Room_Type 6': 1,
        'room_type_reserved_Room_Type 7': 0,
        'market_segment_type_Aviation': 0, 'market_segment_type_Complementary': 0,
        'market_segment_type_Corporate': 0, 'market_segment_type_Offline': 0,
        'market_segment_type_Online': 1
    }
    prediksi_booking(testcase2)