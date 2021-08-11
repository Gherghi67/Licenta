import os
import csv

os.getcwd()

collection1 = 'Dataset/with_mask'
collection2 = 'Dataset/without_mask'

with open('Dataset/labels.csv', mode = 'w') as labels_file:
    labels_writer = csv.writer(labels_file, delimiter = ',')

    for filename1, filename2 in zip(enumerate(os.listdir(collection1)), enumerate(os.listdir(collection2))):
        #print(filename1, filename2)
        
        labels_writer.writerow([os.path.splitext(filename1[1])[0], '1'])
        labels_writer.writerow([os.path.splitext(filename2[1])[0], '0'])


