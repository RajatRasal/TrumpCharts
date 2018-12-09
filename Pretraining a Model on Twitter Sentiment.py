import pandas as pd
import tensorflow as tf
import numpy as np
batch_size = 50
tweets = np.load("data/tweets_integerized.npy")
tweets = [item for sublist in tweets for item in sublist]

couples, labels = tf.keras.preprocessing.sequence.skipgrams(tweets, len(tweets), window_size=1)
bigrams = [x for x, y in zip(couples, labels) if y]
batches = [bigrams[i:i + batch_size] for i in range(0, len(bigrams), batch_size)]
input_inputs = [list(zip(*x)) for x in batches]
input_inputs = input_inputs[:-1]
print("done with preprocessing")


# In[38]:


import math
num_sampled = 64
graph = tf.Graph()
vocab_size = len(tweets)
embedding_size = 4
with graph.as_default():
    
    embeddings = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0))
    
    nce_weights = tf.Variable(tf.truncated_normal(
        [vocab_size, embedding_size], stddev=1.0/math.sqrt(embedding_size)))
    
    nce_biases = tf.Variable(tf.zeros([vocab_size]))
    
    
    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    
    embed = tf.nn.embedding_lookup(embeddings, train_inputs)
    
    loss = tf.reduce_mean(
        tf.nn.nce_loss(weights=nce_weights,
                       biases=nce_biases,
                       labels=train_labels,
                       inputs=embed,
                       num_sampled=num_sampled,
                       num_classes=vocab_size))
    
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)
    init = tf.global_variables_initializer()

    saver = tf.train.Saver()


# In[42]:



with tf.Session(graph=graph) as session:
    init.run()
    
    for inputs, labels in input_inputs:
        inputs = np.array(inputs)
        labels_array = [[l] for l in labels]
        feed_dict = {train_inputs: inputs, train_labels: labels_array}
        _, cur_loss = session.run([optimizer, loss], feed_dict=feed_dict)

    save_path = saver.save(session, "/tmp/model.ckpt")

    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
    normalized_embeddings = embeddings / norm

print("yeet done")


