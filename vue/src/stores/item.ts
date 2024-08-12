import { reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadUserFile } from 'element-plus'

import type { companyI } from "@/interface"

export const useitem = defineStore('item', () => {
  // 当前被选中的项目id
  const id = ref()

  const name = ref()

  // 公司基本资料
  const company = reactive<companyI>({
    id: 0,
    companyName: "",
    companyMoney: 0,
    companyIntro: "",
    companyTime: new Date(),
    companyScope: "",
    companyFile: ""
  })

  return { id, name, company }
})
