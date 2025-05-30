import tkinter
from textblob import TextBlob
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords

main = tkinter.Tk()
main.title("Balancing Social Influencing positive and negative opinions in online networks") #designing main screen
main.geometry("1300x1200")

global filename
tweets_list = []
clean_list = []
global pos, neu, neg

def tweetCleaning(doc):
    tokens = doc.split()
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    tokens = ' '.join(tokens) #here upto for word based
    return tokens

def upload(): #function to upload tweeter profile
    global filename
    filename = filedialog.askopenfilename(initialdir="dataset")
    pathlabel.config(text=filename)
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");

def read():
    text.delete('1.0', END)
    tweets_list.clear()
    train = pd.read_csv(filename,encoding='iso-8859-1')
    for i in range(len(train)):
        tweet = train._get_value(i, 'Text')
        tweets_list.append(tweet)
        text.insert(END,tweet+"\n")
    text.insert(END,"\n\nTotal tweets found in dataset is : "+str(len(tweets_list))+"\n\n\n")        

def clean():
    text.delete('1.0', END)
    clean_list.clear()
    for i in range(len(tweets_list)):
        tweet = tweets_list[i]
        tweet = tweet.strip("\n")
        tweet = tweet.strip()
        tweet = tweetCleaning(tweet.lower())
        clean_list.append(tweet)
        text.insert(END,tweet+"\n")
    text.insert(END,"\n\nTotal tweets found in dataset is : "+str(len(clean_list))+"\n\n\n")         
    
    
def machineLearning():
    text.delete('1.0', END)
    global pos, neu, neg
    pos = 0
    neu = 0
    neg = 0
    for i in range(len(clean_list)):
        tweet = clean_list[i]
        blob = TextBlob(tweet)
        if blob.polarity <= 0.5:
            neg = neg + 1
            text.insert(END,tweet+"\n")
            text.insert(END,"Predicted Sentiment : FAKE\n")
            text.insert(END,"Polarity Score      : "+str(blob.polarity)+"\n")
            text.insert(END,'====================================================================================\n')
        
        if blob.polarity > 0.51:
            pos = pos + 1
            text.insert(END,tweet+"\n")
            text.insert(END,"Predicted Sentiment : AUTHENTICATED\n")
            text.insert(END,"Polarity Score      : "+str(blob.polarity)+"\n")
            text.insert(END,'====================================================================================\n')
    
def graph():
    label_X = []
    category_X = []
    text.delete('1.0', END)
    text.insert(END,"Saftey Factor\n\n")
    text.insert(END,'Authenticated : '+str(pos)+"\n")
    text.insert(END,'Fake : '+str(neg)+"\n")
    text.insert(END,'Length of tweets  : '+str(len(clean_list))+"\n")
    text.insert(END,'Authenticated : '+str(pos)+' / '+ str(len(clean_list))+' = '+str(pos/len(clean_list))+'%\n')
    text.insert(END,'Fake : '+str(neg)+' / '+ str(len(clean_list))+' = '+str(neg/len(clean_list))+'%\n')
    label_X.append('Authenticated')
    label_X.append('Fake')
    category_X.append(pos)
    category_X.append(neg)

    plt.pie(category_X,labels=label_X,autopct='%1.1f%%')
    plt.title('Sentiment Graph')
    plt.axis('equal')
    plt.show()

font = ('times', 16, 'bold')
title = Label(main, text='Balancing Social Influencing positive and negative opinions in online networks')
title.config(bg='LightSteelBlue', fg='black')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
uploadButton = Button(main, text="Upload Tweets Dataset", command=upload)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='sky blue3', fg='white')  
pathlabel.config(font=font1)           
pathlabel.place(x=370,y=100)

readButton = Button(main, text="Read Tweets", command=read)
readButton.place(x=50,y=150)
readButton.config(font=font1) 

cleanButton = Button(main, text="text Preprocessing", command=clean)
cleanButton.place(x=210,y=150)
cleanButton.config(font=font1) 

mlButton = Button(main, text="NLP + Machine Learning", command=machineLearning)
mlButton.place(x=470,y=150)
mlButton.config(font=font1) 

graphButton = Button(main, text="Performance Graph", command=graph)
graphButton.place(x=730,y=150)
graphButton.config(font=font1) 

font1 = ('times', 12, 'bold')
text=Text(main,height=25,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)


main.config(bg='LightSteelBlue')
main.mainloop()
