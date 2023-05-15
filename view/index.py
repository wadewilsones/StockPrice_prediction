from flask import Flask, render_template, request
from analyzer.data_processing.data_training import process_data


app = Flask(__name__)

#Create routing for an app
@app.route("/", methods=['GET', 'POST'])

def index():
    #Validate input
    errorMessage = None
    try:
        errorMessage = None # update error value to null
        if request.method == 'POST':
                selected_radio = request.form.get('stock').lower()
                print(selected_radio)
                #Start builing a model
                getPrediction = process_data(selected_radio)
             
    except Exception as err:
        #Display error
        errorMessage = err#"Select one of the options!"
        print(errorMessage)
    return render_template('index.html', errorMessage = errorMessage)