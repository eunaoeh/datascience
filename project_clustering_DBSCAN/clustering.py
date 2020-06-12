import sys
import numpy as np

# Open File
def parse():
    obj = []
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        obj = [ list(line.strip().split('\t')) for line in lines ]
    return obj

# Check neighbor
def check_core(obj, objects):
    Eps = int(sys.argv[3])
    x = float(obj[1])
    y = float(obj[2])
    neighbor = []
    for i in range(len(objects)):
        nx = float(objects[i][1])
        ny = float(objects[i][2])
        # If the distance is less than eps, add this point as a neighbor
        if np.sqrt(np.square(nx-x)+np.square(ny-y)) <= Eps:
            neighbor.append(objects[i])
    return neighbor
    
# Create Cluster
def clustering(objects):
    MinPts = int(sys.argv[4])
    visited = [False]*(len(objects))
    cluster = []
    cid = 0
    for obj in objects:
        pid = int(obj[0])
        # If visited, Check a next point
        if visited[pid] == True:
            continue
        # If not visitied, Check whether it is a core point or not
        neighbor = check_core(obj, objects)
        
        if len(neighbor) >= MinPts:
            # Core point
            # Create a new cluster
            cluster.append([])
            
            while True:
                # If no more points, stop increasing the cluster
                if len(neighbor) == 0:
                    break
                n_pts = neighbor.pop()
                #print(n_pts)
                n_pid = int(n_pts[0])

                # If visited, check a next point
                if visited[n_pid] == True:
                    continue
                visited[n_pid] = True
                
                cluster[cid].append(n_pid)
                
                tmp = check_core(n_pts, objects)
                if len(tmp) >= MinPts:
                    neighbor += tmp
                
            cid += 1
        else:
            # Border Point
            visited[pid] = True
    # Sort according to cluster's size
    # To easily get n clusters as a result
    cluster.sort(key=len, reverse=True)
    return cluster

# Save result
def write(cluster):
    n = int(sys.argv[2])
    idx = sys.argv[1].find(".txt")
    input_file = sys.argv[1][:idx]
    # Get only N elements
    for i in range(n):
        with open(input_file+'_cluster_'+str(i)+'.txt', 'w') as f:
            for obj in cluster[i]:
                f.write(str(obj)+'\n')
        
        
if __name__ == '__main__':
    cluster = clustering(parse())
    write(cluster)
