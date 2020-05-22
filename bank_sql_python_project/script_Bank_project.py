#!/usr/bin/env python
# coding: utf-8

# ### Objectives
# * Clean the data and remove unknown values as much as possible.
# * our object is to move this clean data to mysql database using python.
# #### Steps
# * Import the data using pandas
# * clean the dataframe of null and unwanted values
# * create database and table in mysql
# #### Note:
# * Please refer to readme file for description of columns

# In[1]:


import pandas as pd
import numpy as np
import mysql.connector


# In[2]:


bank_data=pd.read_csv("bank.csv", sep=";")
bank_data.head()


# * We  have 45211 entries. First we will clean the data. Lets check the number of unknown values in each column

# In[4]:


column_list = list(bank_data.columns)   #List of columns in the dataframe
for column in column_list:
    bank_data_unknown=bank_data[bank_data[column]=='unknown']
    unknown_length=len(bank_data_unknown.index)

# * So we have 1857 unknown entries in education, 288 in jobs, 13020 qne 36959 unknown values in contact and poutcome respectively.
# 
# * now we will replace the unknown in education. we will see the most common education for each job role and replace the unknown values

# In[5]:


# Step 1: cleaning education column
job_list=list(bank_data.job.unique())
job_dict={}            #Dict of job roles and education
for jobs in job_list:
    education_as_per_job=bank_data[bank_data.job==jobs].education.value_counts().head(1).index
    job_dict[jobs]=education_as_per_job[0]


# In[6]:


def edu(jobs):
    if jobs.education=='unknown':
        return job_dict[jobs.job]
    else:
        return jobs.education
bank_data['education']=bank_data.apply(edu, axis=1)

# So all the unknown values of education is replaced depending on the job


# * More than 81% of data in poutcome is unknown. We will drop this column. Also this column won't provide much information
# * if some study was to be done in future as a large number of values are not known, this will effect the outcome
# * We will also remove the rows where all three of job, education and contact is unknown

# In[7]:


#Step 2: cleaning poutcome column and rows with lot of unknown values
bank_data.drop(columns=['poutcome'], inplace=True)


bank_unknown_index=list(bank_data[(bank_data.job=='unknown') & (bank_data.education=='unknown') & (bank_data.contact=='unknown')].index)
bank_data.drop(index=bank_unknown_index, inplace=True)

# In[8]:


# Step 3: Cleaning contact columns. 
bank_data.contact.value_counts()


# * We still have 12966 unknown values for contact. We will fill these unknown values with the most occuring type
# * Clearly, about 90% of people have cellular phones, we can safely assume that the remaining unknown people will also have cellular phones

# In[9]:


bank_data.contact.replace({'unknown':'cellular'}, inplace=True)


# * we still have a few rows where both job and education is unknown. We will drop those rows as a clean data needs to be saved to sql

# In[10]:


drop_list=list(bank_data[(bank_data.job=='unknown') & (bank_data.education=='unknown')].index)
bank_data.drop(index=drop_list, inplace=True)


# In[ ]:


# We still have job colmn with unknown values. Since the data is so less compared to total entried, we can either fill this with most occuring value, or drop the row.
# as of now, we will let it be unknown


# ## Transfering data to SQL
# * Now we will move this dataframe to mysql. 
# * At present we will be using our local host. This can also be connected to any online database

# In[18]:


connecter=mysql.connector.connect(host="localhost", user="ashish", passwd='abcd')
cursor=connecter.cursor()


# In[ ]:


cursor.execute("CREATE DATABASE bank_project")


# In[20]:


cursor.execute("USE bank_project")
cursor.execute("DROP TABLE IF EXISTS data")
cursor.execute("""CREATE TABLE data (id INT AUTO_INCREMENT,
                  age INT,
                  job VARCHAR(20),
                  marital VARCHAR(20),
                  education VARCHAR(20),
                  defaults VARCHAR(20),
                  balance VARCHAR(20),
                  housing VARCHAR(20),
                  loan VARCHAR(20),
                  contact VARCHAR(20),
                  day INT,
                  month VARCHAR(20),
                  duration INT,
                  campaign INT,
                  pdays INT,
                  previous INT,
                  subcribed VARCHAR(10),
                  PRIMARY KEY (id))""")


# In[21]:


def insert_value(row):
        mySql_insert_query = """INSERT INTO data (age, job, marital, education, defaults, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, subcribed) 
                               VALUES 
                               (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        
        recordTuple = (int(row.age), row.job, row.marital, row.education, row.default, int(row.balance), row.housing, row.loan, row.contact, int(row.day), row.month, int(row.duration), int(row.campaign), int(row.pdays), int(row.previous), row.y)
                
        cursor.execute(mySql_insert_query, recordTuple)
        connecter.commit()
        return "row inserted"

bank_data["status"] = bank_data.apply(insert_value, axis=1)


# ### Checking if the data was inserted into mysql

# In[23]:


cursor.execute("SELECT * FROM data")

result = cursor.fetchall()

print("csv file exported to mysql successfully")

#Closing the connection
connecter.close()


# In[ ]:




