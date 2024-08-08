import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'
import { generAPI } from '@/request/api'


export const useIP = defineStore('IP', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "知识产权资料": []
  })

  // 内容数据
  const C: { [key: string]: string } = reactive({
    "项目背景": "",
    "项目研发的目的和意义": "",
  })


  return { F, C }
})
