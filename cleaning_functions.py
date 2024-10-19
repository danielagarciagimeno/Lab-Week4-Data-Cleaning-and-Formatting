def standardize_column_names(df):
    df.columns = df.columns.str.replace('ST', 'state').str.lower().str.replace(' ', '_')
    return df

def clean_inconsistent_values(df):
    gender_mapping = {'F': 'F', 'M': 'M', 'Femal':'F', 'Male':'M', 'female':'F'}
    state_mapping = {'Washington': 'Washington', 'Arizona': 'Arizona', 'Nevada':'Nevada', 
                     'California':'California', 'Oregon':'Oregon', 'Cali': 'California', 
                     'AZ':'Arizona', 'WA':'Washington'}
    df['gender'] = df['gender'].map(gender_mapping)
    df['state'] = df['state'].map(state_mapping)
    df['education'] = df['education'].str.replace('Bachelors', 'Bachelor')
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '').astype(float)
    
    vehicle_class_mapping = {"Sports Car": "Luxury", "Luxury SUV": "Luxury", "Luxury Car": "Luxury"}
    df['vehicle_class'] = df['vehicle_class'].replace(vehicle_class_mapping)
    return df

def correct_data_types(df):
    # Correctamente convierte columnas numéricas a float antes de la manipulación, si es necesario
    df["customer_lifetime_value"] = df["customer_lifetime_value"].astype(float)
    
    # Mapeo y corrección de 'number_of_open_complaints'
    open_complaints_mapping = {"1/0/00":0, "1/2/00":2, "1/1/00": 1, '1/3/00':3,'1/5/00':5, '1/4/00':4}
    df['number_of_open_complaints'] = df['number_of_open_complaints'].map(open_complaints_mapping)
    
    # Manejo de valores faltantes con estadísticos
    numerical_vars = ['customer_lifetime_value', 'income', 'monthly_premium_auto', 'number_of_open_complaints', 'total_claim_amount']
    for column in numerical_vars:
        # Reemplaza `NaN` con la media de cada columna
        df[column] = df[column].fillna(df[column].mean()).astype(int)
    
    return df

def handle_missing_values(df):
    # Lista de columnas categóricas
    categorical_vars = ['customer', 'state', 'gender', 'education', 'policy_type', 'vehicle_class']
    
    for column in categorical_vars:
        # Reemplaza NaN con la moda (valor más frecuente) de cada columna categórica
        df[column] = df[column].fillna(df[column].mode()[0])
    
    return df

def remove_duplicates_and_reset_index(df):
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def clean_customer_data(df):
    df = standardize_column_names(df)
    df = clean_inconsistent_values(df)
    df = correct_data_types(df)
    df = handle_missing_values(df)
    df = remove_duplicates_and_reset_index(df)
    return df