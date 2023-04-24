# from sentence_transformers import SentenceTransformer
import requests
import pinecone
import uuid
import os
import openai
from config import OPENAI,PINECONE,PINECONE_REGION,HUGGINGFACE_KEY

openai.api_key = OPENAI

pinecone.init(api_key = PINECONE,
              environment=PINECONE_REGION)
# model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-mpnet-base-v2"
headers = {"Authorization": "Bearer "+HUGGINGFACE_KEY}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()



def get_ans(qustion):
    model_engine = "text-davinci-003"
    prompt = qustion

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response


def get_embaddings(sentences):
    output = query({
    "inputs": [sentences]
    })
    # print(output[0])
    return output[0]



def get_document(question,index_name,topk,threshhold):

    
    try:
      pinecone.create_index(index_name, dimension=768)
    except:
       print("index already created")
    index = pinecone.Index(index_name)
    
    emb=get_embaddings(question)
    try:
      query_response = index.query(
      top_k =topk,
      include_metadata=True,
      vector=emb,
      ) 
    except:
      return "Erro Occured"
    qus=[]
    ans_map=dict()
    # print(query_response)
    # scors=[]
    for i in query_response['matches']:
        try:
          qus.append(i['metadata']['question'])
          ans_map[i['metadata']['question']]=((i['metadata']['answer']),i['score'])
          # scors.append(i['score'])

        except:
           continue
    cnt=0
    result=[]
    for i  in ans_map.keys():
        cnt+=1
        # print(ans[i][1])
        if(ans_map[i][1]>=threshhold/100):
            result.append((i,ans_map[i][0],ans_map[i][1]))
           
    return result

def upload_documnt(question,index_name):
  # print("sdfsldkfjs")
  try:
      pinecone.create_index(index_name, dimension=768)
  except:
      print("index already created")
  index = pinecone.Index(index_name)
  
  emb=get_embaddings(question)
  answer=process_output(get_ans(question))
  try:
    upsert_response = index.upsert(
    vectors=[
        {'id': str(uuid.uuid4()), "values":emb, "metadata": {'answer': answer,'question':question}},
        ]
    )
  except:
    return "Error Occured"
  return answer

def process_output(ans:str):
  if(ans.lower().find('security')!=-1):
     return "be careful before using this code!" +"/n" +ans
   
  return ans
  

def check_input(qus:str):
  if(len(qus.split())>500):
    return False
   
  return True