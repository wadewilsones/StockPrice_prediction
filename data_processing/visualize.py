import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import date, datetime, timedelta

# Create visual representation 
def visualize(company_data, company_name):

    #For company stock prices for last 7 entries
    last_entries = company_data.tail(7)
    # Set up size of visualization
    plt.figure(figsize=(10, 6))
    # Get columns 
    x_axis = last_entries['Date']
    y_axis = last_entries['Price']

    #Create a scatter plot
    plt.scatter(x_axis, y_axis)

    # Set plot labels and title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{company_name} week stock prices')

    # Show the plot
    plt.grid(True)

    # Save the graph to a file
    graph_filename = './lastdata.png'
    plt.savefig(graph_filename)

    plt.show()


def create_histogram(test_data_dates, test_data_prices, predicted_prices):

    #Create lists to enter to histogram
    test = {}
    actual = {}
    
    # Add dates and prices to test and actual hashmaps
    for (_, row), price, predicted_prices in zip(test_data_dates.iterrows(), test_data_prices, predicted_prices):
        date = row['Date']
        test[datetime.fromtimestamp(date + 86400)] = price
        actual[datetime.fromtimestamp(date + 86400)] = predicted_prices

    # Create a bar chart
    plt.figure(figsize=(6, 6))
    plt.bar(list(test.keys()), list(test.values()))
    plt.xlabel('Date')
    plt.ylabel('Price, $')
    plt.title('Test Data Prices')
    plt.xticks(rotation=45)
    
    # Create a new figure and axis for the second bar chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(list(actual.keys()), list(actual.values()))
    ax.set_xlabel('Date')
    ax.set_ylabel('Price, $')
    ax.set_title('Actual Data Prices')

    graph_filename = './testVsActual.png'
    plt.savefig(graph_filename)
    plt.show()



