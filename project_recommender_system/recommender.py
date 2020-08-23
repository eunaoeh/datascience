import sys, time
import numpy as np
import pandas as pd

def getData():
    matrix = np.loadtxt(sys.argv[1], dtype='int', usecols=(0,1,2)) # Load data
    matrix = pd.DataFrame({'user':matrix[:,0],
                           'item':matrix[:,1],
                           'rating':matrix[:,2]})
    # Make it as a rating matrix form    
    rating_matrix = matrix.pivot_table('rating', index='user',columns='item', fill_value=0)
    return rating_matrix

# Get simliarty by using PCC
def get_similarity(rating_matrix):
    sim_matrix = (rating_matrix.T).corr(method='pearson')
    return sim_matrix

# To estimate the rate
def estimate(user, item, rating_matrix, sim_matrix, avg, neighbor):
    # If the item is not rated by all users, return the minimum rate
    if item not in list(rating_matrix.columns):
        return 1.0
    
    norm = cnt = new_rate = res = 0
    # To add the rate of each user
    for idx, sim in neighbor:
        idx = int(idx)
        if rating_matrix.loc[idx][item] == 0:
            continue
        if cnt == 30:
            break
        cnt += 1
        norm += sim
        rate = rating_matrix.loc[idx][item]
        new_rate += sim*(rate-avg[idx])

    if norm == 0:
        res = avg[user]
    else:
        res = avg[user] + (new_rate/norm)
    if res > 5:
        res = 5.0
    elif res < 1:
        res = 1.0

    return res

# Get average rate and neighbors of each user
def get_avg_neighbor(rating_matrix):
    average = {}
    neighbors = {}
    for uid in list(rating_matrix.index):
        # Get average rate of each user
        rating = list(rating_matrix.loc[uid])
        cnt = len(list(filter(lambda x: x!=0, rating)))
        if cnt != 0:
            average[uid] = sum(rating)/cnt
        else:
            average[uid] = 0
        # Get neighbor
        neighbor = sim_matrix[uid].sort_values(ascending=False)
        neighbor = neighbor.reset_index().values.tolist()
        neighbors[uid] = neighbor

    return average, neighbors

# To predict the rate and write the result
def predict(rating_matrix, sim_matrix):
    output = sys.argv[1] + '_prediction.txt' #Output file
    avg, neighbors = get_avg_neighbor(rating_matrix) #Get neighbor list and average list
    
    with open(sys.argv[2], 'r') as tf, open(output, 'w') as f:
        while True:
            line = tf.readline().strip()
            if not line or len(line) == 0:
                break
            line = line.split('\t')
            prediction = estimate(int(line[0]), int(line[1]), rating_matrix, sim_matrix, avg, neighbors[int(line[0])])
            result = line[0] + '\t' + line[1] + '\t' + str(prediction) + '\n'
            f.write(result)
            
if __name__ == '__main__':
    rating_matrix = getData() #processing data into rating matrix
    sim_matrix = get_similarity(rating_matrix) #get similarity matrix
    predict(rating_matrix, sim_matrix) #To predict the rate of given users
