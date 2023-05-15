import data_processing.data_training
import data_processing.visualize

# Create predictions
google = data_processing.data_training.process_data("google")
apple = data_processing.data_training.process_data("apple")
amazon = data_processing.data_training.process_data("amazon")
meta = data_processing.data_training.process_data("meta")

# Visualization

data_processing.visualize.visualize(google, apple, amazon, meta)