import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const useachieve = defineStore('achieve', () => {
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "知识产权资料   ": [],
    "产品销售合同": [],
  })


  return { F }
})
