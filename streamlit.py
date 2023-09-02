import math
import locale
import streamlit as st
import pickle as pkl
import pandas as pd
import numpy as np
import joblib
from dython.nominal import correlation_ratio, associations
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer, LabelEncoder, OrdinalEncoder

# forest = pkl.load(open('model.sav', 'rb'))
forest = joblib.load('model.joblib')
encoders_dict = pkl.load(open('encoders.sav', 'rb'))

# locales
locale.setlocale(locale.LC_ALL, 'en_IN')

def list_to_comma_separated_string(input_list):
    # Use the join method to concatenate list elements with commas
    comma_separated_string = ",".join(map(str, input_list))
    return comma_separated_string


def predict(poss, ufloor, floor_type, addn_rooms, age, area, latitude, longitude,
            local, rera, owner_type, furn_lvl, balc, bath, park, transaction, property_type, beds, tot_flr, water_avail,
            amen_cnt,
            price=100000):
    possStatusD_encoder = encoders_dict['possStatusD_encoder']
    transactionType_encoder = encoders_dict['transactionType_encoder']
    propType_encoder = encoders_dict['propType_encoder']
    isRera_encoder = encoders_dict['isRera_encoder']
    locality_encoder = encoders_dict['locality_encoder']
    ownership_encoder = encoders_dict['ownership_encoder']
    mlb_flooringType = encoders_dict['mlb_flooringType']
    mlb_adrooms = encoders_dict['mlb_adrooms']

    test_df = pd.read_excel('test.xlsx')
    test_df.drop(['landmarkDetails'], axis=1, inplace=True)

    # Replacing building age with numbers (Hard coded method)
    age = age.replace('Less than 5 years', "2")
    age = age.replace('5 to 10 years', "3")
    age = age.replace('10 to 15 years', "4")
    age = age.replace('15 to 20 years', "5")
    age = age.replace('Above 20 years', "6")
    age = age.replace('New Construction', "1")

    if rera:
        rera_opt = 'Y'
    else:
        rera_opt = 'N'

    age = int(age)

    test_df.iloc[0] = [poss, 'NA', ufloor, price, list_to_comma_separated_string(floor_type),
                       list_to_comma_separated_string(addn_rooms), age, 'NA', area, latitude, longitude,
                       str(local).strip(), rera_opt, owner_type, furn_lvl, balc, bath, park, transaction, property_type,
                       beds, tot_flr,
                       water_avail, amen_cnt]

    # Encode labels in columns (using label encoder)
    test_df['possStatusD'] = possStatusD_encoder.transform(test_df['possStatusD'])

    test_df['transactionType'] = transactionType_encoder.transform(test_df['transactionType'])

    test_df['propType'] = propType_encoder.transform(test_df['propType'])

    test_df['isRera'] = isRera_encoder.transform(test_df['isRera'])

    try:
        test_df['locality'] = locality_encoder.transform(test_df['locality'])
    except:
        test_df['locality'] = 0

    # Fit and transform the 'OwnershipTypeD' column
    encoded_ownership = ownership_encoder.transform(test_df[['OwnershipTypeD']])

    # Convert the result to a DataFrame and add column names
    encoded_test_df = pd.DataFrame(encoded_ownership.toarray(),
                                   columns=ownership_encoder.get_feature_names_out(['OwnershipTypeD']))

    # Concatenate the encoded DataFrame with the original DataFrame
    test_df = pd.concat([test_df, encoded_test_df], axis=1)

    # Drop the original 'OwnershipTypeD' column if needed
    test_df = test_df.drop('OwnershipTypeD', axis=1)

    label_mapping_furnished = {"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2}
    test_df = test_df.replace({"isFurnished": label_mapping_furnished})

    label_mapping_waterStatus = {"Water Availability 24 Hours Available": 5, "Water Availability 12 Hours Available": 4,
                                 "Water Availability 6 Hours Available": 2, "Water Availability 2 Hours Available": 1,
                                 "Water Availability 1 Hour Available": 0, "NA": 3}
    test_df = test_df.replace({"waterStatus": label_mapping_waterStatus})

    test_df['flooringType'] = test_df['flooringType'].str.split(',')

    dfa = pd.DataFrame(mlb_flooringType.transform(test_df['flooringType']), columns=mlb_flooringType.classes_,
                       index=test_df.index)
    print(dfa)

    test_df = pd.concat([test_df, dfa], axis=1)

    test_df['adrooms'] = test_df['adrooms'].str.split(',')

    dfa = pd.DataFrame(mlb_adrooms.transform(test_df['adrooms']), columns=mlb_adrooms.classes_, index=test_df.index)
    print(dfa)

    test_df = pd.concat([test_df, dfa], axis=1)

    test_df['price'] = np.log(test_df['price'] + 1)
    test_df['bedroom'] = np.log(test_df['bedroom'] + 1)
    test_df['bathrooms'] = np.log(test_df['bathrooms'] + 1)
    test_df['balconies'] = np.log(test_df['balconies'] + 1)
    test_df['coverArea'] = np.log(test_df['coverArea'] + 1)
    test_df['floorNo'] = np.log(test_df['floorNo'] + 3)
    test_df['floors'] = np.log(test_df['floors'] + 3)

    test_df.dropna(subset=['isFurnished'], inplace=True)
    test_df.drop(['acD', 'None of these', 'landmarkDetails', 'Unknown', 'flooringType', 'adrooms', 'url', 'OwnershipTypeD_Unknown'],
                 inplace=True, axis=1, errors="ignore")
    # test_df.info()

    X_test_ms, y_test_ms = test_df.drop(['price'], axis=1), test_df['price']

    price = forest.predict(X_test_ms)
    formatted_price = round(math.exp(float(price[0])))
    return formatted_price


predicted_price = 0

st.title("Mumbai House Price Predictor")

st.markdown('<style>div.row-widget.stRadio > div{padding: 10px;}</style>', unsafe_allow_html=True)

with st.form("my_form"):
    st.write("Fill out the details accordingly and click Submit to receive a predicted price")

    col1, col2 = st.columns(2)

    # Add inputs to the first column
    with col1:
        poss_stat = st.selectbox(
            'Possesion Status',
            ('Ready to Move', 'Under Construction'))

    # Add inputs to the second column
    with col2:
        build_age = st.selectbox(
            'Building Age',
            ('New Construction', 'Less than 5 years', '5 to 10 years', '10 to 15 years', '15 to 20 years',
             'Above 20 years'))

    col1, col2 = st.columns(2)

    # Add inputs to the first column
    with col1:
        floor = st.number_input('Your Floor', min_value=0)

    # Add inputs to the second column
    with col2:
        total_floors = st.number_input('Total Floors', min_value=0)

    cover_area = st.number_input('Cover Area (in Sq. Ft.)', min_value=100)

    col1, col2 = st.columns(2)

    # Add inputs to the first column
    with col1:
        lat = st.number_input('Latitude (Eg: 19.7238237)', min_value=19.00000000, step=0.00000005, format="%.8f")

    # Add inputs to the second column
    with col2:
        long = st.number_input('Longitude (Eg: 72.2424267)', min_value=72.0000000, step=0.00000005, format="%.8f")

    flooring_type = st.multiselect(
        'Flooring Type (Select all applicable)',
        ['Ceramic Tiles', 'Granite', 'Marble', 'Marbonite', 'Normal Tiles/Kotah Stone', 'Mosaic', 'Vitrified',
         'Wooden'])

    add_rooms = st.multiselect(
        'Additonal rooms (Select all applicable)',
        ['Puja Room', 'Study', 'Servant Room', 'Store'])
    # total_floors = st.number_input('Total Floors', min_value=0)

    col1, col2, col3 = st.columns(3)

    # Add inputs to the first column
    with col1:
        bedrooms = st.number_input('Bedrooms', min_value=0, max_value=12)

    # Add inputs to the second column
    with col2:
        bathrooms = st.number_input('Bathrooms', min_value=0, max_value=12)

    with col3:
        balconies = st.number_input('Balconies', min_value=0, max_value=12)

    col1, col2 = st.columns(2)

    # Add inputs to the first column
    with col1:
        parking = st.number_input('Parking Spaces', min_value=0, max_value=12)

    # Add inputs to the second column
    with col2:
        ameneties = st.number_input('Amenity Count', min_value=0, max_value=20)

    locality = st.text_input('Locality (Eg: Borivali, Kanjurmarg)')

    furnishing = st.select_slider(
        'Furnishing Level',
        options=['Unfurnished', 'Semi-Furnished', 'Furnished'])

    trans_type = st.selectbox(
        'Transaction Type',
        options=['Resale', 'New Property', 'Rent'])

    prop_type = st.selectbox(
        'Property Type',
        options=['Apartment', 'Studio Apartment', 'Penthouse', 'Villa',
                 'Residential House', 'Builder Floor Apartment'])

    water_stat = st.selectbox(
        'Water availability',
        options=['Water Availability 24 Hours Available',
                 'Water Availability 1 Hour Available',
                 'Water Availability 2 Hours Available',
                 'Water Availability 12 Hours Available',
                 'Water Availability 6 Hours Available'])

    own_type = st.selectbox(
        'Ownership Type',
        ('Freehold', 'Co-operative Society', 'Unknown', 'Leasehold', 'Power Of Attorney'))

    rera_val = st.checkbox("RERA registered property")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        predicted_price = predict(poss_stat, floor, flooring_type, add_rooms, build_age, cover_area, lat, long,
                        locality, rera_val, own_type, furnishing, balconies, bathrooms, parking, trans_type, prop_type,
                        bedrooms, total_floors, water_stat, ameneties,
                        price=100000)

if predicted_price > 0:
    formatted_price = locale.format_string("%d", predicted_price, grouping=True, monetary=True)
    st.write(f"Predicted price: Rs {formatted_price}")
