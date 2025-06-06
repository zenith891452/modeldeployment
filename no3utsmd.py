# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1stZriG8guhuMQIfPZlFVXaqPv2214SOA
"""

import pandas as pd
import pickle

class HotelModelInference:
    def __init__(self, model_path, encoder_path):
        """Inisialisasi dan muat model serta encoder dari file pickle"""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        with open(encoder_path, 'rb') as f:
            self.label_encoders = pickle.load(f)

    def preprocess_input(self, input_dict):
        """Melakukan preprocessing input (label encoding)"""
        # Konversi dictionary input ke DataFrame
        df_input = pd.DataFrame([input_dict])

        # Label encoding kolom kategorikal
        for col, le in self.label_encoders.items():
            if col in df_input.columns:
                df_input[col] = le.transform(df_input[col])

        return df_input

    def predict(self, input_dict):
        """Melakukan prediksi berdasarkan input"""
        processed_input = self.preprocess_input(input_dict)
        prediction = self.model.predict(processed_input)[0]
        probability = self.model.predict_proba(processed_input)[0]
        return prediction, probability

# Pemanggilan untuk inferensi
if __name__ == "__main__":
    # Inisialisasi class
    infer = HotelModelInference(model_path='/content/best_model_oop.pkl', encoder_path='/content/label_encoders.pkl')

    # Contoh input (isi sesuai kolom dataset)
    input_data = {
        'Booking_ID': 'INN00001',
        'no_of_adults': 2,
        'no_of_children': 0,
        'no_of_weekend_nights': 1,
        'no_of_week_nights': 2,
        'type_of_meal_plan': 'Meal Plan 1',
        'required_car_parking_space': 0,
        'room_type_reserved': 'Room_Type 1',
        'lead_time': 224,
        'arrival_year': 2017,
        'arrival_month': 10,
        'arrival_date': 2,
        'market_segment_type': 'Offline',
        'repeated_guest': 0,
        'no_of_previous_cancellations': 0,
        'no_of_previous_bookings_not_canceled': 0,
        'avg_price_per_room': 65.0,
        'no_of_special_requests': 0
    }

    # Lakukan prediksi
    result, prob = infer.predict(input_data)

    # Tampilkan hasil prediksi dan probabilitas
    print(f"Prediksi booking_status: {'Not Canceled' if result == 0 else 'Canceled'}")
    print(f"Probabilitas Not Canceled: {prob[0]:.2f} %")
    print(f"Probabilitas Canceled: {prob[1]:.2f} %")