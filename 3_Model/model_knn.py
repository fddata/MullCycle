from sklearn.neighbors import KNeighborsClassifier 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd  
from sklearn import preprocessing  
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
  
  
 # read in csv and filter data on the subset we want
csv_loc = 'C:\\Users\\Samsung\\Desktop\\Programs\\Python\\mull_cycle\\3_Model\\df_mf.csv'
df = pd.read_csv(csv_loc, index_col=0)
df = df[df.gender == 'M'] 
df = df[['age', 'time','course']].dropna(subset = ["age"])


# Split into training and test set  and do your labels
train=df.sample(frac=0.8,random_state=999) 
test=df.drop(train.index)
  
labelEnc = preprocessing.LabelEncoder()

X_prime = np.array(map(list, zip(df.age, df.time)))
X_train =   np.array(map(list, zip(train.age, train.time)))
X_test =  np.array(map(list, zip(test.age, test.time)))

y_train = labelEnc.fit_transform(train['course'])
y_test = labelEnc.fit_transform(test['course'])
y_prime = labelEnc.fit_transform(df['course'])


#==============================================================================
#Testing accuracy code
#==============================================================================

neighbors = np.arange(1, 100) 
train_accuracy = np.empty(len(neighbors)) 
test_accuracy = np.empty(len(neighbors)) 
  
# Loop over K values 
for i, k in enumerate(neighbors): 
    knn = KNeighborsClassifier(n_neighbors=k) 
    knn.fit(X_train, y_train) 
      
    # Compute traning and test data accuracy 
    train_accuracy[i] = knn.score(X_train, y_train) 
    test_accuracy[i] = knn.score(X_test, y_test) 
  
# Generate plot 
plt.plot(neighbors, test_accuracy, label = 'Testing dataset Accuracy') 
plt.plot(neighbors, train_accuracy, label = 'Training dataset Accuracy') 
  
plt.legend() 
plt.xlabel('n_neighbors') 
plt.ylabel('Accuracy') 
plt.show() 





#==============================================================================
#plotting decision boundaries
#==============================================================================
"""
n_neighbors=3

#knn = KNeighborsClassifier(n_neighbors) 
#knn.fit(X_train, y_train) 

clf = KNeighborsClassifier(n_neighbors)
clf.fit(X_train, y_train)

# declare axes and step size
X = X_prime
y = y_prime
h = 0.2

# Plot the decision boundary and assign a color to each point in the mesh.
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
cmap_bold  = ListedColormap(['#FF0000', '#0000FF'])
Z = Z.reshape(xx.shape)
fig = plt.figure()
plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

# Plot the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=20)   
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())


#build the legend
long_course = mpatches.Patch(color='red', label='Long')
short_course = mpatches.Patch(color='blue', label='Short')
plt.legend(handles=[long_course, short_course])
plt.xlabel('Age') 
plt.ylabel('Finishing Time (hrs)') 
plt.title("Course length decision boundary for Age and finishing time, K = %i" % (n_neighbors))
plt.show()

"""


#==============================================================================
#   testing specific values
#==============================================================================
"""
knn = KNeighborsClassifier(n_neighbors=3)    
knn.fit(X_prime, y_prime)

prediction1 = knn.predict([50,5]) # 50 y/o, 5 hours
prediction2 = knn.predict([50,4.5]) # 50 y/o, 4.5 hours

print(prediction1) 
# returns [0] (long course)
print(prediction2)
# returns [1] (short course)

"""




