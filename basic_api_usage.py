import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # 读取本地.env文件

openai.api_key = os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message["content"]

def get_completion_and_token_count(messages,
                                   model='gpt-3.5-turbo',
                                   temperature=0,
                                   max_token=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_token,
    )

    content = response.choices[0].message["content"]

    token_dict = {
        'prompt_tokens':response['usage']['prompt_tokens'],
        'completion_tokens':response['usage']['completion_tokens'],
        'total_tokens':response['usage']['total_tokens'],    
    }

    return content, token_dict

def moderation(messages):
    # 分析用户输入是否和暴力/色情/仇恨相关
    response = openai.Moderation.create(
        input=messages
    )
    return response["results"][0]