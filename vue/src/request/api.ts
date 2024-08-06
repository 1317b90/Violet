import service from "@/request/index";

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
    return service.post('qwenUpFile', data, {
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
