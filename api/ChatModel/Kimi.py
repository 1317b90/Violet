from openai import OpenAI
from pathlib import Path
from fastapi import HTTPException

# token-----------------------------------------------------------------------------------------------------------------------------------------------------------
client = OpenAI(
    api_key="sk-oNrZtxRJbGBDZof8FzEvaQAjUNBc4fWLF0IhcqNIeQHI1D6B",
    base_url="https://api.moonshot.cn/v1",
)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# 基本对话
def chat(messages:list,model: str = "moonshot-v1-8k",temperature:float=0.3,top_p:float=1.0):
    try:
        completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            top_p=top_p
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件 -------- 文件

# 上传文件返回文件id
def upFile(file_path):
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    return file_object.id

# 根据文件id解析文档
def analyFile(file_id):
    return client.files.content(file_id=file_id).text

# 列出所有上传的文档
def getAllFile():
    file_list = client.files.list()
    return file_list.data

# 根据id删除文档
def delFile(file_id):
    try:
        client.files.delete(file_id=file_id)
        return "删除成功！"
    except Exception as e:
        return "删除失败"+str(e)

if __name__ == "__main__":
    print(getAllFile())