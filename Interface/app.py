from nltk import word_tokenize, WordNetLemmatizer
import os
import numpy as np
import matplotlib.pyplot as plt
import time 
import chart as charting

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import taglish_sentiment_analysis_cnn as model

from werkzeug.utils import secure_filename
import os
import pandas as pd
import csv
from io import StringIO
import sys



sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


app = Flask(__name__)

import os
from os.path import join, dirname, realpath

#global variable 
input_with_polarity = []


# enable debugging mode
app.config["DEBUG"] = True

# Upload folder for files
UPLOAD_FOLDER = 'C:/Users/johnr/Documents/Sentiment Analysis/sentiment-analysis-thesis/Interface/static/files/'
#UPLOAD_FOLDER = 'C:/Users/AlphaQuadrant/Documents/thesis-development/sentiment-analysis-thesis/Interface/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER



#homepage
@app.route('/')
def main():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/about',methods=['POST','GET'])
def about():
    return render_template("about_us.html")

# Go to analyze page
@app.route('/sentiment',methods=['POST','GET'])
def sentiment():
    return render_template("analyze.html")
    
#predict single input
@app.route('/predict',methods=['POST','GET'])

def predict():
    
    input = request.form.get("sentimentArea")

    if request.method == "POST" and input != '':
        # getting input with name = fname in HTML form
        sentiment = model.predict_single_sentiment(input)
        print(sentiment)
    else:
        return render_template("analyze.html",sentiment='Input is Empty',input_text=input)
    
    if(sentiment==3):
       return render_template("analyze.html",sentiment='Input is invalid')
    
    if(sentiment==2):
        return render_template("analyze.html",sentiment='Predicted Sentiment:  Positive',input_text=input,
                               input = 'Input text: ' + input)

    if(sentiment==1):
        return render_template("analyze.html",sentiment='Predicted Sentiment:  Neutral',input_text=input, input =  'Input text: ' 
                               + input)

    if(sentiment==0):
        return render_template("analyze.html",sentiment='Predicted Sentiment:  Negative',input_text=input, input =  'Input text: ' 
                               + input)

#------------------------------------------------------------------------------------------------------------------------------

def show_chart(sentiment, data, colors, explode, chart_name,title):
    
        
    # Wedge properties
    wp = { 'linewidth' : 1.5, 'edgecolor' : "black" }
    
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(round(pct / 100.*np.sum(allvalues)))
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
                                    textprops = dict(color ="white"))
    
    # Adding legend
    ax.legend(wedges, sentiment,
            title ="Sentiment Polarity",
            loc ="center left",
            bbox_to_anchor =(1.07, 0, 0.5, 1))
    
    plt.setp(autotexts, size = 12, weight ="bold")
    ax.set_title(title)
    
    #filename = 'C:/Users/AlphaQuadrant/Documents/thesis-development/sentiment-analysis-thesis/Interface/static/images/' + chart_name
    filename = 'C:/Users/johnr/Documents/Sentiment Analysis/sentiment-analysis-thesis/Interface/static/images/' + chart_name
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
    colors = ( "#ff3a47", "#7c777a", "#31458c",'#003700')
    
    # Creating explode data
    explode = (0.01, 0.01, 0.01, 0.01)
    
    title = "Chart by Sentiment Polarity"

    show_chart(sentiment, data, colors, explode, chart_name, title)
   
   
   
# CHART BY WITH OR WITHOUT EMOJI 
def show_with_emoji_chart(data):
    
    chart_name = 'with_emoji_chart'
    
    # Creating dataset
    sentiment = ['WITH EMOJI', 'WITHOUT EMOJI']
    
    # Creating color parameters
    colors = ( "#31458c", "#ff3a47")
    
    # Creating explode data
    explode = (0.01, 0.01)
    
    title = "Chart by Emoji Presence"

    show_chart(sentiment, data, colors, explode,chart_name,title)
    
    
    
# CHART BY SENTIMENT POLARITY WITH OR WITHOUT EMOJI    
def show_sentiment_with_emoji_chart(data):
    
    chart_name = 'sentiment_with_emoji_chart'
    
    # Creating dataset
    sentiment = ['Positive with Emoji', 'Neutral with Emoji', 'Negative with Emoji' ]
    
    # Creating color parameters
    colors = ( "#31458c", "#7c777a", "#ff3a47")
    
    # Creating explode data
    explode = (0.01, 0.01, 0.01)
    
    title = "Chart by Sentiment With Emoji"

    show_chart(sentiment, data, colors, explode, chart_name,title)


# CHART BY SENTIMENT POLARITY WITH OR WITHOUT EMOJI    
def show_sentiment_without_emoji_chart(data):
    
    chart_name = 'sentiment_without_emoji_chart'
    
    # Creating dataset
    sentiment = [ 'Positive without Emoji', 'Neutral without Emoji', 'Negative without Emoji' ]
    
    # Creating color parameters
    colors = ( '#31458c','#7c777a','#ff3a47')
    
    # Creating explode data
    explode = ( 0.01, 0.01, 0.01)
    
    title = "Chart by Sentiment Without Emoji"

    show_chart(sentiment, data, colors, explode, chart_name,title)


#------------------------------------------------------------------------------------------------------------------------------

#predict multiple input   
@app.route('/predict_multiple',methods=['POST','GET'])

def uploadFiles():
    #count sentiments with or without emoji
    isEmoji = []

    positive_with_emoji = 0
    positive_no_emoji = 0

    negative_with_emoji = 0
    negative_no_emoji = 0

    neutral_with_emoji = 0
    neutral_no_emoji = 0

    #global variable list for predicted polarity with emoji(True or False)
    global input_with_polarity
    input_with_polarity = []

    # get the uploaded file
    uploaded_file = request.files['file']    
    
    # check if the file is not empty 
    if uploaded_file.filename != '':
        
        if uploaded_file.filename.rsplit('.', 1)[1].lower() != 'csv':
            return render_template("analyze.html", show = "False")

        

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
         

        #read the uploaded file
        data = pd.read_csv(file_path,header = None)
        
        cols = len(data.axes[1])
        
        # CHECK HOW MANY COLUMNS OF THE CSV FILE
        
        if cols > 1 :
            return render_template("analyze.html", show = "False")
            

        data.columns = ['text']

        sentiment_prediction = []
        emoji = 0
        no_emoji = 0
        inv = 0
      

        for text in data['text']:
            polarity = model.predict_sentiment(text)
            
            print("ETOOOOO : ",polarity)
            
            if(polarity[0]==3):
                print("INVALIIIIIIDDDDDDDD")
                inv += 1
                sentiment_prediction.append("invalid")
            else:
                sentiment_prediction.append(polarity[0])
                    

            isEmoji.append(polarity[1])

            #count inputs with emoji and w/o emoji
            if(polarity[1]):
                emoji += 1
            else:
                no_emoji += 1

        #write to csv
        


        #save the text and its respective polarity into list of list
        for n in range(len(data['text'])):
            input_with_polarity.append([data['text'][n],sentiment_prediction[n],isEmoji[n]])

            if(sentiment_prediction[n] == 0 ):
                if(isEmoji[n] == 1):
                    negative_with_emoji +=1
                else:
                    negative_no_emoji +=1

            elif(sentiment_prediction[n] == 1 ):
                if(isEmoji[n] == 1):
                    neutral_with_emoji +=1
                else:
                    neutral_no_emoji +=1

            elif(sentiment_prediction[n] == 2 ):
                if(isEmoji[n] == 1):
                    positive_with_emoji +=1
                else:
                    positive_no_emoji +=1
        
        pos = 0
        neg = 0
        neu = 0
        

        for sentiment in sentiment_prediction:
            if(sentiment==0):
                neg+=1
            if(sentiment==2):
                pos+=1
            if(sentiment==1):
                neu+=1
            
                
        invalid_qty = inv #len(data['text'])-(pos + neg)
        
        print('positive: ',pos,'  negative: ',neg,'  neutral: ',neu)
        print('with emoji: ',emoji,'   without emoji: ',no_emoji)
        print('Positive with emoji:',positive_with_emoji,'  Positive w/o emoji: ',positive_no_emoji)
        print('Negative with emoji:',negative_with_emoji,'  Negative w/o emoji: ',negative_no_emoji)
        print('Neutral with emoji:',neutral_with_emoji,'  Neutral w/o emoji: ',neutral_no_emoji)
        print('Invalid:',invalid_qty)

        
        
        empty_file = 1
    else:
        empty_file = 0
    
    #start ako dito 
    header = ['Text', 'Polarity','Emoji present']

    si = StringIO()
        
    #with open('summarize.csv', 'w',newline='', encoding='UTF8') as f:
    writer = csv.writer(si)

    # write the header
    writer.writerow(header)

    # write the data
    for i in range(len(input_with_polarity)):
        print(i,' ',input_with_polarity[i])
        writer.writerow(input_with_polarity[i])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
        
    if(empty_file == 1):
        
        # GET THE DATA THAT WILL BE FED INTO THE CHART
        
        sentiment_chart = (pos == 0 and neg == 0 and neu == 0 and invalid_qty == 0)
        if not(sentiment_chart):
            data = (pos, neg, neu, invalid_qty)
            show_sentiment_chart(data)
        
        
        with_emoji_chart  = emoji == 0 and no_emoji == 0
        if not (with_emoji_chart):
            data = (emoji,no_emoji)
            show_with_emoji_chart(data)
            
        sentiment_with_emoji_chart = (positive_with_emoji == 0 and negative_with_emoji == 0 and neutral_with_emoji == 0)
        if not(sentiment_with_emoji_chart) :
            data = (positive_with_emoji,negative_with_emoji,neutral_with_emoji)
            show_sentiment_with_emoji_chart(data)
        
        sentiment_without_emoji_chart = (positive_no_emoji == 0 and neutral_no_emoji == 0 and negative_no_emoji == 0)
        if not (sentiment_without_emoji_chart) :
            data = (positive_no_emoji,neutral_no_emoji,negative_no_emoji)
            show_sentiment_without_emoji_chart(data)
        
        time.sleep(2)
        print("lassttt")
        print(sentiment_with_emoji_chart)
        
        
        return render_template("analyze.html", positive = 'Positive: ', positive_qty = pos, 
                               
        negative= 'Negative:', negative_qty = neg, neutral= 'Neutral:', neutral_qty = neu,
        
        with_emoji_label = 'With Emoji: ',with_emoji=emoji,
        
        wo_emoji_label = 'Without Emoji: ', wo_emoji=no_emoji,
        
        positive_emoji_label = 'Positive with Emoji: ',positive_with_emoji = positive_with_emoji,
        
        negative_emoji_label = 'Negative with Emoji',negative_with_emoji = negative_with_emoji,
        
        neutral_emoji_label = 'Neutral with Emoji: ',neutral_with_emoji = neutral_with_emoji,
        
        positive_no_emoji_label = 'Positive w/o Emoji',positive_no_emoji = positive_no_emoji,
        
        neutral_no_emoji_label = 'Neutral w/o Emoji: ',neutral_no_emoji = neutral_no_emoji,
        
        negative_no_emoji_label = 'Negative w/o Emoji: ',negative_no_emoji = negative_no_emoji,
        
        show = "True", invalid = "Invalid: ",invalid_qty = invalid_qty,sentiment_with_emoji_chart_html = sentiment_with_emoji_chart,
        sentiment_chart_html = sentiment_chart, with_emoji_chart_html = with_emoji_chart, sentiment_without_emoji_chart_html = sentiment_without_emoji_chart  )
        
        
        
    else:
        return render_template("analyze.html", show = "Empty")
    

#download csv copy   
@app.route('/download',methods=['POST','GET'])

def download():

    header = ['Text', 'Polarity','With Emoji']

    si = StringIO()
        
    #with open('summarize.csv', 'w',newline='', encoding='UTF8') as f:
    writer = csv.writer(si)

    # write the header
    writer.writerow(header)

    # write the data
    for i in range(len(input_with_polarity)):
        print(i,' ',input_with_polarity[i])
        writer.writerow(input_with_polarity[i])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
        
    return output

if __name__ == '__main__':
    app.run(debug=True)
    
