# Implementation of Multivariate Attention LSTM + FCN block
# Author: Shobhit Lamba
# e-mail: slamba4@uic.edu

# Importing the libraries
from keras.models import Model
from keras.layers import Input, Dense, concatenate, Activation
from keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout

from utils.layer_utils import AttentionLSTM

MAX_TIMESTEPS = 100 #Placeholder
MAX_NB_VARIABLES = 100 #Placeholder
NB_CLASSES = 100 # Placeholder

def malstm_fcn_block():
    
    ip = Input(shape=(MAX_NB_VARIABLES, MAX_TIMESTEPS))

    x = Masking()(ip)
    x = AttentionLSTM(8)(x)
    x = Dropout(0.8)(x)

    y = Permute((2, 1))(ip)
    y = Conv1D(128, 8, padding = "same", kernel_initializer = "he_uniform")(y)
    y = BatchNormalization()(y)
    y = Activation("relu")(y)

    y = Conv1D(256, 5, padding = "same", kernel_initializer = "he_uniform")(y)
    y = BatchNormalization()(y)
    y = Activation("relu")(y)

    y = Conv1D(128, 3, padding = "same", kernel_initializer = "he_uniform")(y)
    y = BatchNormalization()(y)
    y = Activation("relu")(y)

    y = GlobalAveragePooling1D()(y)

    x = concatenate([x, y])

    out = Dense(NB_CLASS, activation = "softmax")(x)

    model = Model(ip, out)
    model.summary()

    return model