import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'
import { generAPI } from '@/request/api'

// 专利专利专利专利专利专利专利专利专利专利专利专利专利

// 任务需要的文件
const generForFile: { [key: string]: string[] } = {
  "项目概述": ["专利说明书"],
  "立项目的": ["专利说明书"],
  "关键技术": ["专利说明书"],
  "技术创新点": ["专利说明书"],
  "实施方案": ["专利说明书"],
  "已取得的工作进展": ["专利说明书"],
  "下一步研究计划和任务": ["专利说明书"],
  "项目完成情况": ["专利说明书"],
}


export const usesetup2 = defineStore('setup2', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "专利说明书": []
  })

  // 内容数据
  const C: { [key: string]: string } = reactive({
    "项目概述": "",
    "立项目的": "",
    "关键技术": "",
    "技术创新点": "",
    "实施方案": "",
    "已取得的工作进展": "",
    "下一步研究计划和任务": "",
    "项目完成情况": "",
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
