import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Create visual representation for stock predictions
def visualize(google, apple, amazon, meta):

    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
    axs.bar(np.arange(5), google[1][:5], label='Actual')
    axs.bar(np.arange(5), google[2][:5], label='Predicted')
    axs.set_xticks(np.arange(5))
    axs.set_xticklabels(google[0][:5], rotation=45)
    axs.set_title('Google Actual vs. Predicted')
    axs.legend()
    plt.show()
  


    