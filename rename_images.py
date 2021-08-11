import os

os.getcwd()

collection = "Dataset/without_mask"

index = 5521

for filename in enumerate(os.listdir(collection)):
    os.rename(collection + "/" + filename[1], collection + "/" + str(index) + ".jpg")
    index = index + 1
    
