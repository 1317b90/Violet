import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const useRDactivate = defineStore('RDactivate', () => {
  // 本地文件列表
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "项目研发立项报告": [],
    "知识产权证书": [],
  })


  return { F }
})
