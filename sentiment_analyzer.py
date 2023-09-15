
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

def sentiment_analysis(text:str)->list:
    tweet = text

    #preprocessed tweet 
    tweet_word = []
    for word in tweet.split(' '):
        if word.startswith("@") and len(word) > 1:
            word = "@user"
        elif word.startswith("http") and len(word) > 1:
            word = "http"
        elif word.startswith("#") and len(word) > 1:
            word = "#hashtag"
        tweet_word.append(word)

    tweet_processed = ' '.join(tweet_word)

    # load model and tokenizer 
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    #Sentimental Analysis 
    encoded_tweet = tokenizer(tweet_processed, return_tensors='pt')

    output = model(**encoded_tweet)


    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return list(map(float, scores))

   




