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