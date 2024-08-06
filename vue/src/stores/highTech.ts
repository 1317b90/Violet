import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'


export const usehighTech = defineStore('highTech', () => {
  const F: { [key: string]: UploadUserFile[] } = reactive({
    "项目操作使用手册  ": [],
    "知识产权证书或高新技术产品证书（如有）": [],
  })


  return { F }
})
