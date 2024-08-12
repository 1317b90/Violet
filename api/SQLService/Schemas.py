from datetime import datetime

from pydantic import BaseModel, conint, constr, condecimal, Field
from typing import Optional,Union as TypingUnion,List,Dict,Union


# --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表 --------- 用户表

# 一般用户
class User(BaseModel):
    username:str

# 登录用户
class LoginUser(BaseModel):
    username:str
    password:str



# -------- 项目表 -------- 项目表 -------- 项目表 -------- 项目表 -------- 项目表 -------- 项目表 -------- 项目表 -------- 项目表
class Item(BaseModel):
    id: int
    username: str
    itemName: str
    companyName: str
    companyTime: datetime
    companyMoney: int
    companyScope: str
    companyIntro: str
    creationTime: datetime


# 项目中的公司基本资料
class ItemCompany(BaseModel):
    id: int
    companyName: str
    companyTime: datetime
    companyMoney: int
    companyScope: str
    companyIntro: str
    companyFile: str

# 记录表----------
class Log(BaseModel):
    username: str
    type: str
    input: Optional[Union[dict, list]]
    output: str
    state: bool
    time: datetime



# ----------------------------------------------------------------

class Raw(BaseModel):
    uid: Optional[int] = None

class FileListModel(BaseModel):
    name: Optional[str] = None
    percentage: Optional[int] = None
    status: Optional[str] = None
    size: Optional[int] = None
    raw: Optional[Raw] = None
    uid: Optional[int] = None
    response: str

# 生成内容接收的接口
class itemSetupParams(BaseModel):
    fileList: List[FileListModel]
    generType: str

# 接收生成内容
class GenerModel(BaseModel):
    xxx1x: str = Field(..., alias="项目背景")
    xxx2x: str = Field(..., alias="项目研发的目的和意义")
    xxx3x: str = Field(..., alias="项目主要内容")
    xxx4x: str = Field(..., alias="关键技术")
    xxx5x: str = Field(..., alias="技术创新点")
    xxx6x: str = Field(..., alias="技术指标")
    xxx7x: str = Field(..., alias="总体逻辑结构设计")
    xxx8x: str = Field(..., alias="采用的技术路线")
    xxx9x: str = Field(..., alias="市场调研")
    xxx10x: str = Field(..., alias="研发基础")
    xxx11x: str = Field(..., alias="效益分析")
    xxx12x: str = Field(..., alias="风险分析")
