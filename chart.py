import numpy as np
import matplotlib.pyplot as plt
import time

def show_chart(sentiment, data, colors, explode, chart_name):
    
    
    # Wedge properties
    wp = { 'linewidth' : 3, 'edgecolor' : "black" }
    
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d} )".format(pct, absolute)
    
    # Creating plot
    fig, ax = plt.subplots(figsize =(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                    autopct = lambda pct: func(pct, data),
                                    explode = explode,
                                    labels = sentiment,
                                    shadow = True,
                                    colors = colors,
                                    startangle = 90,
                                    wedgeprops = wp,
                                    textprops = dict(color ="black"))
    
    # Adding legend
    ax.legend(wedges, sentiment,
            title ="Sentiment Polarity",
            loc ="center left",
            bbox_to_anchor =(1.07, 0, 0.5, 1))
    
    plt.setp(autotexts, size = 12, weight ="bold")
    ax.set_title("Chart")
    
    filename = 'C:/Users/AlphaQuadrant/Documents/thesis-development/sentiment-analysis-thesis/Interface/static/images/' + chart_name
    plt.savefig(filename) 

    # show plot
    #plt.show()


# CHART BY SENTIMENT POLARITY  
def show_sentiment_chart(data):
    
    chart_name = 'sentiment_chart'
    
    print(data)
    
    # Creating dataset
    sentiment = ['NEGATIVE', 'NEUTRAL', 'POSITIVE','INVALID']
    
    
    # Creating color parameters
    colors = ( "red", "grey", "green",'black')
    
    # Creating explode data
    explode = (0.0, 0.0, 0.0, 0.0)

    show_chart(sentiment, data, colors, explode, chart_name)
   
   
   
# CHART BY WITH OR WITHOUT EMOJI 
def show_with_emoji_chart():
    
    chart_name = 'with_emoji_chart'
    
    # Creating dataset
    sentiment = ['WITH EMOJI', 'WITHOUT EMOJI']
    
    data = [390, 367]
    
    # Creating color parameters
    colors = ( "yellow", "grey")
    
    # Creating explode data
    explode = (0.0, 0.0)

    show_chart(sentiment, data, colors, explode,chart_name)
    
    
    
# CHART BY SENTIMENT POLARITY WITH OR WITHOUT EMOJI    
def show_sentiment_with_emoji_chart():
    
    chart_name = 'sentiment_with_emoji_chart'
    
    # Creating dataset
    sentiment = ['Positive with Emoji', 'Neutral with Emoji', 'Negative with Emoji', 'Positive without Emoji', 'Neutral without Emoji', 'Negative without Emoji' ]
    
    data = [390, 367, 410, 321, 333, 225]
    
    # Creating color parameters
    colors = ( "red", "grey", "green",'red','grey','green')
    
    # Creating explode data
    explode = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    show_chart(sentiment, data, colors, explode, chart_name)



# SHOW SENTIMENT BY CHART
#show_sentiment_chart(data)

# SHOW CHART BY EMOJI 
#show_with_emoji_chart()

# CHART BY SENTIMENT POLARITY WITH OR WITHOUT EMOJI
#show_sentiment_with_emoji_chart()

