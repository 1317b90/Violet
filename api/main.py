import json
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from docx import Document
from ChatModel import Spark,Kimi,Qwen
from SqlService import Schemas
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

"""
               _oo0oo_
              o8888888o
              88" . "88
              (| -_- |)
              0\  =  /0
            ___/`---'\___
          .' \\|     |// '.
         / \\|||  :  |||// \
        / _||||| -:- |||||- \
       |   | \\\  -  /// |   |
       | \_|  ''\---/''  |_/ |
       \  .-\__  '-'  ___/-. /
     ___'. .'  /--.--\  `. .'___
  ."" '<  `.___\_<|>_/___.' >' "".
 | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 \  \ `_.   \_ __\ /__ _/   .-` /  /
=====`-.____`.___ \_____/___.-`___.-'=====
               `=---='


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       菩提本无树    明镜亦非台
       本来无BUG    何必常修改
"""


app = FastAPI(title='AI申请书API文档', description='🙏🙏🙏  愿天堂没有BUG')

app.mount("/Files", StaticFiles(directory="Files"), name="Files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权
@app.post("/IPadvanced", summary='先进性说明', tags=['知识产权'])
def IPadvanced(fileList:list[Schemas.FileListModel]):

    messages = [
        {"role": "system",
         "content": f"""
    #Role
    - 你是一个擅长帮企业分析汇总文档的企业技术员，可以帮助企业分析专利文件并输出知识产权的先进性说明
                 """}
    ]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
    )

    messages.append(
        {"role": "user",
         "content": f"""
根据文档内容，生成以下内容，400字以内：
-输出知识产权的先进核心关键技术特点，分点描述，总结出文档中的具体的关键技术实现并详细描述，不要列举功能，要体现功能背后的技术，不要超过5点，以“本知识产权”为开头

             """}
# 结合企业简介输出内容该知识产权对本企业主营产品（服务）核心技术的支持作用说明，不要分点描述，生成文本一段式，不出现具体的公司名称，以“公司”代替
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# IP RD关联表
@app.post("/IPRD", summary='IP RD关联表', tags=['知识产权'])
def IPRD(fileList:list[Schemas.FileListModel]):
    messages = [
        {"role": "system",
         "content": f"""
    #Role
    - 你是一名专业的高新技术材料撰写员，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮企业做知识产权和研发项目的梳理以及匹配
    ## Language
    - 中文
                 """}
    ]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
    )

    messages.append(
        {"role": "user",
         "content": f"""
## Workflow:
- 从用户上传的文档中获取知识产权的名称
- 分析知识产权名称的关键词，并把有关联性的归为一类研发活动，并编写相应的研发活动名称
- 输出编写的研发活动名称和对应的知识产权名称
- 以表格的形式按【研发活动名称-关联知识产权名称】输出

## Rules:
- 每个知识产权只能关联一个研发活动，但一个研发活动可以关联多个知识产权。
- 依据知识产权名称撰写研发活动名称，要符合要求且不能重复
- 直接输出最后的表格结果，不要其他文字内容
             """}
    )

    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------- 立项报告 -------- 立项报告 -------- 立项报告 -------- 立项报告 -------- 立项报告 -------- 立项报告 -------- 立项报告 -------- 立项报告

@app.post("/itemSetup", summary='立项报告', tags=['立项报告'])
def itemSetup(data:Schemas.itemSetupParams):
    messages = []

    for item in data.fileList:
        messages.append({
            "role": "system",
            "content": f'fileid://{item.response}',
        }
    )

    # 本地获取提示词
    with open("./Prompt/itemSetup.json", 'r', encoding='utf-8') as file:
        promptJson = json.load(file)

    messages.append(
        {"role": "user",
         "content": f"""
        # Role
        你是一名高新技术认定申请材料撰写专家，精通高新技术企业认定申请的材料撰写技巧，擅长撰写优质的研发活动立项报告书。
        ## Background
        - 研究开发活动是指，为获得科学与技术（不包括社会科学、艺术或人文学）新知识，创造性运用科学技术新知识，或实质性改进技术、产品（服务）、工艺而持续进行的具有明确目标的活动。
        - 近期这家企业要申报高新技术企业，需要撰写研究开发活动立项申请资料。
        ## Language
        - 中文
        ## Rules
        ### 撰写材料要依据用户提供的知识产权资料，贴合实际
        ### 数据详实：尽量使用数据来支持你的分析和观点，提高报告的说服力。
        ### 语言准确：用词要准确、严谨，避免使用模糊、含糊的词语。
        ### 文本风格要符合企业技术研发人员撰写技术材料风格，最大化消除机器痕迹，用词要丝滑，内容要具体详细、要接地气。
        ### 不要出现知识产权的具体名称。
        ### 直接给出具体内容，不需要开头论述和结尾总结（如“综上所述”、“结论”、“总结”）。
        ### 不用统计字数。
         """}
    )

    messages.append(
        {"role": "user",
     "content": promptJson[data.generType]}
    )

    return Qwen.chat(messages)


# 生成立项报告文档
@app.post("/generDoc", summary='效益与风险分析', tags=['立项报告'])
def generDoc(data: Schemas.GenerModel,request: Request):
    file1 = './Files/gener/mod.docx'
    ip=request.client.host
    ip=ip.replace('.', '')
    file2 = f'./Files/gener/项目研发立项报告{ip}.docx'
    # 复制并重命名文件
    shutil.copy(file1, file2)

    # 打开文档
    doc = Document(file2)

    # 便利所有输入数据
    for key, value in  data.model_dump().items():
        # 遍历所有段落
        for para in doc.paragraphs:
            if key in para.text:
                # 替换段落中的文本
                para.text = para.text.replace(key, value)

    # 保存修改后的文档
    doc.save(file2)

    fileurl="http://www.oliven.top:800"+file2[1:]
    xurl = "https://view.xdocin.com/view?src="+fileurl+"&saveable=true&title=项目研发立项报告"

    return xurl

# --------- 研发活动情况 --------- 研发活动情况 --------- 研发活动情况 --------- 研发活动情况 --------- 研发活动情况 --------- 研发活动情况
@app.post("/RDactive", summary='研发情况活动表', tags=['研发情况活动表'])
def RDactive(fileList:list[Schemas.FileListModel]):
    messages = []

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
    )

    messages.append(
        {"role": "user",
         "content": f"""
        #Role
        - 你是一名企业的技术部员工，十分擅长撰写研发活动情况表

        ##Background
        - 近期这家企业要申报高新技术和企业，要撰写申报材料中的研发活动情况表

        ##Language：中文

        ##Goal
        - 依据用户提供的研发活动立项报告、结题报告，项目关联的知识产权证书等文档，撰写研发活动情况表

        ##Rules
        ###撰写的材料要严格按照用户提供文档输出
        ###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹，不要出现函数名、变量名等代码细节
        ###输出内容包括：
        - 研发活动名称
        - 目的及组织实施方式（400字以内）：
        立项目的：按照用户提供的立项报告中的“立项背景与意义”进行改写
        组织实施方式：主要提供项目的立项开发时间，采用何种项目管理制度，项目人员组织情况，项目实施阶段与内容，项目实施总历程时间，项目结项日期等，以“本项目”为主语，没有提供的信息用**代替
        - 核心技术及创新点（400字以内）：
        核心技术：按照用户提供的立项报告中的“关键技术”进行改写，分点描述，最多5个，尽可能详细描述使用的核心技术，不要出现函数名、变量名等代码细节
        创新点：按照用户提供的立项报告中的“技术创新点”进行改写，分点描述，最多5个
        - 取得的阶段性成果（400字以内）：
        知识产权成果：根据用户上传的知识产权证书，描述获得的知识产权的数量，名称，登记号等。参考格式：“本项目取得了*项软件著作权，著作权名称：***，登记号：***”
        阶段性成果：
        1.日期：阶段性成果内容
        2.日期：阶段性成果内容
        3.......

        ##Example
        研发活动名称:CA互认平台软件开发
        目的及组织实施方式:
        立项目的：网融公司开发的CA互认平台软件，按照国家推进“互联网+政务服务”及政务信息化工程建设规划工作总体部署，紧紧围绕“数字政府”改革建设需要，构建全省统一身份认证中心，实现对互联网用户和政务人员的用户身份可信等级管理、账户全生命周期管理。为各地市和省有关部门政务服务平台及移动端提供统一身份认证服务，推进公共支撑一体化，促进政务服务跨地区、跨部门、跨层级协同办理，全城通办、就近能办、异地可办，服务效能大幅提升，为持续推进“放管服”改革、推动政府治理现代化提供强有力支撑。
        组织实施方式： 本项目于2016年1月4日开始立项开发，按照开发项目管理制度开展项目工作，项目负责人负责项目的统筹，项目工作组编制项目立项书并制定项目计划及进行项目费用预算。项目经过需求调研、系统架构设计、代码编写、功能模块实现、软件测试等过程，历经12个月的开发，于2016年12月31日完成。 |
        核心技术及创新点: 
        核心技术：
        1、围绕可信数字身份整合各种核验方式，创新应用云计算、大数据、移动互联网等新技术，建成网上统一身份认证体系，为市民及企业全流程网上办事提供基础支撑服务，提供覆盖线上服务、线下窗口，移动终端，PC终端，自动终端的电子签名、电子印章支撑服务。
        2、结合生物识别技术、电子营业执照技术、密码云服务技术，依托微信、支付宝、企业微信、钉钉等第三方互联网平台逐步发布更加人性化的SaaS服务，直接向市民及企业提供更加便捷的电子签名、电子印章服务。
        创新点：
        1、统一的CA接入、证书漫游服务。通过交叉互认平台，将实现省内5家CA机构、1家网银、1家跨境CA机构的互联互通，实现证书用户一证通行、全省漫游、统一认证。
        2、基于网银证书的实名身份认证服务。银行系统对个人用户有严格的全生命周期身份审核。
        3、可信站点证书服务。电子政务网站都部署可信站点证书（SSL证书）来保证用户账户登录安全、系统机密信息安全和站点可信可视化。 |
        取得的阶段性成果: 
        知识产权成果：本项目取得1项软件著作权，著作权名称：CA互认平台软件V5.0，登记号：2018SR126888；取得了1项高新技术产品认定证书，高新产品名称：CA互认平台软件V5.0，证书编号：201819809。
        阶段性成果：
        1、2016年2月，成立专门项目组，进行方案论证，需求分析；
        2、2016年4月，完成需求功能模块设计定稿及评审；
        3、2016年8月，完成系统功能模块设计与开发，编码实现产品功能及软件；
        4、2016年10月，完成系统测试及功能改进完善；
        5、2016年12月，完成产品定型，系统上线，项目验收。

        ##Skill
        -能够依据不同的领域公司的材料对内容做相应的变化

        ##Workflow
        - 让用户上传研发活动立项及结题报告，以及关联的专利编号和名称
        - 解析用户上传的内容，并捕捉研发活动情况表表格所需要的关键信息
        - 输出研发活动情况

        ##Initialization
        - 作为角色 <Role>, 严格遵守 <Rules>，按照<Workflow>进行工作
             """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------- 高新技术产品情况表 --------- 高新技术产品情况表 --------- 高新技术产品情况表 --------- 高新技术产品情况表 --------- 高新技术产品情况表
@app.post("/highTech", summary='高新技术产品情况表', tags=['高新技术产品情况表'])
def highTech(fileList:list[Schemas.FileListModel]):
    messages = [
        {"role": "system",
         "content": f"""
    #Role
    - 你是一名企业的技术部员工，十分擅长撰写高新技术产品情况表

    ##Background
    - 近期这家企业要申报高新技术和企业，要撰写申报材料中的高新技术产品情况表

    ##Language：中文

    ##Goal
    - 依据用户提供的高新技术产品文档，相关的知识产权证书（如有）等文档，撰写高新技术产品情况表

    ##Rules
    ###撰写的材料要严格按照用户提供文档输出
    ###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹
    ###输出内容包括：
- 关键技术及主要技术指标（400字左右）：
关键技术：分点描述，不超过3点，使用数字序号编号，从高新技术产品文档中总结出关键技术，不要出现具体的函数名、变量名等代码细节
主要技术指标：分点描述，不超过3点，使用数字序号编号，从高新技术产品文档中总结出主要技术指标，不要出现具体的函数名、变量名等代码细节
- 与同类产品（服务）的竞争优势 （400字左右）
分点描述，使用数字序号编号
结合文档的具体内容，从性能、成本、市场情况等方面进行说明
- 知识产权获得情况及其对产品（服务）在技术上发挥的支持作用（400字左右）：
仅提取上传文档中知识产权证书/高新技术产品证书，不要提取产品文档中的知识产权证书/高新技术产品证书
如果有知识产权证书/高新技术产品证书，则根据用户上传的证书，描述获得的知识产权/高新技术产品的数量，名称，登记号等。参考格式：“本项目取得了*项软件著作权/高新技术产品证书，著作权/产品名称：***，登记号：***”，然后再描述产品（服务）在技术上发挥的支持作用
如果没有知识产权证书/高新技术产品证书，则输出“本产品目前暂无授权知识产权证书”，并详细描述产品（服务）在技术上发挥的支持作用（400字左右）
    ##Skill
    -能够依据不同的领域公司的材料对内容做相应的变化


                 """}
    ]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
    )

    messages.append(
        {"role": "user",
         "content": f"""
- 解析用户的文档内容，并捕捉高新技术产品情况表表格所需要的关键信息
- 输出高新技术产品情况表
             """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------- 成果转化说明 --------- 成果转化说明 --------- 成果转化说明 --------- 成果转化说明 --------- 成果转化说明
@app.post("/achieve", summary='成果转化说明', tags=['成果转化说明'])
def achieve(fileList: list[Schemas.FileListModel]):
    messages = [ {"role": "system",
         "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写高新技术成果转化说明

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的高新技术成果转化说明

##Language：中文

##Goal
- 依据用户提供的产品采购合同，产品相关的使用文档，撰写高新技术成果转化说明
- 不要分点，输出文本段落，不要输出标题
- 不要输出文档名称
- 输出内容包括三段内容:
- 第一段：
开头：我公司的科技成果“***（从产品采购合同中获取，如果是高新技术服务类，合同中没有给出具体的科技成果名称，则从产品文档中总结获取）”......，
介绍科技成果的来源（企业自主研发等）
编写该产品的研发目的，可以从响应国家政策、市场需求、企业发展等角度撰写
介绍该研发成果的主要内容（从产品使用手册中获取）
- 第二段：
以“本项目”为主语，编写该科技成果的重要意义（400字左右）
- 第三段：
以“本项目”为主语，介绍该科技成果的研发情况，是否已完成各模块的开发，是否进行完整性测试，是否实现应用等。（400字左右）

##Rules
###撰写的材料要严格按照用户提供文档输出
###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹

##Skill
-能够依据不同的领域公司的材料对内容做相应的变化
             """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
- 解析用户的文档内容
- 撰写高新技术成果转化说明
             """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------- 企业创新能力评价 --------- 企业创新能力评价 --------- 企业创新能力评价 --------- 企业创新能力评价

# 知识产权对企业竞争力作用
@app.post("/IPcompetion", summary='知识产权对企业竞争力作用', tags=['企业创新能力评价'])
def IPcompetion(fileList: list[Schemas.FileListModel]):
    messages = [{"role": "system",
                 "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写企业创新能力评价

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的企业创新能力评价

##Language：中文

##Goal
- 依据用户提供的知识产权资料，撰写知识产权对企业竞争力作用
- 不要分点，输出文本段落，不要输出标题，不要输出公司和知识产权的具体名称
- 不要输出文档名称
- 总字数为500字左右
- 输出内容包括:
- 知识产权对企业竞争力的重要作用
- 企业对知识产权进行开发、管理、保护、运营等方面的做法
- 根据上传的知识产权证书，总结公司近三年的知识产权情况，包括授权的知识产权总数量，以及不同类型的知识产权数量，输出格式为“近三年，公司取得的授权的知识产权共*项，其中软件著作权共*项（如有），发明专利共*项（如有），实用新型专利共*项（如有），外观专利共*项（如有）”
- 根据知识产权资料和企业简介，描述这些知识产权对公司主营业务、主营产品的重要性和作用
- 编写公司在创新发展、技术进步等方面的具体做法和成果

##Rules
###撰写的材料要严格按照用户提供文档输出
###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹

##Skill
-能够依据不同的领域公司的材料对内容做相应的变化
                 """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
- 解析上传的文档内容
- 撰写知识产权对企业竞争力作用
                 """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 研究开发与技术创新管理组织情况
@app.post("/manage400", summary='研究开发与技术创新管理组织情况', tags=['企业创新能力评价'])
def manage400(fileList: list[Schemas.FileListModel]):
    messages = [ {"role": "system",
         "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写研究开发与技术创新管理组织情况，并熟悉企业的各项研发和管理制度。

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的研究开发与技术创新管理组织情况

##Language：中文
             """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
总结各文档的主要内容，按照文档生成企业研究开发与技术创新管理组织情况，字数为400字以内，涉及到具体的制度时应当使用书名号强调“《》”
             """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 科技成果转化情况
@app.post("/scienceAchieve", summary='科技成果转化情况', tags=['企业创新能力评价'])
def scienceAchieve(fileList: list[Schemas.FileListModel]):
    messages = [{"role": "system",
                 "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写企业科技成果转化情况

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的企业科技成果转化情况

##Language：中文

##Goal
- 依据用户提供的知识产权资料和科技成果转化资料，撰写企业科技成果转化情况
- 不要分点，输出文本段落，不要输出标题，不要输出公司和知识产权的具体名称
- 不要输出文档名称
- 总字数为400字左右
- 输出内容包括:
- 企业对技术创新的重视，采取的措施，包括制度、流程、激励措施等
- 根据上传的科技成果转化资料，提取出科技成果转化总数量，总结公司近三年的科技成果转化情况，输出格式为“近三年，公司取得的科技成果转化共*项”
- 根据上传的知识产权证书，提取出知识产权总数量，总结公司近三年的知识产权情况，包括授权的知识产权总数量，以及不同类型的知识产权数量，输出格式为“近三年，公司取得的授权的知识产权共*项，其中软件著作权共*项（如有），发明专利共*项（如有），实用新型专利共*项（如有），外观专利共*项（如有）”
- 根据知识产权和科技成果转化资料和企业简介，描述这些知识产权和科技成果转化对公司主营业务、主营产品的重要性和作用

##Rules
###撰写的材料要严格按照用户提供文档输出
###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹

##Skill
-能够依据不同的领域公司的材料对内容做相应的变化
                 """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
- 解析上传的文档内容
- 撰写知识产权对企业竞争力作用
                 """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 管理与科技人员
@app.post("/sciencePeople", summary='管理与科技人员', tags=['企业创新能力评价'])
def sciencePeople(fileList: list[Schemas.FileListModel]):
    messages = [{"role": "system",
                 "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写高新技术企业申报书

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的公司的管理与科技人员情况

##Language：中文

##Goal
- 依据用户提供的公司的管理与科技人员情况说明，按照要求撰写材料

##Rules
###撰写的材料要严格按照用户提供文档输出
###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹
##总字数400字以内，生成文本一段式，不要分点描述
###输出内容包括：
- 描述公司的职工总人数，学历构成，公司从事研发和相关技术的科技人员总数，占职工总数的比例，员工职称构成，研发人员专业分布情况，专业结构是否合理。
- 描述公司的研发场地、研发环境和研发设备等情况，以及研发投入情况，是否符合高新技术企业认定标准。
- 描述公司的经营管理团队，管理制度，管理理念，在高新技术领域的创新能力和水平以及优势
       
##Skill
-能够依据不同的领域公司的材料对内容做相应的变化
                 """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
- 解析用户上传的内容，分析这家公司的管理与科技人员情况
- 按照要求输出内容
                 """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------- 研究开发组织管理水平 --------- 研究开发组织管理水平 --------- 研究开发组织管理水平 --------- 研究开发组织管理水平
@app.post("/manage1000", summary='研究开发组织管理水平', tags=['研究开发组织管理水平'])
def manage1000(fileList: list[Schemas.FileListModel]):
    messages = [ {"role": "system",
         "content": f"""
#Role
- 你是一名企业的技术部员工，十分擅长撰写研究开发组织管理水平，并熟悉企业的各项研发和管理制度。

##Background
- 近期这家企业要申报高新技术和企业，要撰写申报材料中的研究开发组织管理水平

##Language：中文
             """}]

    for item in fileList:
        messages.append({
            "role": "system",
            "content": kimiAnalyFile(item.response),
        }
        )

    messages.append(
        {"role": "user",
         "content": f"""
总结各文档的主要内容，按照文档生成企业研究开发与技术创新管理组织情况，字数为1000字以内，涉及到具体的制度时应当使用书名号强调“《》”，按照以下5个方面进行描述：
1.研发项目管理制度方面（200字左右）
2.研发经费投入管理制度方面（200字左右）
3.产学研合作管理方面（200字左右）
4.研发中心及创新平台建设方面（200字左右）
5.科技人员激励及培训制度方面（200字左右）
             """}
    )
    try:
        return Qwen.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#
# ---------- Kimi ---------- Kimi ---------- Kimi ---------- Kimi ---------- Kimi ---------- Kimi ---------- Kimi ---------- Kimi

# 单轮对话
@app.get("/kimiChat", summary='单轮对话', tags=['Kimi'])
def sparkChat(question: str, model: str = "moonshot-v1-8k", temperature: float = 0.3, top_p: float = 1.0):
    """
    - question：对AI的提问
    - model：模型版本
        - moonshot-v1-8k: 它是一个长度为 8k 的模型，适用于生成短文本。 （默认）
        - moonshot-v1-32k: 它是一个长度为 32k 的模型，适用于生成长文本。
        - moonshot-v1-128k: 它是一个长度为 128k 的模型，适用于生成超长文本。
    """
    messages = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": question}
    ]

    return Kimi.chat(messages, model, temperature, top_p)


# 上传文件获取ID
@app.post("/kimiUpFile", summary='上传文档', tags=['Kimi'])
def kimiUpFile(file: UploadFile = File(...)):
    if file.content_type not in ["application/msword",
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 "application/pdf", "text/markdown", "text/plain"]:
        return "文件类型不符"

    if file.size > 30 * 1024 * 1024:
        return "文件过大"

    try:
        save_path = './test_files/' + file.filename

        # 将文件保存
        with open(save_path, 'wb') as f:
            for line in file.file:
                f.write(line)

        return Kimi.upFile(save_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 通过ID解析文档
@app.get("/kimiAnalyFile", summary='解析文档', tags=['Kimi'])
def kimiAnalyFile(fileID: str):
    return Kimi.analyFile(fileID)


# 查询所有文档
@app.get("/kimiAllFile", summary='查询所有文档', tags=['Kimi'])
def kimiAllFile():
    return Kimi.getAllFile()


# 根据id删除文档
@app.get("/kimiDelFile", summary='删除文档', tags=['Kimi'])
def kimiDelFile(fileID: str):
    return Kimi.delFile(fileID)


# --------- 通义千问 --------- 通义千问 --------- 通义千问 --------- 通义千问 --------- 通义千问 --------- 通义千问 --------- 通义千问

@app.get("/qwenChat", summary='单轮对话', tags=['Qwen'])
def qwenChat(question: str, model: str = "qwen-long", temperature: float = 0.3, top_p: float = 1.0):

    messages = [
        {"role": "system",
         "content": "你是一个好人"},
        {"role": "user", "content": question}
    ]

    return Qwen.chat(messages, model)

@app.post("/qwenUpFile", summary='上传文档', tags=['Qwen'])
def qwenUpFile(file: UploadFile = File(...)):
    # 获取主要的 MIME 类型，忽略 charset 部分
    main_content_type = file.content_type.split(';')[0]
    if main_content_type not in ["application/msword",
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 "application/pdf", "text/markdown", "text/plain"]:
        raise HTTPException(status_code=400, detail="文件类型不符")
    if file.size > 30 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件过大")

    save_path = './test_files/' + file.filename

    # 将文件保存
    with open(save_path, 'wb') as f:
        for line in file.file:
            f.write(line)

    return Qwen.upFile(save_path)


@app.post("/qwenFileChat", summary='文件对话 自带的', tags=['Qwen'])
def qwenFileChat(fileID:str):
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": f"fileid://{fileID}"},
        {"role": "user", "content": "请帮忙概括文件讲述了什么"},
    ]
    return Qwen.chat(messages)


# --------- 讯飞星火 --------- 讯飞星火 --------- 讯飞星火 --------- 讯飞星火 --------- 讯飞星火 --------- 讯飞星火 --------- 讯飞星火
@app.get("/sparkChat", summary='单轮对话', tags=['讯飞星火'])
def sparkChat(question: str, domain: str = "generalv3.5", temperature: float = 0.8, top_k: int = 5,
              max_tokens: int = 8192):
    """
    - question：对AI的提问
    - domain：模型版本
        - "generalv3.5"：Max版本（默认）
        - "generalv3"：Pro版本
        - "general"：Lite版本
    - temperature：
    - top_k：
    - max_tokens：
    """
    question = [{"role": "user", "content": question}]
    return Spark.chat(domain, question, temperature, top_k, max_tokens)


@app.get("/sparkDocFileID", summary='文档对话（FileID）', tags=['讯飞星火'])
def sparkDocFileID(
        wikiPromptTpl: str = "请将以下内容作为已知信息：\n<wikicontent>\n请根据以上内容回答用户的问题。\n问题:<wikiquestion>\n回答:",
        fileIds: str = "89994307b1ff4707b878a99485f360aa",
        question: str = "请生成该文档中的先进性说明，主要输出知识产权的先进核心关键技术特点，以“本知识产权”为开头，不要小标题，不要分段，不要出现“首先”，“其次”，“此外”，“最后”,“综上所述”等字眼请生成该文档中的先进性说明，主要输出知识产权的先进核心关键技术特点，以“本知识产权”为开头，不要小标题，不要分段，不要出现“首先”，“其次”，“此外”，“最后”,“综上所述”等字眼",
        wikiFilterScore: float = 0.8,
        temperature: float = 0.5,
        sparkWhenWithoutEmbedding: bool = False):
    """
    - wikiPromptTpl：wiki 大模型问答模板
    - fileIds：文档的id
        - eg:"89994307b1ff4707b878a99485f360aa"
    - question: 对AI的提问
        - eg:'请生成该文档中的先进性说明，主要输出知识产权的先进核心关键技术特点，以“本知识产权”为开头，不要小标题，不要分段，不要出现“首先”，“其次”，“此外”，“最后”,“综上所述”等字眼'
    - wikiFilterScore: wiki 结果分数阈值，低于这个阈值的结果丢弃。取值范围为(0,1] 参考值为：0.80非常宽松 0.82宽松 0.83标准0.84严格 0.86非常严格。
    - temperature: 大模型问答时的温度，取值 0-1，temperature 越大，大模型回答随机度越高
    - sparkWhenWithoutEmbedding: 用户问题未匹配到文档内容时，是否使用大模型兜底回答问题
    """

    return Spark.doc_chat(wikiPromptTpl, fileIds, question, wikiFilterScore, temperature, sparkWhenWithoutEmbedding)
