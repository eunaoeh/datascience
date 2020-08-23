import sys
import itertools
import copy

def apriori(transaction, minSup):
    total_trans = len(transaction)
    minSup = (minSup/100)*total_trans #save minimum support as a number
    line = '' # to save result

    C = set() # candidate
    L = set() # FP
    k = 1
    
    # C1 for k = 1
    for trx in transaction:
        for item in trx:
            if item not in C:
                C.add(item)
    C = sorted(C)
    #print('1st C:', C)

    # L1 for k = 1
    for c in C:
        if getSupport([c], transaction) >= minSup:
            L.add(c)
    #print('1st L:', L)
    L = sorted(L)
    
    # k >= 2
    while True:
        k += 1
        previous_L = copy.deepcopy(L)
        # do self joining first to get k+1 candidates
        C = selfJoin(L, k) #return tuples in set
        #print(k,'st Join:', C)
        # do pruninig after self joining
        C = prune(C, previous_L, k) #return as tuple in set
        #print(k,'st Prune:', C) #return tuples in set
        # check minimum support
        L = testSupport(C, minSup, transaction)
        #print(k, 'st FP:', L)

        # if there is no more FP, stop apriori algorithm
        if not L: 
            break
        else:
            # if there is a FP, apply associative rule 
            line += associationRule(L, k, minSup, total_trans, transaction)
    return line
        
def selfJoin(C, k):
    joined_C = []
    
    for itemset in C:
        if k == 2:
            itemset = [itemset]
        for item in itemset:
            if item not in joined_C:
                #print(item)
                joined_C.append(item)
    joined_C = set((itertools.combinations(sorted(joined_C), k)))

    return joined_C

def prune(C, previous_L, k):
    pruned_C = copy.deepcopy(C)
    
    for itemset in C:
        comb = set(itertools.combinations(sorted(itemset), k-1))

        if k == 2:
            for item in comb:
                if not set(item).issubset(previous_L):
                    pruned_C.remove(itemset)
                    break
        else:
            for item in comb:
                #print(item, previous_L)
                if not set((item,)).issubset(previous_L):
                    pruned_C.remove(itemset)
                    break
        
    return pruned_C

# function to check its support whether it is higher than minimum support or not
def testSupport(itemset, minSup, transaction):
    C = copy.deepcopy(itemset) #save whole itemset first

    for item in itemset:
        if getSupport(item, transaction) < minSup:
            C.remove(item) #if its support is lower than minimum, remove it
    return C
    
# function to get support of an item
def getSupport(item, transaction):
    cnt = 0
    for trx in transaction:
        if set(item).issubset(set(trx)):
            cnt += 1
            
    return cnt


def associationRule(L, k, minSup, total, transaction):
    line = "" #variable to save result
    tmp = k #to save k
    
    for itemset in L:    
        while k > 1:
            comb = list(itertools.combinations(itemset, k-1)) #find the combinations of FP
            #print(itemset, comb)
            for item in comb:
                #print(item)
                a = set(item) # an item
                b = set(itemset) - a #find another part of the set
                cnt = 0 # to find appearance of item to find confidence
                for trx in transaction:
                    if a.issubset(set(trx)):
                        cnt += 1
                support = getSupport(itemset, transaction) #find the number of appearance
                confidence = (support/cnt)*100 #find percentage of confidence
                support = (support/total)*100 #find percentage of support

                line += str(a)+'\t'+str(b)+'\t'+str('%.2f'%round(support,2))+'\t'+str('%.2f'%round(confidence, 2))+'\n'
            k -= 1 #keep repeating the procedure to find all subsets
        k = tmp
        
    return line

def openfile(file):
    f = open(file, 'r')
    arr = list()
    arr2 = list()
    while True:
        line = f.readline().strip()
        if not line: break
        # save give transactions as an integer
        arr.append(sorted(map(int, line.split('\t')))) 
    f.close()
    return arr

def writefile(file, result):
    f = open(file, 'w')
    f.write(result)
    f.close()
    
if __name__ == '__main__':
    minSup = int(sys.argv[1])
    file = sys.argv[2]
    output = sys.argv[3]
    transaction = openfile(file)
    result = apriori(transaction, minSup)
    writefile(output, result)
