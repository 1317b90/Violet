import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const useachieve = defineStore('achieve', () => {
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "项目操作使用手册 ": [],
    "产品采购合同": [],
  })


  return { F }
})
