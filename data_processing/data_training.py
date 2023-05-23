import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from analyzer.data_processing.visualize import visualize, create_histogram
from datetime import date, datetime, timedelta

import requests
from flask import Flask, jsonify

import matplotlib.pyplot as plt

from analyzer.config import API_KEY


def process_data(companyName):
    # Read and load data from csv to variable
    data = pd.read_csv(f'../data_processing/{companyName}.csv')

    #Create visual Representation
    visualize(data, companyName)

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
    
    # Display test vs predicted value graph
    create_histogram(X_test, y_test, y_pred)
    
    return model, y_train, y_pred
   

#Get stock data for today
def getStockToday(company):

    #Filter company
    if company == "apple":
        company = "aapl"
    elif company == "amazon":
        company = "amzn"
    elif company == "google":
         company = "goog"

    #Assign endpoint
    data_Access_Url =  f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company}&apikey={API_KEY}'
    #Make Request and convert to json
    response = requests.get(data_Access_Url)
    json_response = response.json()

    #Get today stock data
    daily_Data = json_response['Time Series (Daily)']
    today_Data =  list(daily_Data.keys())[0]
    # Access the data for the first date
    today = daily_Data[today_Data]
    return today

#Predict stock prices for next 14 days for selected company
def predict_stock_values(company, data, model):
    price_list = {}

    # Prepare first input Data
    open_price = data['1. open']
    high = data["2. high"]
    low = data[ "3. low"]
    volume = data["6. volume"]
    close_price = data['4. close']
    # Convert current date to float
    date = datetime.now() + timedelta(days=1)
    date =  date.timestamp()

    #Get the current date
    featured_data = pd.DataFrame({
        'Date': [date],
        'Open': open_price,
        'High': high,
        'Low': low,
        'Vol.':float(volume) / 10 ** 3
    })

    counter = 0

    #Get prices for next 14 days
    while counter < 14:
        #Predict
        futurePrediction = model.predict(featured_data[['Date', 'Open', 'High', 'Low', 'Vol.']])
        # Add price and date (converted from timestamp) to list
        price_list[(datetime.fromtimestamp(date + counter * 86400)).strftime('%d-%m-%Y')] = futurePrediction

        #Update data
        counter += 1
        # add day
        next_date = date + counter * 86400
        # update featured_data
        featured_data.at[0, 'Date'] = next_date
        featured_data.at[0, 'Open'] = futurePrediction

    return price_list
    

# Create a graph
def create_graph(data):
    
    dates = []
    prices = []
    # Add key and value to lists
    for keys, values in data.items():
        dates.append(keys)
        prices.append(values)

    # Create the graph

    plt.figure(figsize=(8, 8))
    plt.plot(dates, prices, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices')
    plt.xticks(rotation=45)

    # Save the graph to a file
    graph_filename = 'static/graph.png'
    plt.savefig(graph_filename)

    return graph_filename




   



