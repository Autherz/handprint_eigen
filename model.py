# ref : https://github.com/vutsalsinghal/EigenFace/blob/master/Face%20Recognition.ipynb
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imread
from PIL import Image
import cv2
# import images // #resize // # createDataframe image
dataset_path = "PCA_based Fingerprint Recognition System/TrainDatabase/"
dataset_dir = os.listdir(dataset_path)

test_path = "PCA_based Fingerprint Recognition System/TestDatabase/"
test_dir = os.listdir(test_path)

width = 512
height = 512

training_tensor = np.ndarray(shape=(len(dataset_dir), height*width), dtype=np.float64)
testing_tensor   = np.ndarray(shape=(len(test_dir), height*width), dtype=np.float64)

for i in range(len(dataset_dir)):
    #img = plt.imread(dataset_path + dataset_dir[i])
    img = Image.open(dataset_path + str((i+1)) +'.jpg')
    img = img.resize((512, 512))
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    training_tensor[i, :] = np.array(img, dtype='float64').flatten()

for i in range(len(test_dir)):
    img = Image.open(test_path + str((i+1)) +'.jpg')
    img = img.resize((512, 512))
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    testing_tensor[i, :] = np.array(img, dtype='float64').flatten()

print("tranining shape : ", training_tensor.shape)
print(type(dataset_dir))

print("Testing shape : ", testing_tensor.shape)

# eigenfaceCore
## Mean
mean_face = np.zeros((1, height*width))
for i in training_tensor:
    mean_face = np.add(mean_face, i)

mean_face = np.divide(mean_face, float(len(dataset_dir))).flatten()
print("Shape of mean face : ", mean_face.shape)

## Calculating the deviation of each image from mean image
## Normalised faces
normalised_training_tensor = np.ndarray(shape=(len(dataset_dir), height*width))

for i in range(len(dataset_dir)):
    normalised_training_tensor[i] = np.subtract(training_tensor[i], mean_face)

print("Shape of normalize face : ", normalised_training_tensor.shape)   

## Convariance matrix
cov_matrix = np.cov(normalised_training_tensor)
cov_matrix = np.divide(cov_matrix, float(len(dataset_dir))) # L 

eigenvalues, eigenvectors, = np.linalg.eig(cov_matrix) # [V, D] = eig(L)

eig_pairs = [(eigenvalues[index], eigenvectors[:,index]) for index in range(len(eigenvalues))]
# Sort the eigen pairs in descending order:
eig_pairs.sort(reverse=True)
eigvalues_sort  = [eig_pairs[index][0] for index in range(len(eigenvalues))]
eigvectors_sort = [eig_pairs[index][1] for index in range(len(eigenvalues))]


# *******************************************************
# Find cumulative variance of each principle component
var_comp_sum = np.cumsum(eigvalues_sort)/sum(eigvalues_sort)
# print("Cumulative proportion of variance explained vector: \n%s" %var_comp_sum)
num_comp = range(1,len(eigvalues_sort)+1)
plt.title('Cum. Prop. Variance Explain and Components Kept')
plt.xlabel('Principal Components')
plt.ylabel('Cum. Prop. Variance Expalined')
plt.scatter(num_comp, var_comp_sum)
# plt.show()
# *****************************End ***********************


# Eigen Face or Projected Data
## PCA 
reduced_data = np.array(eigvectors_sort[:50]).transpose()
proj_data = np.dot(training_tensor.transpose(),reduced_data)
proj_data = proj_data.transpose()

# Finding weights for each traning image
w = np.array([np.dot(proj_data,i) for i in normalised_training_tensor])
print(w.shape)
# recognition

count = 0
def recogniser(img):
    global count
    
    normalised_uface_vector = np.subtract(img, mean_face)
    w_unknown = np.dot(proj_data, normalised_uface_vector )
    
    diff = w - w_unknown
    norms = np.linalg.norm(diff, axis=1)
    index = np.argmin(norms)
    min_norm = min(norms)
    max_norm = max(norms)

    if norms[index] < max_norm:
        print("Matched!")
    else:
        print("Not Matched!")

    return index

def recogniser_str(img):
    global count
    img = Image.open(img)
    img = img.resize((512, 512))
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.array(img, dtype='float64').flatten()

    normalised_uface_vector = np.subtract(img, mean_face)
    w_unknown = np.dot(proj_data, normalised_uface_vector )
    
    diff = w - w_unknown
    norms = np.linalg.norm(diff, axis=1)
    index = np.argmin(norms)
    min_norm = min(norms)
    max_norm = max(norms)

    if norms[index] < max_norm:
        print("Matched!")
    else:
        print("Not Matched!")

    return index, norms[index]

# recogniser(testing_tensor[1, :], dataset_dir, proj_data, w)


