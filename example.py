# an example
from keras.utils.np_utils import to_categorical
from keras.layers import Dense
import pandas as pd
from lineage import Lineage
import numpy as np


# load the data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

Y_train = train[['label']]
X_train = train.drop(train.columns[[0]], axis=1)
X_test = test

#Reshape the training and test set
X_train = np.array(X_train)
X_test = np.array(X_test)
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

#Padding the images by 2 pixels since in the paper input images were 32x32
X_train = np.pad(X_train, ((0,0),(2,2),(2,2),(0,0)), 'constant')
X_test = np.pad(X_test, ((0,0),(2,2),(2,2),(0,0)), 'constant')

#Standardization
mean_px = X_train.mean().astype(np.float32)
std_px = X_train.std().astype(np.float32)
X_train = (X_train - mean_px)/(std_px)

#One-hot encoding the labels
Y_train = to_categorical(Y_train)


# we split off a validation set for assessing fitness
X_val = X_train[1:10000]
Y_val = Y_train[1:10000]

X_train = X_train[10001:]
Y_train = Y_train[10001:]

# We need a few things to establish a population
output_config = Dense(units = 10, activation = 'softmax').get_config()
input_shape = (32, 32, 1)
loss = 'categorical_crossentropy'


lineage = Lineage(input_shape, output_config, loss, X_train, Y_train, X_val, Y_val, trainsize = 31999, valsize = 5000)
lineage.initialise(20)
lineage.evolve([20]*50, num_parents = 2, selection = "weighted")
lineage.evolve([50]*50, num_parents = 2, selection = "weighted")



# establish a lineage with training and validation data
lineage = Lineage(input_shape, output_config, loss, X_train, Y_train, X_val, Y_val, trainsize = 20000, valsize = 2000)

# start with a population of 10 random networks
lineage.initialise(5)

# now we'll evolve it with 2 parents:
	# 5 generations of population size 10
	# 5 generations of population size 20
lineage.evolve([10]*5 + [20]*5, num_parents = 2)

# then for another 50 generations of 40 individuals, with 4 parents each
# we'll also kill off the least-fit 20 individuals in each generation
# first we have to increase the population size to 40, to give us enough to kill 20
lineage.evolve([40]*1, num_parents = 2)

# now we can do our next 50 generations
lineage.evolve([40]*50, num_parents = 2, kill = 20)


