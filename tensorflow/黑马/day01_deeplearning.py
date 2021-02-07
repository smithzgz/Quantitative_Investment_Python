import tensorflow as tf


def tensorflow_demo():
    a = 2
    b = 3
    c = a + b
    print("普通加分运行结果：", c)

    a_t = tf.constant(2)
    b_t = tf.constant(3)
    c_t = a_t + b_t
    print("tf运行结果：", c_t)

    # 开启会话
    with tf.Session() as sess:
        c_t_value = sess.run(c_t)
        print("会话结果" , c_t_value)

if __name__ == "__main__":
    tensorflow_demo()
