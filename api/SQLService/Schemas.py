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
class setupParams(BaseModel):
    fileList: List[FileListModel]
    generType: str

# 生成文档的参数（软著）
class softDocParams(BaseModel):
    itemBack: str = Field(..., alias="项目背景")
    itemGoal: str = Field(..., alias="项目研发的目的和意义")

    itemMain: str = Field(..., alias="项目主要内容")

    techKey: str = Field(..., alias="关键技术")
    techNew: str = Field(..., alias="技术创新点")
    techIndex: str = Field(..., alias="技术指标")
    techLogic: str = Field(..., alias="总体逻辑结构设计")
    techRouter: str = Field(..., alias="采用的技术路线")

    market: str = Field(..., alias="市场调研")
    RDbase: str = Field(..., alias="研发基础")

    benefit: str = Field(..., alias="效益分析")
    risk: str = Field(..., alias="风险分析")

    companyName:str=Field(..., alias="公司名称")

# 生成文档的参数（专利）
class pantentDocParams(BaseModel):
    itemOverview: str = Field(..., alias="项目概述")
    itemGoal: str = Field(..., alias="立项目的")

    techKey: str = Field(..., alias="关键技术")
    techNew: str = Field(..., alias="技术创新点")
    put: str = Field(..., alias="实施方案")

    yet: str = Field(..., alias="已取得的工作进展")
    next: str = Field(..., alias="下一步研究计划和任务")
    done: str = Field(..., alias="项目完成情况")

    companyName: str = Field(..., alias="公司名称")
