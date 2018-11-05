import yaml
import time
from random import randint

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback, TensorBoard
from keras.models import load_model

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

from numpy import array
import numpy as np

import gym

'''
from test_suite.MSPackman import MSPackMan
from test_suite.CartPole import CartPole
from test_suite.RPM import RPM

from test_suite.benchmark import Benchmark

from test_suite.gen import gen
'''

# RPM STUFF *************************

#https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list

def genRPM():
    rpm = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    
    #We have three variables in each Matrix
    for i in range(0,3):
        #Start var at a random type (not always blue to start)
        tempVar = randint(0,2) / 2
    
        #Not always increment by type (not blue -> red always)
        if randint(0,1) == 1:
            menter = -1/2
        else:
            menter = 1/2
        
        #Change all columns (accros a row it is the same)
        if randint(0,1) == 1:
            for j in range(0,3):
                #1.1 used to set 1.5 -> 0 so possible choice becomes 0, 0.5, 1.0
                rpm[0 + 3*j][i] = (tempVar + (j * menter))
                rpm[1 + 3*j][i] = (tempVar + (j * menter))
                rpm[2 + 3*j][i] = (tempVar + (j * menter))
        
        #Change all rows
        else:
            for j in range(0,3):
                rpm[0 + j][i] = (tempVar + (j * menter))
                rpm[3 + j][i] = (tempVar + (j * menter))
                rpm[6 + j][i] = (tempVar + (j * menter))
                
        for a in rpm:
            for ind, b in enumerate(a):
                if b > 1.0:
                    a[ind] = 0.0
                if b < 0:
                    a[ind] = 1.0
    
    return rpm
    
def genRPMSet(amount):
    info = []
    solution = []
    rpms = []
    for i in range(0, amount):
        rpm = genRPM()
        if rpm not in rpms:
            rpms.append(rpm)
            #[0:8] because 8 is not included
            info.append(flatten(rpm[0:8]))
            solution.append(rpm[8])
    return (info, solution)

def scoreRPM(x, y):
    runningScore = 0
    maxScore = len(x) * 3
    for set, i in enumerate(x):
        i = i[0]

        #Copy prediction data
        tmpVal = i
        
        #Classify data based on closest prediction
        for ind,val in enumerate(tmpVal):
            
            if val < (1/3):
                tmpVal[ind] = 0.0
            elif val < (2/3) and val >= (1/3):
                tmpVal[ind] = 0.5
            else:
                tmpVal[ind] = 1.0
                
        for ind, j in enumerate(i):
            if j == y[set][0][ind]:
                runningScore += 1
                
    return runningScore / maxScore

# END RPM STUFF **************************


# 


def getMeanModel(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(int(input_dim + output_dim / 2), input_shape=(input_dim,), activation='relu'))
    model.add(Dense(output_dim, activation='relu'))
    return model

def getMeanModel2(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(int(input_dim + output_dim / 2), input_shape=(1, input_dim), activation='relu'))
    model.add(Dense(output_dim, activation='relu'))
    return model

def getHalfModel(input_dim, output_dim):
    model = Sequential()
    i = input_dim
    model.add(Dense(i, input_shape=(input_dim,), activation='relu'))
    while int(i/2) >= output_dim:
        i = int(i/2)
        model.add(Dense(i, activation='relu'))
        
    model.add(Dense(output_dim, activation='relu'))
    return model

def getHalfModel2(input_dim, output_dim):
    model = Sequential()
    i = input_dim
    model.add(Dense(i, input_shape=(1, input_dim), activation='relu'))
    while int(i/2) >= output_dim:
        i = int(i/2)
        model.add(Dense(i, activation='relu'))
        
    model.add(Dense(output_dim, activation='relu'))
    return model

def getTenthModel(input_dim, output_dim):
    model = Sequential()
    i = input_dim
    model.add(Dense(i, input_shape=(input_dim,), activation='relu'))
    while int(i/10) >= output_dim:
        i = int(i/10)
        model.add(Dense(i, activation='relu'))
        
    model.add(Dense(output_dim, activation='relu'))
    return model

def getTenthModel2(input_dim, output_dim):
    model = Sequential()
    i = input_dim
    model.add(Dense(i, input_shape=(1, input_dim), activation='relu'))
    while int(i/10) >= output_dim:
        i = int(i/10)
        model.add(Dense(i, activation='relu'))
        
    model.add(Dense(output_dim, activation='relu'))
    return model


    
import csv

def logit(data, name):
    with open(name, 'a') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data['val_loss'][1::100])

def logit2(data, name):
    with open(name, 'a') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data['episode_reward'])


def main():

    #Tensorboard callback
    '''
    # Train and test models on RPM here
    x,y = genRPMSet(1000)
    x = array(x)
    y = array(y)

    #Mean
    for i in range(100):

        model = getMeanModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "mean_layer.csv")


    #half
    for i in range(100):

        model = getHalfModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "half_layer.csv")


    #tenth
    for i in range(100):

        model = getTenthModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "tenth_layer.csv")
    '''
    #**** BEGIN RPM ***** #
    
    ENV_NAME = 'CartPole-v0'

 

    # Get the environment and extract the number of actions.
    env = gym.make(ENV_NAME)
    np.random.seed(14372098)
    env.seed(14372098)

    nb_actions = env.action_space.n
    obs_dim = env.observation_space.shape[0]

    memory = EpisodeParameterMemory(limit=1000, window_length=1)

    #Mean
    '''
    for i in range(100):
        model = getMeanModel2(obs_dim, nb_actions)
        cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
                       batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
        cem.compile()

        data = cem.fit(env, nb_steps=120000, visualize=False, verbose=1)
        logit2(data.history, 'mean_rpm.csv')
    
    for i in range(50):
        model = getHalfModel2(obs_dim, nb_actions)
        cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
                       batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
        cem.compile()

        data = cem.fit(env, nb_steps=120000, visualize=False, verbose=1)
        logit2(data.history, 'half_rpm.csv')
    '''
    for i in range(50):
        model = getTenthModel2(obs_dim, nb_actions)
        cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
                       batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
        cem.compile()

        data = cem.fit(env, nb_steps=120000, visualize=False, verbose=1)
        logit2(data.history, 'tenth_rpm.csv')


    AIQ_Pack = MSPackMan()
    
    # Pass in our login info
    AIQ_Pack.username = credentials['username']
    AIQ_Pack.password = credentials['password']
    
    # For debugging
    # print(AIQ_Pack.username, AIQ_Pack.password)
    
    #Check login data
    if not AIQ_Pack.connect():
        print("Invalid login Credentials")
        exit()

    # Run 10 times
    for iter in range(1):
    
        #reset before each iteration
        AIQ_Pack.reset()
        
        for ___ in range(200):
            AIQ_Pack.render()
            AIQ_Pack.act(AIQ_Pack.env.action_space.sample()) # take a random action
            if AIQ_Pack.done:
                break
        
        print(iter + 1, ": score = ", AIQ_Pack.reward_total)

    #***** Begin RPM Example **********#
    username = credentials['username']
    password = credentials['password']
    AIQ_RPM = RPM(username, password)
    
    #Check login data
    if not AIQ_RPM.connect():
        print("Invalid login Credentials")
        exit()
    
    # Request data from RPM generator (max 750)
    results_train = AIQ_RPM.get_train(750)
    print(results_train)
    
    # Request data that needs a solution
    results_test = AIQ_RPM.get_test()
    print(results_test)
    
    #Submit a solution
    data = '"[[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]"'
    print(AIQ_RPM.submit(data))
    
    exit()

    bench = Benchmark(['RPM'])
    bench.begin()


    # Declare our AIQ object
    AIQ_cart = CartPole()
    
    # Pass in our login info
    AIQ_cart.username = credentials['username']
    AIQ_cart.password = credentials['password']
    
    # For debugging
    #print(AIQ_cart.username, AIQ_cart.password)
    
    #Check login data
    if not AIQ_cart.connect():
        print("Invalid login Credentials")
        exit()

    # Run 10 times
    for iter in range(1):
    
        #reset before each iteration
        AIQ_cart.reset()
        
        for ___ in range(200):
            AIQ_cart.render()
            AIQ_cart.act(AIQ_cart.env.action_space.sample()) # take a random action
            if AIQ_cart.done:
                break
        
        print(iter + 1, ": score = ", AIQ_cart.reward_total)
        
    
    
    
    
    
if __name__ == '__main__':
    main()
    
