import time
import os
import plot_utility
import numpy as np
import string_processing
from lstm import *

SEQUENCE_LEN = 50
BATCH_SIZE = 256

IN_LEN = string_processing.CHARS_LEN
HIDDEN_LEN_1 = 500
HIDDEN_LEN_2 = 400
OUT_LEN = string_processing.CHARS_LEN

layer1 = LSTM_Layer("layer501",IN_LEN,HIDDEN_LEN_1)
layer2 = LSTM_Layer("layer402",HIDDEN_LEN_1,HIDDEN_LEN_2)
layer3 = TanhLayer("tanh_layer34",HIDDEN_LEN_2,OUT_LEN)
full_layer = TwoLayerLSTM(TwoLayerLSTM(layer1,layer2),layer3)

optimizer = RMSpropOpt(0.02)

full_layer_learner = Learner(full_layer,optimizer,calc_error_squared,BATCH_SIZE,SEQUENCE_LEN)

def generate_text_input():
    train_str = string_processing.get_str("data/huck_fin.txt")
    in_vec_list = string_processing.in_vec(train_str)
    in_stack = np.vstack(in_vec_list)
    return in_stack

def save_text(filename,outtxt):
    with open(filename,"w") as file:
        file.write(outtxt)

def run():
    text_in = generate_text_input()
    NUM_EPOCS = 500
    #train(full_layer_learner,text_in,text_in,NUM_EPOCS)
    state_pred = full_layer_learner.get_stateful_predict()
    [outs] = state_pred(text_in[:1000])
    #np.set_printoptions(threshold=np.inf)
    print(outs)
    print(string_processing.out_list_to_str(outs))
    [full_outs] = state_pred(text_in)
    outstr = string_processing.out_list_to_str(full_outs)
    save_text("sampled_outputs/deep_learner.txt",outstr)



def test():
    text_in = generate_text_input()
    expected = text_in[:200]
    [actual] = full_layer_learner.get_stateful_predict()(expected)
    act_text = string_processing.out_list_to_str(actual)
    my_error_fn = error_fn(calc_error_squared)
    errors = []
    skip =  1
    for i in range(0,198,skip):
        [err] = my_error_fn(expected[i+1:i+skip+1],actual[i:i+skip])
        print(err,act_text[i:i+skip])
run()
