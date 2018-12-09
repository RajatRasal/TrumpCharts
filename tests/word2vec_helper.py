import re
import pickle
import numpy as np

tweets = []

with open("../data/tweets_edited.pkl", "rb") as f:
    unpickler = pickle.Unpickler(f)
    sentences = unpickler.load()

    wordlist = None
    
    def find_index(x):
        try:
            i = wordlist.index(x)
        except Exception:
            i = wordlist.index("") 
        return i

    with open("../data/tweets_wordlist.pkl", "rb") as g:
        # unpickler = pickle.Unpickler(g)
        wordlist = pickle.load(g)
    
    sizes_sum = 0
    
    for i in range(len(sentences)):
        s_lower_split = re.split("( |[^a-zA-Z\d])", "".join(sentences[i]).lower())
        s_lower_split = list(filter(lambda x : x not in [" ", ""], s_lower_split))
        s_lower_split = list(map(lambda x : find_index(x), s_lower_split))
        sizes_sum += len(s_lower_split)
        tweets.append(s_lower_split)

        if i % 1000 == 0:
            print(i)

    # This is about 24.
    print(f"AVERAGE: {sizes_sum / len(sentences)}")

tweets = np.asmatrix(tweets)  # , dtype=[np.int32])

np.save("../data/tweets_integerized.npy", tweets)
