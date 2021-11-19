
# coding: utf-8

# In[31]:


import pandas as pd
import os
import shutil


# In[32]:


#create the data for positive samples(github)

FILE_PATH = "E:\sem7\INT248\metadata.csv"
IMAGES_PATH = "E:\sem7\INT248\images"


# In[33]:


df = pd.read_csv(FILE_PATH)
print(df.shape)


# In[34]:


df.head()


# In[36]:


TARGET_DIR = "Desktop/Dataset/covid"

if not os.path.exists(TARGET_DIR):
    os.mkdir(TARGET_DIR)
    print("covid folder created")


# In[37]:


cnt = 0

for (i,row) in df.iterrows():
    if row["finding"]=="Pneumonia/Viral/COVID-19" and row["view"]=="PA":
        filename = row["filename"]
        image_path = os.path.join(IMAGES_PATH,filename)
        image_copy_path = os.path.join(TARGET_DIR,filename)
        shutil.copy2(image_path,image_copy_path)
        #print("moving image", cnt)
        cnt += 1
        
print(cnt)


# In[38]:


#sampling of images from kaggle

import random
KAGGLE_FILE_PATH = "Desktop/chestxray/NORMAL"
TARGET_NORMAL_DIR = "Dataset/Normal"


# In[39]:


image_names = os.listdir(KAGGLE_FILE_PATH)


# In[40]:


random.shuffle(image_names)


# In[42]:


for i in range(196):
    image_name = image_names[i]
    image_path = os.path.join(KAGGLE_FILE_PATH,image_name)
    
    target_path = os.path.join(TARGET_NORMAL_DIR,image_name)
    
    shutil.copy2(image_path,target_path)
    print("copying image",i)

