import docx2txt,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
stop_words = set(stopwords.words('english'))

def clean(text):
  text=re.sub('http\S+\s*',' ',text)
  text=re.sub('RT|cc',' ',text)
  text=re.sub('#\S+','',text)
  text=re.sub('@\S+','',text)
  text=re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""),' ' ,text)
  text=re.sub('\s+',' ',text)
  text=re.sub(r'[^\x00-\x7f]',r' ',text)
  return text


def getText(filename):
    return docx2txt.process(filename)

#nlp tasks
def cleanData(text):
    text = text.lower() #lower case
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] #stopwords removal
    text = ' '.join(filtered_sentence)
    text = re.sub(r'[^\w\s]', '', text) #remove punctuations
    text = re.sub(' +', ' ',text) #remove extra spaces
    return text

def howmuchsimilar(text):
    count_matrix = cv.fit_transform(text)
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text[0])
    
    top_keywords = list(word_cloud.words_.keys())[:20]
    return [matchPercentage,top_keywords]

def thresholddata(matchPercentage):
    # if matchPercentage <= 6:
    #     return "Rejected!"
    if (matchPercentage <=15):
        return "Rejected!"
    elif (matchPercentage > 15 and matchPercentage <=35):
        return "Selected! Esclated to the next round!"
    elif matchPercentage>35 and matchPercentage<=100:
        return "Great Match! "

"""# New Section"""