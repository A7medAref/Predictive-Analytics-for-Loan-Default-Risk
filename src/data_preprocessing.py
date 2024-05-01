import pandas as pd

def get_cleaned_data(convert_categorical=False, print_description=False):
    # Load data
    data = pd.read_csv('../data/application_data.csv')

    # drop id column
    data = data.drop('SK_ID_CURR', axis=1)

    # Get columns that have missing values with percentage > 5%
    missing_data = data.isnull().mean() * 100
    missing_data = missing_data[missing_data > 5]

    # Drop columns with missing values percentage > 5%
    cleaned_data = data.drop(missing_data.index, axis=1)

    # Fill the missing values
    numerical_columns = cleaned_data.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = cleaned_data.select_dtypes(include=['object']).columns

    # Fill the missing values with the mean for numerical columns
    for column in numerical_columns:
        cleaned_data[column] = cleaned_data[column].fillna(cleaned_data[column].mean())

    # Fill the missing values with the mode for categorical columns
    for column in categorical_columns:
        cleaned_data[column] = cleaned_data[column].fillna(cleaned_data[column].mode()[0])

    # Convert categorical columns to numerical columns
    if convert_categorical:
        cleaned_data = pd.get_dummies(cleaned_data, columns=categorical_columns)
    
    # Remove coloumns that contain document information
    cleaned_data = cleaned_data.drop(columns=["FLAG_DOCUMENT_2", "FLAG_DOCUMENT_4", "FLAG_DOCUMENT_5", "FLAG_DOCUMENT_6", "FLAG_DOCUMENT_7", "FLAG_DOCUMENT_8", "FLAG_DOCUMENT_9", "FLAG_DOCUMENT_10", "FLAG_DOCUMENT_11", "FLAG_DOCUMENT_12", "FLAG_DOCUMENT_13", "FLAG_DOCUMENT_14", "FLAG_DOCUMENT_15", "FLAG_DOCUMENT_16", "FLAG_DOCUMENT_17", "FLAG_DOCUMENT_18", "FLAG_DOCUMENT_19", "FLAG_DOCUMENT_20", "FLAG_DOCUMENT_21"])
    
    # Print the description of the columns
    if print_description:
        # Get Description of columns
        cols = pd.read_csv("../data/columns_description.csv")
        cols = cols[["Row", "Description"]]
        # print remaining columns with their datatype and description

        print(len(data.columns))
        for col in data.columns:
            print(f"Column '{col}' with datatype '{data[col].dtype}' and description : '{cols.loc[cols['Row'] == col].values[0][1]}'")

    return cleaned_data
