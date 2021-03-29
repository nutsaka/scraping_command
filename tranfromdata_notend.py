

import pandas as pd

#input your file name
print("Enter your file name:")
file_name = input()

print(file_name)
#import data
data = pd.read_csv(file_name)
print(data)
#process data
#process data
first = data.iloc[:,0].dropna()
data_s = data.iloc[:,0:2]
g = {}
j = 0
for i in range(len(data_s.iloc[:,1])):
    if(data_s.iloc[:,0].isna()[i] == False):
        j = 0
        if j not in g:
            g[j] = []
        g[j].append(data.iloc[:,1][i])
    else:
        j = j + 1
        if j not in g:
            g[j] = []
        g[j].append(data.iloc[:,1][i])
left_add = pd.DataFrame(g)
right_add = data.iloc[:,2:].dropna()
first = first.reset_index().iloc[:,1:]
left_add = left_add.reset_index().iloc[:,1:]
right_add = right_add.reset_index().iloc[:,1:]
data_new = pd.concat([first,left_add,right_add], axis=1)

#export data
data_new.to_csv('output_'+file_name,index=False)