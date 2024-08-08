import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'

export const usemanage = defineStore('manage', () => {
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "管理制度文件": [],
  })
  return {F}
})
