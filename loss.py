import tensorflow as tf
from keras.backend.tensorflow_backend import _to_tensor
from keras.backend.common import epsilon
def entropy_categorical_crossentropy(target, output):
    output /= tf.reduce_sum(output,
                            axis=len(output.get_shape()) - 1,
                            keep_dims=True)

    _epsilon = _to_tensor(epsilon(), output.dtype.base_dtype)
    output = tf.clip_by_value(output, _epsilon, 1. - _epsilon)
    return - tf.reduce_sum((target - .001*output) * tf.log(output),
                           axis=len(output.get_shape()) - 1)
    #return - tf.reduce_sum((target) * tf.log(output),
    #                       axis=len(output.get_shape()) - 1)
