import service from "@/request/index";

// --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户

// 登录
export async function login(username: string, password: string) {
    return service({
        url: "login",
        method: "POST",
        data: {
            "username": username,
            "password": password,
        }
    })
}


// --------- 项目 --------- 项目 --------- 项目 --------- 项目 --------- 项目 --------- 项目

// 根据id查询项目
export async function getItem(id: number) {
    return service({
        url: "getItem?id=" + String(id),
        method: "GET",
    })
}

// 新建项目
export async function addItem(username: string) {
    return service({
        url: "addItem?username=" + username,
        method: "GET",
    })
}

// 查询指定用户的所有项目
export async function getItems_by_user(username: string) {
    return service({
        url: "getItems_by_user?username=" + username,
        method: "GET",
    })
}

// 更新项目公司基本资料
export async function setItemCompany(data: Object) {
    return service({
        url: "setItemCompany",
        method: "POST",
        data: data
    })
}


// 删除项目
export async function delItem(id: number) {
    return service({
        url: "delItem?id=" + String(id),
        method: "GET",
    })
}

// 修改项目名称

export async function setItemName(id:number,name:string) {
    return service({
        url: "setItemName?id="+String(id)+"&name="+name,
        method: "GET",
        
    })
}


// ------------------------------------
// 知识产权
export async function generIPadvanced(fileList: Array<Object>) {
    return service({
        url: "IPadvanced",
        method: "POST",
        data: fileList
    })
}

export async function generIPRD(fileList: Array<Object>) {
    return service({
        url: "IPRD",
        method: "POST",
        data: fileList
    })
}


// ---------- 立项报告 ---------- 立项报告 ---------- 立项报告 ---------- 立项报告 ---------- 立项报告


// 通用生成请求
export async function generAPI(fileList: Array<Object>, generType: string) {
    return service({
        url: "itemSetup",
        method: "POST",
        data: {
            generType: generType,
            fileList: fileList
        }
    })
}


// 上传公司基本资料
export async function upCompanyForm(data: FormData) {
    return service.post('kimiUpFile', data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}



// 生成预览
export async function generDoc(generData: { [key: string]: string }) {
    console.log(generData)
    return service({
        url: "generDoc",
        method: "POST",
        data: generData
    })
}


// 研发活动情况表

export async function generRDactive(fileList: Array<Object>) {
    return service({
        url: "RDactive",
        method: "POST",
        data: fileList
    })
}



// 高新技术产品情况表
export async function generHighTech(fileList: Array<Object>) {
    return service({
        url: "highTech",
        method: "POST",
        data: fileList
    })
}



// 成果转化说明

export async function generAchieve(fileList: Array<Object>) {
    return service({
        url: "achieve",
        method: "POST",
        data: fileList
    })
}


// 企业创新能力评价
export async function generInnovative(fileList: Array<Object>, generType: string) {
    let urlName = ""
    switch (generType) {
        case "知识产权对企业竞争力作用":
            urlName = "IPcompetion";
            break;
        case "研究开发与技术创新管理组织情况":
            urlName = "manage400";
            break;
        case "科技成果转化情况":
            urlName = "scienceAchieve";
            break;
        case "管理与科技人员":
            urlName = "sciencePeople";
            break;
        default:
            break;
    }
    return service({
        url: urlName,
        method: "POST",
        data: fileList
    })
}


// 研究开发组织管理水平
export async function generManage(fileList: Array<Object>) {
    return service({
        url: "manage1000",
        method: "POST",
        data: fileList
    })
}