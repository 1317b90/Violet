import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'
import { generAPI } from '@/request/api'

// 软著软著软著软著软著软著软著软著软著软著软著软著软著软著

// 任务需要的文件
const generForFile: { [key: string]: string[] } = {
  "项目背景": ["软件著作权登记申请表", "用户手册或设计说明书"],
  "项目研发的目的和意义": ["软件著作权登记申请表", "用户手册或设计说明书"],

  "项目主要内容": ["用户手册或设计说明书"],
  "关键技术": ["代码文档"],
  "技术创新点": ["代码文档"],
  "技术指标": ["代码文档"],

  "总体逻辑结构设计": ["用户手册或设计说明书"],
  "采用的技术路线": ["软件著作权登记申请表", "代码文档"],

  "市场调研": ["用户手册或设计说明书"],
  "研发基础": ["软件著作权登记申请表", "公司基本资料"],

  "效益分析": ["用户手册或设计说明书"],
  "风险分析": ["用户手册或设计说明书"]
}


export const usesetup1 = defineStore('setup1', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "软件著作权登记申请表": [],
    "用户手册或设计说明书": [],
    "代码文档": [],
    "公司基本资料": []
  })

  // 内容数据
  const C: { [key: string]: string } = reactive({
    "项目背景": "",
    "项目研发的目的和意义": "",

    "项目主要内容": "",
    "关键技术": "",
    "技术创新点": "",
    "技术指标": "",

    "总体逻辑结构设计": "",
    "采用的技术路线": "",

    "市场调研": "",
    "研发基础": "",

    "效益分析": "",
    "风险分析": "",
  })

  // 发起请求，获取生成内容
  async function getGener(generType: string) {
    let fileList: Object[] = []
    for (const fileType of generForFile[generType]) {
      let fileList1 = F[fileType]

      if (fileList1.length == 0) {
        ElMessage.error("请先上传" + fileType + "！")
        // 如果发现文件不齐全，返回一个值，打断函数
        return false
      } else {
        fileList = fileList.concat(fileList1)
      }
    }

    try {
      const res = await generAPI(fileList, generType);
      C[generType] = res.data;
      ElNotification({
        title: '生成成功',
        message: generType + '生成成功！',
        type: 'success',
        position: 'bottom-right',
      });

      // 生成完毕后自动保存一次
      sessionStorage.setItem(generType, res.data);
      return true
    } catch (err) {
      const errMsg = generType + '生成失败，请重试！';
      ElNotification({
        title: '生成失败',
        message: errMsg,
        type: 'error',
        position: 'bottom-right',
      });
      return false
    }
  }

  // 获取批量任务
  async function getGeners() {
    let tasks = []
    // 依次添加每一项任务
    for (const generType of Object.keys(C)) {
      tasks.push(getGener(generType))
    }
    return tasks
  }


  return { F, C, getGener, getGeners }
})
