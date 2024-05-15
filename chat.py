import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import  sys
sys.path.append(r"D:\myproject\chat_llm")
from Query_classification import Neo4jQueryHandler
import pandas as pd
from snownlp import SnowNLP
import re


model_name_or_path = "./models/Shanghai_AI_Laboratory/internlm2-chat-1_8b"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True, device_map='cuda:0')
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True,torch_dtype=torch.bfloat16, device_map='cuda:0')
model = model.eval()

system_prompt = """你是一个海岛领域专家
"""

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:
    input_text = input("\nUser  >>> ")
    input_text = input_text.replace(' ', '')
    length = 0
    island = pd.read_excel('./data/island_name.xlsx')
    b_names = island['标准名称'].tolist()
    for response, _ in model.stream_chat(tokenizer, input_text, messages):
        input_text1 = f'判断问题"{input_text}"属于哪个问题,如果属于"询问海岛相关研究人员"相关的问题,返回1;如果属于"询问海岛的位置"相关的问题，则返回数字2。只返回问题类型对应的数字'
        response1, history = model.chat(tokenizer, input_text1, history=[])
        try:
            response2=re.findall(r'\d+', response1)[0]
        except:
            if "询问海岛相关研究人员" in response1:
                response2='1'
            elif "询问海岛的位置" in response1:
                response2='2'
            else:
                response2='3'


        if input_text == "exit":
            break
        if response2 == '1' or response2 == '2':
            # text, history = model.chat(tokenizer, '请提取海岛名称,有多个海岛时，用;隔开:'+input_text, history=[])

            text = []
            for name in b_names:
                if name in input_text:
                    text.append(name)
            text=text[0]
            Query = Neo4jQueryHandler("bolt://localhost:7687", "neo4j", "neo4j1234")
            results = Query.query_and_return(response2, text)
            input_text = '请结合答案提示(' +results + ')回答问题：' + input_text
        else:
            input_text='如果你能回答，请在回答后注明"不在数据库，仅有AI训练数据生成"；如果你不会，请委婉拒答。'+'问题为：'+input_text
        response, history = model.chat(tokenizer, input_text, history=[])
        if response is not None:
            print(response[length:], flush=True, end="")
            length = len(response)
