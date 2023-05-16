from flask import Flask, render_template, request
from analyzer.data_processing.data_training import process_data, getStockToday, predict_stock_values
from datetime import date


app = Flask(__name__)
app.debug = True
#Create routing for an app
@app.route("/", methods=['GET', 'POST'])

def index():
    #Validate input
    errorMessage = None
    stockData = None
    try:
        errorMessage = None # update error value to null
        if request.method == 'POST':
                selected_radio = request.form.get('stock').lower()
                
                #Start builing a model
                model = process_data(selected_radio)

                # Get selected stock data for today
                today_Stock_Data = getStockToday(selected_radio)

                # Predict values based on today's data

                predicted_Stock_Data = predict_stock_values(selected_radio, today_Stock_Data, model[0])

                stockData = {
                    "Company": selected_radio,
                    "Date": date.today(),
                    "Open": today_Stock_Data['1. open'],
                    "High":  today_Stock_Data['2. high'],  
                    "Low":today_Stock_Data['3. low'],
                    "Volume":today_Stock_Data['4. close'],
                    "Prediction for tommorow":"Test"
                }
                
             
    except Exception as err:
        #Display error
        errorMessage = err#"Select one of the options!"
        print(errorMessage)
    return render_template('index.html', errorMessage = errorMessage, stockData = stockData)