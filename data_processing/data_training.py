import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def process_data(companyName):
    # Read and load data from csv to variable
    data = pd.read_csv(f'./data_processing/{companyName}.csv')

    # Drop empty values
    data = data.dropna()  
   # Update volume values with actual numbers
    data['Vol.'] = data['Vol.'].str.replace('M', '000000')
    data['Vol.'] = data['Vol.'].str.replace('B', '000000000')
    data['Vol.'] = data['Vol.'].astype(float)

    #Convert date to seconds
    data['Date'] = pd.to_datetime(data['Date'])  # convert date to datetime
    data['Date'] = data['Date'].apply(lambda x: x.value // 10 ** 9)  # convert datetime to seconds to represent it as numerical value

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data[['Date', 'Open', 'High', 'Low', 'Vol.']], data['Price'], test_size=0.2, random_state=42)

    # Train the model on training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Test after training
    y_pred = model.predict(X_test)

    # Evaluate Results
    mse = mean_squared_error(y_test, y_pred)
    
    print('Mean squared error:', mse)

    return model, y_train, y_pred
   