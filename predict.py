import pandas as pd
from dython.nominal import correlation_ratio, associations
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer, LabelEncoder, OrdinalEncoder
import pickle as pkl

# forest = pkl.load(open('model.sav', 'rb'))
# encoders_dict = pkl.load(open('encoders.sav', 'rb'))
# possStatusD_encoder = encoders_dict['possStatusD_encoder']
# transactionType_encoder = encoders_dict['transactionType_encoder']
# propType_encoder = encoders_dict['propType_encoder']
# isRera_encoder = encoders_dict['isRera_encoder']
# locality_encoder = encoders_dict['locality_encoder']
# ownership_encoder = encoders_dict['ownership_encoder']
# mlb_flooringType = encoders_dict['mlb_flooringType']
# mlb_adrooms = encoders_dict['mlb_adrooms']
#
# test_df = pd.read_excel('test.xlsx')
# user_input_df = test_df.iloc[0]
#
# test_df.iloc[0] = ['Ready to Move', 'NA', 1, 25000000, "Mosaic", "Study", 11656, 'NA', 1000, 19.247437, 72.847117,
#                    'Borivali', 'N', 'Co-operative Society', 'Furnished', 2, 2, 1, 'Resale', 'Apartment',
#                    2, 4, 'Water Availability 24 Hours Available', 8, 3]
#
#
# # Replacing building age with numbers (Hard coded method)
# test_df['buildingAge'].replace(11652, 2, inplace=True)
# test_df['buildingAge'].replace(11653, 3, inplace=True)
# test_df['buildingAge'].replace(11654, 4, inplace=True)
# test_df['buildingAge'].replace(11655, 5, inplace=True)
# test_df['buildingAge'].replace(11656, 6, inplace=True)
# test_df['buildingAge'].replace(11651, 1, inplace=True)
# test_df['buildingAge'].replace(10080, 0, inplace=True)
#
# # Encode labels in columns (using label encoder)
# test_df['possStatusD'] = possStatusD_encoder.transform(test_df['possStatusD'])
#
# test_df['transactionType'] = transactionType_encoder.transform(test_df['transactionType'])
#
# test_df['propType'] = propType_encoder.transform(test_df['propType'])
#
# test_df['isRera'] = isRera_encoder.transform(test_df['isRera'])
#
# test_df['locality'] = locality_encoder.transform(test_df['locality'])
#
# # Fit and transform the 'OwnershipTypeD' column
# encoded_ownership = ownership_encoder.transform(test_df[['OwnershipTypeD']])
#
# # Convert the result to a DataFrame and add column names
# encoded_test_df = pd.DataFrame(encoded_ownership.toarray(), columns=ownership_encoder.get_feature_names_out(['OwnershipTypeD']))
#
# # Concatenate the encoded DataFrame with the original DataFrame
# test_df = pd.concat([test_df, encoded_test_df], axis=1)
#
# # Drop the original 'OwnershipTypeD' column if needed
# test_df = test_df.drop('OwnershipTypeD', axis=1)
#
# label_mapping_furnished = {"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2}
# test_df = test_df.replace({"isFurnished": label_mapping_furnished})
#
# label_mapping_waterStatus = {"Water Availability 24 Hours Available": 5, "Water Availability 12 Hours Available": 4, "Water Availability 6 Hours Available": 2, "Water Availability 2 Hours Available": 1, "Water Availability 1 Hour Available": 0, "NA": 3}
# test_df = test_df.replace({"waterStatus": label_mapping_waterStatus})
#
#
# # mlb = MultiLabelBinarizer()
#
# test_df['flooringType'] = test_df['flooringType'].str.split(',')
#
# dfa = pd.DataFrame(mlb_flooringType.transform(test_df['flooringType']),columns=mlb_flooringType.classes_, index=test_df.index)
# print(dfa)
#
# test_df = pd.concat([test_df, dfa], axis=1)
#
# test_df['adrooms'] = test_df['adrooms'].str.split(',')
#
# dfa = pd.DataFrame(mlb_adrooms.transform(test_df['adrooms']),columns=mlb_adrooms.classes_, index=test_df.index)
# print(dfa)
#
# test_df = pd.concat([test_df, dfa], axis=1)
#
# # test_df['landmarkDetails'] = test_df['landmarkDetails'].apply(lambda x: len(x.split(',')))
#
# # test_df['amenities'] = test_df['amenities'].astype(str).apply(lambda x: len(x.split(' ')))
#
# test_df['price'] = np.log(test_df['price'] + 1)
# test_df['bedroom'] = np.log(test_df['bedroom'] + 1)
# test_df['bathrooms'] = np.log(test_df['bathrooms'] + 1)
# test_df['balconies'] = np.log(test_df['balconies'] + 1)
# test_df['coverArea'] = np.log(test_df['coverArea'] + 1)
# test_df['floorNo'] = np.log(test_df['floorNo'] + 3)
# test_df['floors'] = np.log(test_df['floors'] + 3)
#
# test_df.dropna(subset=['isFurnished'], inplace=True)
# test_df.drop(['acD', 'None of these', 'Unknown', 'flooringType', 'adrooms', 'url', 'OwnershipTypeD_Unknown'], inplace=True, axis=1, errors="ignore")
# # test_df.info()
#
# X_test_ms, y_test_ms = test_df.drop(['price'], axis=1), test_df['price']
# # forest.predict(X_test_ms)
# price = forest.predict(X_test_ms)
# print(price)