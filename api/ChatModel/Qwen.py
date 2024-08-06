from openai import OpenAI
from pathlib import Path
from fastapi import HTTPException

# token-----------------------------------------------------------------------------------------------------------------------------------------------------------
client = OpenAI(
    api_key="sk-cacc5d644acb4810949926aebd246374",  # 替换成真实DashScope的API_KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务endpoint
)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# 去除markdown语法
def removeMark(text):
    remove_chars = ["#", "**", "- "]
    for char in remove_chars:
        text = text.replace(char, "")

    return text

# 基本对话
def chat(messages:list,model: str = "qwen-long"):
    #temperature:float,top_p:float,

    completion = client.chat.completions.create(
        messages=messages,
        model=model
        # temperature=temperature,
        # top_p=top_p,
    )
    return removeMark(completion.choices[0].message.content)

        # return str(e)

# -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件

# 上传文件返回文件id
def upFile(file_path):
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    return file_object.id

# 根据文件id解析文档
def analyFile(file_id):
    pass

# 列出所有上传的文档
def getAllFile():
    pass

# 根据id删除文档
def delFile(file_id):
    pass
if __name__ == "__main__":
    print(getAllFile())