from slugbot import botutils
import configs
import commands
import utils
import lang
from utils import aqua_slug

token = configs.ACCESS_TOKEN
page = configs.ID
page1 = configs.PAGE_ID[0]
poem = '''
<澎湖賦別>
甘草抗告唐僧
農夫偷走大坌坑
鱉蔑視卡達路燈
興奮珊瑚瞪阿瞪
南投仙人掌不出聲
謙虛律師吸柳橙
坑?
我躲起來冷
好冷! 好冷! 鬍鬚博士說 "有風箏!"
可惜大舅媽捨不得陪霧淞哼哼哼
鮮豔蟾蜍不肯爬老枯藤
螺絲緊緊咬著角落帳篷
旋轉曼陀羅是無敵麻繩
保證砍倒痲瘋
粉筆，假髮，雷射鹹菜羹
'''
r = utils.page_post(page, token, poem)
print(r)




