from DrissionPage import ChromiumPage

# 获取企业id
def getID(companyName:str):
    page = ChromiumPage()
    url = 'https://aiqicha.baidu.com/s?q=' + companyName + '&t=0'
    page.get(url)
    company_list = page.ele(".company-list")
    company_list_wrap = company_list.ele(".wrap")
    companys = company_list_wrap.eles("tag:a")
    companyID = companys[0].attr("data-log-title")[5:]
    page.close()
    return companyID

def getInfo(companyID:str):
    page = ChromiumPage()

if __name__ == '__main__':
    iiid=getID("昆明依利科特科技有限公司")
    print(iiid)


