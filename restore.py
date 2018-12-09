import tensorflow as tf
import numpy as np
from tensorflow.python.tools import inspect_checkpoint as chkp
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

tf.reset_default_graph()

# Create some variables.
v1 = tf.get_variable("Variable", shape=[2868364,4])

# Add ops to save and restore all the variables.
saver = tf.train.Saver({"Variable": v1})

# Later, launch the model, use the saver to restore variables from disk, and
# do some work with the model.
with tf.Session() as sess:
  # Restore variables from disk.
  saver.restore(sess, "/tmp/model.ckpt")
  print("Model restored.")
  # Check the values of the variables
  print("v1 : %s" % v1.eval())

  wordVectors = v1.eval()

embedded = TSNE(n_components=2, perplexity=50).fit_transform(final_embeddings[:1000])

plt.scatter(embedded[:, 0], embedded[:, 1])
plt.show()


