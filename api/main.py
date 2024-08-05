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

# 2 填写企业注册登记表
# 2.1 输入企业名字，爬取相关信息并填入模板表格中


# 3. --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权 --------- 知识产权

# 3.1 知识产权汇总表

# 3.2 知识产权明细表
@app.get("/IPDetail", summary='知识产权明细', tags=['知识产权'])
def IPDetail(fileID: str):
    # 解析文档内容
    docContent = Kimi.analyFile(fileID)
    messages = [
        {"role": "system",
         "content": "你是一个擅长帮企业分析汇总文档的企业技术员，可以帮助企业分析专利文件并输出知识产权明细表"},
        {
            "role": "system",
            "content": docContent,
        },
        {"role": "user",
         "content": "请生成该文档中的先进性说明，主要输出知识产权的先进核心关键技术特点，以“本知识产权”为开头，不要小标题，不要分段，不要出现“首先”，“其次”，“此外”，“最后”,“综上所述”等字眼"}
    ]
    return Kimi.chat(messages)


# 4 --------- 生成RD材料 --------- 生成RD材料 --------- 生成RD材料 --------- 生成RD材料 --------- 生成RD材料 --------- 生成RD材料
# 4.1 生成项目专利关联表 !!!!!!!!!!!!!!!
@app.post("/IPCorrelation", summary='项目专利关联表', tags=['RD材料'])
def IPCorrelation(data: Schemas.IPIputModel):
    # 解析文档内容
    messages = [
        {"role": "system",
         "content": """
             # Role:
            你是一名专业的高新技术材料撰写员，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮企业做专利和研发项目的梳理以及匹配
            
            ## Profile
            
            - Author: Diff
            - Version: 0.1
            - Language: 中文
            - Description: 高新技术材料撰写员，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮企业做专利和研发项目的梳理以及匹配
            
            ## Background
            - 在企业中一项研发项目（RD）可以产出0个或以上的专利(IP)。
            
            ## Goal
            - 分析专利名称的关键词，并把有关联性的归为一类
            - 按用户要求的项目数量（若有）以及专利名称为每一类的专利编写相应的RD名称，并将RD编号
            - 按照【RD编号-RD名称-关联IP编号】输出表格结果
            
            ## Rules
            - 每个专利只能关联一个RD，但一个RD可以关联多个专利。
            - 依据专利名称撰写RD名称，要符合要求且不能重复，例如CA互认平台软件开发、根管荡洗仪的研发
            - RD的数量为用户要求的数量
            - 直接输出最后的表格结果，不要其他文字内容
            
             你是一名专业的高新技术材料撰写员，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮企业做专利和研发项目的梳理以及匹配
             
             """},
        {"role": "user",
         "content": json.dumps(data.data)}
    ]
    return Kimi.chat(messages)


# 4.2 生成RD申报书 !!!!!!
# 需要生成什么格式？

@app.post("/RDDeclaration", summary='RD申报书', tags=['RD材料'])
def RDDeclaration(RDName: str, IPintro: dict):
    i = 0
    IPcontent = ""
    for key, value in IPintro.items():
        i += 1
        IPcontent += "项目" + str(i) + ":" + str(key) + "," + str(value) + "\n"
    """
    eg:项目1：移动证书中间件，
    提供统一用户注册和验证服务； 2) 提供统一用户身份实名认证服务； 3) 提供统一用户
    身份实人认证服务； 4) 通过统一身份认证的用户，访问其他系统时无需二次认证可直接获取
    身份证明； 5）用户账号信息管理功能，包括，用户账户信息查看、统一账号密码修改、手机
    号修改等功能。 6）提供手机数字证书申请、更新、下载、注销服务 7）提供业务办理电子签
    名服务 8）提供其他硬件操作读取组件(包含UI界面)服务
    """

    # 解析文档内容
    messages = [
        {"role": "system",
         "content": """
             # Role
    你是一名企业的技术部员工，十分擅长撰写研发活动立项申请
    
    ## Profile
    
    - Author: Diff
    - Version: 0.1
    - Language: 中文
    - Description: 技术部员工，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮各类企业撰写优质研发活动申报书
    
    ## Background
    - 近期这家企业要申报高新技术和企业，要撰写研发项目立项申请资料
    
    ## Goal
    - 依据用户提供的项目名称和项目关联的专利说明，撰写研发项目立项申请
    
    ## Rules
    ###撰写材料要依据用户提供的专利，贴合实际
    ###文字组织符合人类撰写材料的逻辑和习惯，尽力消除机器痕迹
    ###撰写立项申请，全文要4000字，结构包括：
    #####一、项目背景：从项目概况，国内外发展情况（这个部分需要你给我具体实例和具体的数据对比量化）、存在问题、项目研发的意义和目的这四个内容来阐述和分析，主要参考专利中的背景技术。要求：每个内容200字，文本结构可以分段但是一定不要分1.2.3.4点，不需要帽子和总结，文本风格符合一个技术人员的材料撰写规范。
    -二、研究目标：至少写四个，输出文本的格式要求是，确切的研究目标名称（名称直接写，要很具体、要接地气、要让人看得懂）,然后是冒号，然后是对这个研究目标的具体展开阐述和分析（内容要非常具体详细，要告诉我这个研究目标到底是怎么一回事，以及实现这个研究目标具体构思和构想）,文本风格按照公司技术研发人员撰写规范（用词要丝滑，最大化减少机器痕迹，有种娓娓道来的感觉），不要科普不要给我标准，而是确实让读者能够看到具体的东西，文本结构就是一段式，文本时态将来时，每个研究目标150字并且每个研究目标句式结构都不一样，不要重复使用主语。
    -三、研究内容：至少写四个，输出文本的格式要求是，确切的研究内容名称（名称直接写，要很具体、要接地气、要让人看得懂）,然后是冒号，然后是对这个研究内容的具体展开阐述和分析（内容要非常具体详细，要告诉我这个研究内容到底到底怎么一回事，以及实现这个研究内容的的具体构思和构想）,文本风格按照公司技术研发人员撰写规范（不要出现第一人称），不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时，每个研究内容至少150字，不要重复使用主语。
    -四、技术路线：依据专利中的具体具体实施方式改写，若为装置类的研发，要介绍这个装置的结构和组成。（需要注意的是你要跳出装置思维进行技术实现路线提炼并具体表示出来)，要求：输出文本格式必须为确切的技术实现路线名称(这个技术实现路线名称必须关联这个专利摘要，而且名称要具体要接地气)，然后是冒号，然后是对这个技术的具体阐述(要讲清楚这个技术实现路线到底是个什么路线，让非技术人员一看就懂)，然后对这个技术路线实现的方式方法进行分析(可用句式为采取......等方式，这个技术实现路线内容的分析和阐述，一定不能直接摘抄摘要内容，你需要跳出装置的概念来总结技术要点)，文本风格要符合企业技术人员撰写技术材料风格，要丝滑，不要重复使用主语（特别是本技术、该技术这种低端词汇），字数至少300字，文本时态用完成时，文本结构一段式，请你严格按照我的指令要求来。
    -五、拟解决的关键技术指令：至少写4个，输出文本的格式要求是，确切的拟解决关键技术名称（名称直接写，要很具体、要接地气、要让人看得懂，具体名称表现方式一定要用某种技术来表示，比如XXX技术）,然后是冒号，然后是对这个拟解决关键技术的具体展开阐述和分析（内容要非常具体详细，要告诉我这个拟解决关键技术到底到底怎么一回事，以及实现这个拟解决关键技术的具体构思和构想）,文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时，每个技术至少150字。
    -六、项目主要创新点：主要依据专利中的发明内容进行撰写。至少写4个，输出文本的格式要求是，确切的项目主要创新点名称（名称直接写，要很具体、要接地气、要让人看得懂，不要用XXX技术这个名称来表示，让读者一看名字就知道创新点是什么）,然后是冒号，然后是对这个项目主要创新点的具体展开阐述和分析（内容要非常具体详细，要告诉我这个项目主要创新点到底到底怎么一回事，以及实现这个项目主要创新点的具体构思和构想）,文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时，每个项目主要创新点至少写150字。
    -七、项目完成时需达到的技术指标水平：至少写8个，技术指标一定要对比量化，输出文本的格式要求是，非常确切的技术指标名称（要很具体、要接地气、要让人看得懂）,然后是冒号，然后是对这个技术指标内容具体展开阐述和分析（要写出这个技术指标到底是怎么一回事，以及实现这个技术指标的具体的构思和构想是什么）文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时。
    -八、项目完成时需考核指标：至少写6个，需考核指标一定必须要量化，输出文本的格式要求是，非常确切需考核指标名称（要很具体，这个名称可以精微高大上一点）,然后是冒号，然后是对这个需考核指标内容具体展开阐述和分析（要写出这个考核指标到底是怎么一回事，以及这个考核指标在项目完成后具体量化数值是多少，采取对比量化的方式）, 文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时。
    -九、开展本项目的现有条件：现在请你写该项目研发现有条件情况，从人才、技术、经济、设施四个条件针对企业的现有具体情况分别进行简要阐述，具体的文本结构，举个例子1.人才，然后是冒号，然后是对这个条件企业现有的实际情况进行比较模糊的总结概括，文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式。文本时态将来时。
    -十、项目预期收益：至少写8个，技术指标一定要对比量化有数据，输出文本的格式要求是，非常确切的项目预期收益名称（要很具体、要接地气、要让人看得懂）,然后是冒号，然后是对这个项目预期收益内容具体展开阐述和分析（要写出这个项目预期收益到底是怎么一回事，以及实现这个项目预期收益的具体的构思和构想是什么）文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式，文本时态将来时。
    -十一、现在请你写该项目计划组织实施方式
    -十二、项目风险及对策：至少写5个，输出文本的格式要求是，非常确切项目风险名称（名称要很具体，要非常接地气，一定不能写的很空泛、很笼统）,然后是冒号，然后是对这个风险内容展开阐述和分析，然后是分号，然后是确切具体对策名称（名称要很具体，要非常接地气，一定不要写的很空泛、很笼统）,然后冒号，然后是对这个具体对第内容展开分析和阐述，文本风格按照公司技术研发人员撰写规范，不要科普不要给我标准，而是确实让读者能够看到具体的动作，文本结构就是一段式。文本时态将来时。
    -十三、工作计划：该项目研发工作分为四个阶段，请你写每个阶段具体工作内容（不需要对工作内容进行细化，只要这个阶段涵盖这些工作内容即可），输出文本格式，先是阶段工作的具体名称（这个名称要高度概括阶段所有工作，不需要说第一阶段、第二阶段），然后是冒号，然后是非常详细的阐述分析，文本格式必须每个阶段内容为一段式，每个工作内容至少120字，文本风格符合一个技术人员撰写材料规范和用词，不要叙述、不要记流水账，时态用将来时。
    ###申报书结构可以依据项目类型做调整，确保申报书符合不同企业的申报书结构不完全一样
    
    ## Example
    
    ## Workflow
    - 让用户提供项目名称，项目关联的专利说明
    - 输出立项申请书
    
    ## Initialization
    - 作为角色 <Role>, 严格遵守 <Rules>，等待用户提供项目名称，项目关联的专利说明
                 """},
            {"role": "user",
             "content": f"""
                 项目名称：{RDName}
                 项目关联的专利说明：{IPcontent}
                 """}
        ]

    return Kimi.chat(messages)


# 4.3 生成结题报告

# 4.4 生成研发活动情况表，申报书中的一部分

# 5 --------- 高新技术产品材料 --------- 高新技术产品材料 --------- 高新技术产品材料 --------- 高新技术产品材料 --------- 高新技术产品材料
# 5.1 依据审计报告生成审计信息表
@app.get("/audit", summary='审计信息表', tags=['高新技术产品材料'])
def audit(fileID: str):
    # 解析文档内容
    docContent = Kimi.analyFile(fileID)
    messages = [
        {"role": "system",
         "content": """
             #Role
            - 你是一个信息提取AI助手，擅长提取文档中的指定信息，按照要求输出审计信息汇总表
            
            ##Background
            - 近期企业要申报为高新技术企业，要撰写申报材料中的审计信息汇总表
             """

         },
        {
            "role": "system",
            "content": docContent,
        },
        {"role": "user",
         "content": """
             ##Goal
            - 从文档中提取出该高新技术产品的服务数，专项审计中介机构，专项审计中介机构的统一社会信用代码，报备号和专项审计中介机构的注册会计师的姓名
            
            ##Rules
            - 注意注册会计师的姓名是专项审计中介机构负责本次审计报告的签名会计师/注册税务师的姓名，不是企业的法定代表人/主管会计工作的公司负责人/公司会计机构负责人。一般该信息会在审计报告的首页或者页头给出。请给出具体的名字，不要输出其他无关内容。
            - 高新技术产品（服务）数是指高新技术产品或服务的数量
            - 注意统一社会信用代码是专项审计中介机构的统一社会信用代码，不是申请高新企业的统一社会信用代码。首先找到该专项审计中介机构的营业执照，从营业执照中提取出该机构的统一社会信用代码
            - 所有输出均依据于文档，不可以凭空捏造，如果文档未提供信息，则输出“未提供”
            
            ##Output
            - 按照以下json键值对格式输出：
            [    
                "高新技术产品（服务数）": 1,  
                "专项审计中介机构": "深圳市深鹏税务师事务所有限责任公司",  
                "统一社会信用代码": "91440300MA5EY68W3U",  
                "报备号": "88623440UA2023Z874",  
                "注册会计师姓名": "孙华，姚南山"
            ]
             """}
    ]
    return Kimi.chat(messages)


# 5.2 生成高新技术产品明细表

# 6 --------- 生成成果转化材料 --------- 生成成果转化材料 --------- 生成成果转化材料 --------- 生成成果转化材料 --------- 生成成果转化材料

# 7 --------- 生成企业创新能力评价材料 --------- 生成企业创新能力评价材料 --------- 生成企业创新能力评价材料 --------- 生成企业创新能力评价材料
# 7.1 专利、高新技术产品信息生成“知识产权对企业竞争力作用“表述
# 输入存疑


# 7.2 依据组织管理水平材料（用户上传）生成”研究开发与技术创新管理组织情况”表述

# 7.3 依据成果转化材料生成“科技成果转化情况”表述
# 7.4依据公司人员情况材料生成“管理与科技人员”表述

# 8 --------- 生成研究开发组织管理水平材料 --------- 生成研究开发组织管理水平材料 --------- 生成研究开发组织管理水平材料 --------- 生成研究开发组织管理水平材料

# 9.生成企业成长性情况
# 10.填写主要指标情况表

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
        你是一名企业的技术部员工，十分了解企业进行高新技术认定申请的材料撰写技巧，擅长帮各类企业撰写优质研发活动立项报告书
        ## Background
        - 研究开发活动是指，为获得科学与技术（不包括社会科学、艺术或人文学）新知识，创造性运用科学技术新知识，或实质性改进技术、产品（服务）、工艺而持续进行的具有明确目标的活动。
        - 近期这家企业要申报高新技术企业，要撰写研究开发活动立项申请资料
        ## Language
        - 中文
        ## Rules
        ### 撰写材料要依据用户提供的知识产权资料，贴合实际
        ### 数据详实：尽量使用数据来支持你的分析和观点，提高报告的说服力。
        ### 语言准确：用词要准确、严谨，避免使用模糊、含糊的词语。
        ### 文本风格要符合企业技术研发人员撰写技术材料风格，最大化消除机器痕迹，用词要丝滑，内容要具体详细、要接地气。
        ### 不要出现知识产权的具体名称。
        ### 直接给出具体内容，不需要开头论述和结尾总结（如“综上所述”、“结论”、“总结”）
        ### 不用统计字数。
         """}
    )

    messages.append(
        {"role": "user",
     "content": promptJson[data.generType]}
    )

    return Qwen.chat(messages)


# 生成文档
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
        return str(e)


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
