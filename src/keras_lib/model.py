'''
Created on 8 Mar 2017

@author: Srikanth Ronanki
'''

import random
import numpy as np

import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, LSTM
from keras.layers import Dropout

class kerasModels(object):
    
    def __init__(self, n_in, hidden_layer_size, n_out, hidden_layer_type, output_type='linear', dropout_rate=0.0, loss_function='mse', optimizer='adam'):
        """ This function initialises a neural network
        
        :param n_in: Dimensionality of input features
        :param hidden_layer_size: The layer size for each hidden layer
        :param n_out: Dimensionality of output features
        :param hidden_layer_type: the activation types of each hidden layers, e.g., TANH, LSTM, GRU, BLSTM
        :param output_type: the activation type of the output layer, by default is 'LINEAR', linear regression.
        :param dropout_rate: probability of dropout, a float number between 0 and 1.
        :type n_in: Integer
        :type hidden_layer_size: A list of integers
        :type n_out: Integrer
        """
        
        self.n_in  = int(n_in)
        self.n_out = int(n_out)
        
        self.n_layers = len(hidden_layer_size)
       
        self.hidden_layer_size = hidden_layer_size
        self.hidden_layer_type = hidden_layer_type
        
        assert len(self.hidden_layer_size) == len(self.hidden_layer_type)
        
        self.output_type   = output_type 
        self.dropout_rate  = dropout_rate
        self.loss_function = loss_function
        self.optimizer     = optimizer

        self.batch_size    = 10
        self.utt_length    = 100

        print "output_type   : "+self.output_type
        print "loss function : "+self.loss_function
        print "optimizer     : "+self.optimizer

        # create model
        self.model = Sequential()

    def define_feedforward_model(self):
        seed = 12345
        np.random.seed(seed)
        
        # add hidden layers
        for i in xrange(self.n_layers):
            if i == 0:
                input_size = self.n_in
            else:
                input_size = self.hidden_layer_size[i - 1]

            self.model.add(Dense(
                    units=self.hidden_layer_size[i],
                    activation=self.hidden_layer_type[i],
                    kernel_initializer="normal",
                    input_dim=input_size))
            self.model.add(Dropout(self.dropout_rate))

        # add output layer
        self.final_layer = self.model.add(Dense(
            units=self.n_out,
            activation=self.output_type.lower(),
            kernel_initializer="normal",
            input_dim=self.hidden_layer_size[-1]))

        # Compile the model
        self.compile_model()

    def define_sequence_model(self):
        seed = 12345
        np.random.seed(seed)
        
        # add hidden layers
        for i in xrange(self.n_layers):
            if i == 0:
                input_size = self.n_in
            else:
                input_size = self.hidden_layer_size[i - 1]
           
            if self.hidden_layer_type[i]=='lstm': 
                self.model.add(LSTM(
                        units=self.hidden_layer_size[i],
                        input_shape=(None, input_size),
                        return_sequences=True))
                        #stateful=True))   #go_backwards=True))
            else:
                self.model.add(Dense(
                        units=self.hidden_layer_size[i],
                        activation=self.hidden_layer_type[i],
                        kernel_initializer="normal",
                        input_shape=(None, input_size)))

        # add output layer
        self.final_layer = self.model.add(Dense(
            units=self.n_out,
            input_dim=self.hidden_layer_size[-1],
            kernel_initializer='normal',
            activation=self.output_type.lower()))

        # Compile the model
        self.compile_model()
    
    def define_stateful_model(self):
        seed = 12345
        np.random.seed(seed)
        
        # params
        batch_size = self.batch_size
        timesteps  = self.utt_length

        # add hidden layers
        for i in xrange(self.n_layers):
            if i == 0:
                input_size = self.n_in
            else:
                input_size = self.hidden_layer_size[i - 1]
           
            if hidden_layer_type[i]=='lstm': 
                self.model.add(LSTM(
                        units=self.hidden_layer_size[i],
                        batch_input_shape=(batch_size, timesteps, input_size),
                        return_sequences=True,
                        stateful=True))   #go_backwards=True))
            else:
                self.model.add(Dense(
                        units=self.hidden_layer_size[i],
                        activation=self.hidden_layer_type[i],
                        kernel_initializer="normal",
                        batch_input_shape=(batch_size, timesteps, input_size)))

        # add output layer
        self.final_layer = self.model.add(Dense(
            units=self.n_out,
            input_dim=self.hidden_layer_size[-1],
            kernel_initializer='normal',
            activation=self.output_type.lower()))

        # Compile the model
        self.compile_model()

    def compile_model(self):
        self.model.compile(loss=self.loss_function, optimizer=self.optimizer, metrics=['accuracy'])
        print "model compiled successfully!!"
        
    def save_model(self, json_model_file, h5_model_file):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(json_model_file, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(h5_model_file)
        print("Saved model to disk")

    def load_model(self, json_model_file, h5_model_file):
        #### load the model ####
        json_file = open(json_model_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(h5_model_file)
        print("Loaded model from disk")
    
        #### compile the model ####
        self.model = loaded_model
        self.compile_model()



        
