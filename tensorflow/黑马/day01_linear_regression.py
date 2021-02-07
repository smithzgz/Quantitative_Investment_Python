import tensorflow as tf


def leaner_regression():
    """
    自实现显性回归
    :return:
    """
    # 准备数据
    x = tf.random_normal(shape=[100, 1])
    y_true = tf.matmul(x, [[0.8]]) + 0.7

    # 构造模型 定义模型参数用变量
    weights = tf.Variable(initial_value=tf.random_normal(shape=[1, 1]))
    bias = tf.Variable(initial_value=tf.random_normal(shape=[1, 1]))
    y_predict = tf.matmul(x, weights) + bias

    # 构造损失函数
    error = tf.reduce_mean(tf.square(y_predict - y_true))

    # 优化损失
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(error)

    # 显性初始化变量
    init = tf.global_variables_initializer()

    # 开启会话
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init)

        # 查看初始化模型前值
        print("训练前，权重%f, 偏置%f, 损失%f" % (weights.eval(), bias.eval(), error.eval()))

        # 开始训练
        for i in range(500):
            sess.run(optimizer)
            # 查看初始化模型后值
            print("训练前，权重%f, 偏置%f, 损失%f" % (weights.eval(), bias.eval(), error.eval()))


if __name__ == "__main__":
    leaner_regression()
