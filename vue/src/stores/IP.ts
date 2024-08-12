import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const useIP = defineStore('IP', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "知识产权资料": [],
    "公司基本资料": [],
  })

  // 内容数据
  const C: { [key: string]: string } = reactive({
    "研发活动专利关联表": "",
  })


  return { F, C }
})
