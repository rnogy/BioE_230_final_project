###Just for fun, although we will not get any insight, and no dim to be reduced.
###But we can try NNMF to see what happenes

import tensorflow as tf
weights = DOPC_X
MSE = tf.keras.losses.MeanSquaredError()
opt = tf.keras.optimizers.Adam(learning_rate = 1)
num_cluster = 13
dim = num_cluster
H = tf.Variable(tf.random.normal((weights.shape[0], dim)))
W = tf.Variable(tf.random.normal((dim, weights.shape[1])))
for step in range(202):
    with tf.GradientTape(persistent=True) as tape:
        tape.watch([H, W])
        out = MSE(H@W, weights)
        
    grads = tape.gradient(out, [H, W])
    opt.apply_gradients(zip(grads, [H,W]))
    if step % 100 == 1:
        print(step, out)

for i in range(num_cluster):
    clu = np.where(np.argmax(H, 1) == i)
    plt.scatter(X[:,0][[clu]],X[:,1][[clu]])