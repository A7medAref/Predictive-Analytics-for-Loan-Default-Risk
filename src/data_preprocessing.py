import pandas as pd
from sklearn.preprocessing import LabelEncoder

# def get_cleaned_data(convert_categorical=False, print_description=False):
# 	# Load data
# 	data = pd.read_csv('../data/application_data.csv')

# 	# drop id column
# 	data = data.drop('SK_ID_CURR', axis=1)

# 	# Get columns that have missing values with percentage > 5%
# 	missing_data = data.isnull().mean() * 100
# 	missing_data = missing_data[missing_data > 5]

# 	# Drop columns with missing values percentage > 5%
# 	cleaned_data = data.drop(missing_data.index, axis=1)

# 	# Fill the missing values
# 	numerical_columns = cleaned_data.select_dtypes(include=['int64', 'float64']).columns
# 	categorical_columns = cleaned_data.select_dtypes(include=['object']).columns

# 	# Fill the missing values with the mean for numerical columns
# 	for column in numerical_columns:
# 		cleaned_data[column] = cleaned_data[column].fillna(cleaned_data[column].mean())

# 	# Fill the missing values with the mode for categorical columns
# 	for column in categorical_columns:
# 		cleaned_data[column] = cleaned_data[column].fillna(cleaned_data[column].mode()[0])

# 	# Convert categorical columns to numerical columns
# 	if convert_categorical:
# 		# cleaned_data = pd.get_dummies(cleaned_data, columns=categorical_columns)
# 		le = LabelEncoder()
# 		for col in categorical_columns:
# 			cleaned_data[col] = le.fit_transform(cleaned_data[col])
# 	# Remove coloumns that contain document information
# 	cleaned_data = cleaned_data.drop(columns=["FLAG_DOCUMENT_2", "FLAG_DOCUMENT_3", "FLAG_DOCUMENT_4", "FLAG_DOCUMENT_5", "FLAG_DOCUMENT_6", "FLAG_DOCUMENT_7", "FLAG_DOCUMENT_8", "FLAG_DOCUMENT_9", "FLAG_DOCUMENT_10", "FLAG_DOCUMENT_11", "FLAG_DOCUMENT_12", "FLAG_DOCUMENT_13", "FLAG_DOCUMENT_14", "FLAG_DOCUMENT_15", "FLAG_DOCUMENT_16", "FLAG_DOCUMENT_17", "FLAG_DOCUMENT_18", "FLAG_DOCUMENT_19", "FLAG_DOCUMENT_20", "FLAG_DOCUMENT_21"])

# 	# Print the description of the columns
# 	if print_description:
# 		# Get Description of columns
# 		cols = pd.read_csv("../data/columns_description.csv")
# 		cols = cols[["Row", "Description"]]
# 		# print remaining columns with their datatype and description

# 		print(len(data.columns))
# 		for col in data.columns:
# 			print(f"Column '{col}' with datatype '{data[col].dtype}' and description : '{cols.loc[cols['Row'] == col].values[0][1]}'")

# 	# Remove outliers
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_INCOME_TOTAL'] > 0.6e6].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_ANNUITY'] > 0.125e6].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_CREDIT'] > 2.0e6].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['DAYS_REGISTRATION'] < -15e3].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['DEF_60_CNT_SOCIAL_CIRCLE'] > 15].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['OBS_60_CNT_SOCIAL_CIRCLE'] > 100].index)
# 	cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['CNT_FAM_MEMBERS'] > 10].index)

# 	return cleaned_data

def get_cleaned_data_final(convert_categorical=False, drop_correlated=True, drop_outliers=True, print_description=False):
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
		# cleaned_data = pd.get_dummies(cleaned_data, columns=categorical_columns)
		le = LabelEncoder()
		for col in categorical_columns:
			cleaned_data[col] = le.fit_transform(cleaned_data[col])
	# Remove coloumns that contain document information
	cleaned_data = cleaned_data.drop(columns=["FLAG_DOCUMENT_2", "FLAG_DOCUMENT_3", "FLAG_DOCUMENT_4", "FLAG_DOCUMENT_5", "FLAG_DOCUMENT_6", "FLAG_DOCUMENT_7", "FLAG_DOCUMENT_8", "FLAG_DOCUMENT_9", "FLAG_DOCUMENT_10", "FLAG_DOCUMENT_11", "FLAG_DOCUMENT_12", "FLAG_DOCUMENT_13", "FLAG_DOCUMENT_14", "FLAG_DOCUMENT_15", "FLAG_DOCUMENT_16", "FLAG_DOCUMENT_17", "FLAG_DOCUMENT_18", "FLAG_DOCUMENT_19", "FLAG_DOCUMENT_20", "FLAG_DOCUMENT_21"])

	# Print the description of the columns
	if print_description:
		# Get Description of columns
		cols = pd.read_csv("../data/columns_description.csv")
		cols = cols[["Row", "Description"]]
		# print remaining columns with their datatype and description

		print(len(data.columns))
		for col in data.columns:
			print(f"Column '{col}' with datatype '{data[col].dtype}' and description : '{cols.loc[cols['Row'] == col].values[0][1]}'")

	if drop_correlated:
		high_corr_cols = [
			'REGION_RATING_CLIENT', 
			'AMT_GOODS_PRICE', 
			'OBS_30_CNT_SOCIAL_CIRCLE', 
			'DEF_30_CNT_SOCIAL_CIRCLE',
			'REG_CITY_NOT_WORK_CITY',
			'CNT_CHILDREN',
			'FLAG_MOBIL',
			'REG_REGION_NOT_LIVE_REGION',
			'REG_REGION_NOT_WORK_REGION'
			]

		cleaned_data = cleaned_data.drop(columns=high_corr_cols)

	# Remove outliers
	if drop_outliers:
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_INCOME_TOTAL'] > 0.6e6].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_ANNUITY'] > 0.125e6].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['AMT_CREDIT'] > 2.0e6].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['DAYS_REGISTRATION'] < -15e3].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['DEF_60_CNT_SOCIAL_CIRCLE'] > 15].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['OBS_60_CNT_SOCIAL_CIRCLE'] > 100].index)
		cleaned_data = cleaned_data.drop(cleaned_data[cleaned_data['CNT_FAM_MEMBERS'] > 10].index)

	return cleaned_data

def convert_numberical_to_categorical(data, print_counts=False):

	cols = [
			'TARGET', 
			'REGION_RATING_CLIENT_W_CITY', 
			'FLAG_WORK_PHONE', 
			'FLAG_MOBIL', 
			'FLAG_EMP_PHONE',
			'FLAG_CONT_MOBILE',
			'FLAG_PHONE',
			'REG_REGION_NOT_LIVE_REGION',
			'REG_CITY_NOT_LIVE_CITY',
			'LIVE_REGION_NOT_WORK_REGION',
			'FLAG_EMAIL',
			'LIVE_CITY_NOT_WORK_CITY'
		]

	for col in data.columns:
		if col in cols or data[col].dtype == 'object':
			if col in data.columns:
				data[col] = data[col].map({x: col + "_" + str(x) for x in data[col].unique()})

	col = 'DAYS_LAST_PHONE_CHANGE'
	bins = [-4000, -1500, 0]
	labels = [
			'DAYS_LAST_PHONE_CHANGE_-4000_-1500',
			'DAYS_LAST_PHONE_CHANGE_-1500_0']


	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)

	col = 'HOUR_APPR_PROCESS_START'
	bins = [0, 6, 18, 24]
	labels = [
			'HOUR_APPR_PROCESS_START_0_6',
			'HOUR_APPR_PROCESS_START_6_18',
			'HOUR_APPR_PROCESS_START_18_24']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'EXT_SOURCE_1'
	bins = [0, 0.4, 1]
	labels = [
			'EXT_SOURCE_1_0_0.',
			'EXT_SOURCE_1_0.4_1']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'EXT_SOURCE_2'
	bins = [0, 0.4, 1]
	labels = [
			'EXT_SOURCE_2_0_0.',
			'EXT_SOURCE_2_0.4_1']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'EXT_SOURCE_3'
	bins = [0, 0.4, 1]
	labels = [
			'EXT_SOURCE_3_0_0.',
			'EXT_SOURCE_3_0.4_1']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'AMT_INCOME_TOTAL'
	bins = [0, 200_000, 400_000, 1_000_000]
	labels = [
			'AMT_INCOME_TOTAL_0_200000',
			'AMT_INCOME_TOTAL_200000_400000',
			'AMT_INCOME_TOTAL_400000_1000000']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)		
	col = 'AMT_CREDIT'
	bins = [0, 600_000, 1_000_000, 2_000_000]
	labels = [
			'AMT_CREDIT_0_600000',
			'AMT_CREDIT_600000_1000000',
			'AMT_CREDIT_1000000_2000000']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)	
	col = 'AMT_ANNUITY'
	bins = [0, 30_000, 50_000, 200_000]
	labels = [
			'AMT_ANNUITY_0_30000',
			'AMT_ANNUITY_30000_50000',
			'AMT_ANNUITY_50000_200000']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'CNT_FAM_MEMBERS'
	bins = [0, 3, 5, 10]
	labels = [
			'CNT_FAM_MEMBERS_0_3',
			'CNT_FAM_MEMBERS_3_5',
			'CNT_FAM_MEMBERS_5_10']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'REGION_POPULATION_RELATIVE'
	bins = [0, 0.02, 0.04, 0.08]
	labels = [
			'REGION_POPULATION_RELATIVE_0_0.02',
			'REGION_POPULATION_RELATIVE_0.02_0.04',
			'REGION_POPULATION_RELATIVE_0.04_0.08']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'DAYS_BIRTH'
	bins = [-30_000, -20_000, -12_500, 0]
	labels = [
			'DAYS_BIRTH_-30000_-20000',
			'DAYS_BIRTH_-20000_-12500',
			'DAYS_BIRTH_-12500_0']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'DAYS_EMPLOYED'
	bins = [-20_000, -5_000, 0, 1_000_000]
	labels = [
			'DAYS_EMPLOYED_-20000_-5000',
			'DAYS_EMPLOYED_-5000_0',
			'DAYS_EMPLOYED_0_1000000']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'DAYS_REGISTRATION'
	bins = [-15_000, -8_000, -2_000, 0]
	labels = [
			'DAYS_REGISTRATION_-15000_-8000',
			'DAYS_REGISTRATION_-8000_-2000',
			'DAYS_REGISTRATION_-2000_0']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	col = 'DAYS_ID_PUBLISH'
	bins = [-7_000, -5_000, -2_000, 0]
	labels = [
			'DAYS_ID_PUBLISH_-7000_-5000',
			'DAYS_ID_PUBLISH_-5000_-2000',
			'DAYS_ID_PUBLISH_-2000_0']
	if col in data.columns:
		data[col] = pd.cut(data[col], bins=bins, labels=labels, right=False)
		if print_counts:
			print(col)
			print(data[col].value_counts() / len(data) * 100)
	return data