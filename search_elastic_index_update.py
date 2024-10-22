import os
from pathlib import Path
#import numpy as np
from transformers import AutoTokenizer, AutoModel
from elasticsearch import Elasticsearch
import torch
import shutil
import pandas as pd 

print("Running code to build Elastic index")
es = Elasticsearch("http://host.docker.internal:9200")

# Check if Elasticsearch is reachable
if es.ping():
    print("Successfully connected to Elasticsearch")
else:
    print("Elasticsearch connection failed")
    
    

def rename_rmd_to_md(folder_path):
    # Use Path from pathlib to manage paths
    folder = Path(folder_path)
    # Create a dictionary to store subfolder names and file contents
    file_data = {}
    # Get all .md files from subfolders recursively
    rmd_files = [str(f) for f in folder.glob('**/*.Rmd')]

    #print(rmd_files)
    for rmd_file in rmd_files:
        print(rmd_file)
        # Create the new filename by replacing .Rmd with .md
        md_file = rmd_file.replace('.Rmd', '.md')

        # Check if the .md file already exists
        if not os.path.exists(md_file):
            # Copy the .Rmd file to .md
            shutil.copy(rmd_file, md_file)
            print(f'Copied {rmd_file} to {md_file}')
        else:
            print(f'{md_file} already exists. Skipping.')
    return
    


def read_md_files_from_subfolders(folder_path):
    # Use Path from pathlib to manage paths
    folder = Path(folder_path)

    # Create a dictionary to store subfolder names and file contents
    file_data = {}

    # Get all .md files from subfolders recursively
    md_files = folder.glob('**/*.md')

    # Iterate through each file and read content
    for md_file in md_files:
        try:
            # Extract the subfolder name
            subfolder = md_file.parent.name
            folder_name = md_file.parent.parent.name
            
            # Open and read the .md file
            with open(md_file, 'r', encoding='utf-8') as file:
                content = file.read()

#                 # Store the content under the subfolder key
#                 if subfolder not in file_data:
#                     file_data[subfolder] = []

#                 # Append a tuple (filename, content) to the subfolder entry
#                 file_data[subfolder].append((md_file.name, content))
                
                
                # Store the content under the subfolder key
                if folder_name not in file_data:
                    file_data[folder_name] = []

                # Append a tuple (filename, content) to the subfolder entry
                file_data[folder_name].append((md_file.name, content))
                

        except Exception as e:
            print(f"Could not read {md_file}: {e}")

    return file_data



rename_rmd_to_md('./sources/') # rename .Rmd files to .md
file_data = read_md_files_from_subfolders('./sources/')

# Display the results
for subfolder, files in file_data.items():
    print(f"Subfolder: {subfolder}")
    for file_name, content in files:
        try:
            print(f"  File: {file_name}, Content: {content[5]}...")  # Display first 100 characters for brevity
        except:
            print("error for - {}".format(file_name))
            
            
doc_list = []
for subfolder, files in file_data.items():
    for file_name, content in files:
        temp_dict = {
        'package_name': subfolder,
        'file_name': file_name,
        'content': content
        }
    
        # Append the dictionary to the list
        doc_list.append(temp_dict)
        
        
        
mapping = {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": 'true',
            "similarity": "cosine",
          },
               
     "filename": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "content": {
        "type": "text",
        "analyzer": "standard"
      },
        
    "package_name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 768
          }
        }
      }
        
        }

    
    
  }

# Create an index with the defined mapping
try:
    es.indices.create(index='embedding_index_demo_include_vignette', body={'mappings': mapping})
except:
    pass

# # Load the BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('distilbert/distilbert-base-uncased')
model = AutoModel.from_pretrained('distilbert/distilbert-base-uncased')

# Generate embeddings for the documents using BERT

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

for idx, doc in enumerate(doc_list):
    print("Percentage complete : {}".format(round(100*(idx/len(doc_list)),2)))
    text = doc['content']
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    print("tokenization complete")
    with torch.no_grad():
        
        output = model(**inputs,).last_hidden_state.mean(dim=1).squeeze(0).numpy()
        doc['embedding'] = output.tolist()
        
for doc in doc_list:  
    es.index(index='embedding_index_demo_include_vignette', body=doc)
    
    
temp_df = pd.DataFrame(doc_list)
temp_df.to_csv('./embedding_df_with_vignette.csv', index= False)

print("---------- Indexing completed --------------")