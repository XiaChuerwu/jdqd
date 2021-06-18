import requests
import re
import json
import urllib
import time
import timeit
import math
import sys
from datetime import datetime
from dateutil import tz
import os
import dateutil.parser
requests.packages.urllib3.disable_warnings()
osenviron={}
djj_djj_cookie=''
Card_telegram=''
inviteid=''
versions='V1.3-2021-6-18'
version='红鲤鱼绿鲤鱼与驴，学习与测试用2021.6.18 '
#修复圈叉环境提示连接失败。
#集卡划分万瓶正装美丽研究院,每天手动运行两次即可。
#微信群友互助码，接力增加后面
inviteidlist=['2554','1704695','1934043','1931425']
#互助码格式['1233','56666','55666']
#感谢支持我的互助码267592

#填写京东ck格式pt_key=,,,,pin:xxxxc;
#多号码用&链接
Formatcookie=0#0是&连接1是换行连接


osenviron["JD_COOKIE"]='pt_key=AAJgwUGkADCaWr6xNZLunmC8gezA_csDMKNydCBIacPJ_SUYfties3UrZeoZJG9nlyPp53fa5iM;pt_pin=jd_6f9b9a6769afb;&pt_key=AAJgwFJLADCj2XL3qGWsl_jMQOHKfk4xujGynyx3RL0usxwQlr1LGBJMethUQlzIrs4XQzmQwMg;pt_pin=jd_7d11b7fef428f;&pt_key=AAJgujtMADCAUi5Zz7Nl0p7koS92S5LffbUMSdVvSWpCMg1rApe8Kl2_RCUpdNqb2oi8_mREHoc;pt_pin=jd_756c956e68aee;&pt_key=AAJgujvMADC4GPnqm_pDCpliIk6Crbh9rqmKC1xAyGHTcVMCxaCeWxHSv_W5TtlvlYhLXGnYk1M;pt_pin=jd_47a6d379fd0fe;&pt_key=AAJgwfCvADAm8rCo_cRCYkI7ApIuJA5VCnlydbPj2c5lTvjOje2Gfl531KenrIQToB8Boo6oJsw;pt_pin=%E6%A2%81%E9%9C%9E%E5%AE%87123;&pt_key=AAJgxJu5ADBw8qEmwanb83KPmtZ_44wu70f9ZoIVvwNOCCkbib4tce-FExM47y6S2w9Jrpejrgw;pt_pin=242486518-117963;'



#关注助力模块1是打开，0是关闭
Helpfun=1#关注助力模块1是打开，0是关闭
Taskdo=1#关注做任务模块1是打开，0是关闭
Chosecount=0#选择助力账号组的第x个，0位全部账号运行，1代表只运行第1个，2代表第2个



userNameList = []
cookiesList = []
pinNameList = []
jd_cookie=''
ckList=[]
telelist=[]
#=============
#osenviron["Card_telegram"]=''
Bearer=''
bean=0
result=''


Jdheader={"Accept": "application/x.jd-cosmetic-618.v1+json","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-cn","User-Agent": "jdapp;iPhone;9.4.0;14.4.2;3c6b06b6a8d9cc763215d2db748273edc4e02512;network/4g;ADID/B38160D2-DC94-4414-905B-D15F395FD787;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone11,8;addressid/2173286081;supportBestPay/0;appBuild/167541;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1","Content-Type": "application/json;charset=utf-8"}
def get_user_info(s):
    print('\n 获取活动主页'+str(s))
    global result
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/get_user_info'
    
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    if 'status_code' in resp:
       if resp['status_code']==401:
          print('Authorization失效，请重新获取')
          return
    if json.dumps(resp).find('status_code')>0:
          result+=resp['message']+'\n'
    else:
       if s==2:
        #result+=f"{resp['step1_num']}\n"
        print(f"当前活动已有{resp['step1_num']}人集齐卡片")
        inviteid=resp['id']
        result+='【邀请码:'+str(inviteid)+'】\n【卡片详情:】\n'
        n=0
        result+=' 1级卡:'
        for card in resp['my_card']:
           if card['type']==1:
              result+=f"【{card['name']}】{card['num']}"   
        result+='\n 2级卡:'
        for card in resp['my_card']:
           if card['type']==2:
              result+=f"【{card['name']}】{card['num']}"   
        
             
             
        return 
       
       elif s==1:
         Hecheng1=[]
         Hecheng2=[]
         n=0
         for card in resp['my_card']:
           if card['type']==1:
              Hecheng1.append(card['num'])
           if card['type']==2:
              Hecheng2.append(card['num'])
         print('等级1的卡:')
         print(Hecheng1)
         print('等级2的卡:')
         print(Hecheng2)
         print('可以合成'+str(min(Hecheng1))+'张金卡')
         if int(min(Hecheng1))>0:
           	   synthetize(int(min(Hecheng1)))
           	   
           	   
           	   
         inviteid=resp['id']
         print('【邀请码:'+str(inviteid)+'】')
         print(f"剩余{resp['draw_times']}次")
         if resp['draw_times']>0:
             drew(resp['draw_times'])
         if resp['is_sign']==0:
              sign_in()
         
def access_token(token):
    print('\n 更新2')
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/jd-user-info'
    body={"token":token,"source":"01"}
    Jdheader['Content-Type']= "application/json;charset=utf-8"
    Jdheader['Accept']='application/x.jd-cosmetic-618.v1+json'
    resp = requests.post(url,headers=Jdheader,data=json.dumps(body),verify=False,timeout=60).json()
    Bearer=resp['access_token']
    return Bearer
      
def get_token():
  print('\n 更新1')
  try:
    url = 'https://api.m.jd.com/client.action?functionId=isvObfuscator'
    body='adid=B38160D2-DC94-4414-905B-D15F395FD787&area=19_1601_50284_50451&body=%7B%22url%22%3A%22https%3A%5C/%5C/xinruimz1-isv.isvjcloud.com%22%2C%22id%22%3A%22%22%7D&build=167694&client=apple&clientVersion=10.0.2&d_brand=apple&d_model=iPhone11%2C8&eid=eidIea548121a9saMHu2CIDQQGexggddnFKEUTB7t3bzepH%2Bp8EudbuNOzqyu8XNW7OkG1ZXbb0MU28RFow3tJU8tLSZJNqceCDF/l%2B57QmpG5kgk19N&isBackground=N&joycious=2&lang=zh_CN&networkType=4g&networklibtype=JDNetworkBaseAF&openudid=3c6b06b6a8d9cc763215d2db748273edc4e02512&osVersion=14.6&partner=apple&rfs=0000&scope=11&screen=828%2A1792&sign=4089167097dc0705b9f97f6a86b8265d&st=1624003289105&sv=112&uemps=0-0&uts=zrHR4oLv7fO8bj08KaWkuJrGiAm/G6alpSm6Xi3w6q6St29zL/3WOO6K%2Bj6xe%2BAVa0OTjS1zYWcWPxqDzVZJxYHk%2BqLSSnp91wBjZ7Dp9UuOhliM95VNAYi3%2BO0HWnakJ4QoSljqVcqATvj2ylOjjTRIhAqsm/NT&uuid=hjudwgohxzVu96krv/T6Hg%3D%3D&wifiBssid=unknown'
    Jdheader['Content-Type']='application/x-www-form-urlencoded'
    resp = requests.post(url,headers=Jdheader,data=body,verify=False,timeout=60).json()
    token=resp['token']
    return token
  except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
      

def synthetize(jj):
  print('\n 合成金卡')
  try:
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/synthetize'
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    print(resp)
    print(f"合成{resp['card']['name']}集齐卡片")
    jj-=1
    if jj>0:
       synthetize(jj)
       time.sleep(5)
  except Exception as e:
      msg=str(e)
      print(msg)



def sign_in():
    print('\n 签到')
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/sign_in'
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    print(resp)
    time.sleep(1)
    
def drew(mm):
  print('\n 还有'+str(mm)+'次抽奖机会')
  try:
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/drew'
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    #print(resp)
    if 'card' in resp:
       print(f"结果:获得{resp['card']['name']}卡")
    else:
        print(f"{resp['message']},可能需要手动解除。")
    time.sleep(2)
    mm-=1
    if mm>0:
       drew(mm)
  except Exception as e:
      msg=str(e)
      print(msg)
def meetingplace_view():
  print('\n 浏览会场')
  try:
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/meetingplace_view'
    for i in range(15):
      resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
      if 'status_code' in resp:
       if resp['status_code']==401:
          print('Authorization失效，请重新获取')
          break
      print('第'+str(i+1)+'执行:::')
      if 'coins' in resp:
        print(f"{resp['coins']}-{resp['user_coins']}")
      else:
         print(resp['message'])
      time.sleep(2)
  except Exception as e:
      msg=str(e)
      print(msg)
def beauty_view():
    print('\n 进去美丽研究院')
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/beauty_view'
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    if 'coins' in resp:
        print(f"{resp['coins']}-{resp['user_coins']}")
    else:
         print(resp['message'])
    time.sleep(1)
def task_state():
    print('\n 任务列表')
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/task_state'
    resp = requests.get(url=url,headers=Jdheader,verify=False,timeout=60).json()
    if 'status_code' in resp:
       if resp['status_code']==401:
          print('Authorization失效，请重新获取')
          return
    #if resp['today_follow_nums']==resp['daily_shop_follow_times']:
      #print('完成')
      #return 
    N=0
    for data in resp['follow_shop']:
       print(str(N+1)+'店铺:'+data['name'])
       if data['is_done']==0:
         m=data['id']
         shop_view(m)
         time.sleep(1)
         add_product(m)
         time.sleep(1)
       else:
          print('完成')
       N+=1

def invite():
   if Helpfun==0:
     print('\n【你已经关闭互助模块.需要开启功能，请在代码开始处将Helpfun=1】\n')
     return
   print('\n开始互助========')
   try:
    if len(inviteidlist)==0:
       print('\n互助码为0个,请在本代码中开始处【inviteidlist=['']】增加')
    else:
        print('共有'+str(len(inviteidlist))+'个互助码')
    N=0
    for inviteid in inviteidlist:
      N+=1
      print(str(N)+'开始互助好友:'+inviteid)
      #if inviteid==
      url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/invite'
      bd={"inviter_id":inviteid}
      res = requests.post(url=url,headers=Jdheader,verify=False,data=json.dumps(bd),timeout=60)
      if str(res).find('204')>=0:
         print('网络错误,访问频繁,互助码数组过多======')
         break
      else:
      	 print(res.json()['message'])
      if 'status_code' in res.json():
       if res.json()['status_code']==401:
          print('Authorization失效，请重新获取')
          break
      time.sleep(10)
   except Exception as e:
      msg=str(e)
      print(msg)
         
         

    
def shop_view(m):
    print('关注和浏览店铺id:'+str(m))
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/shop_view'
    bd={"shop_id":m}
    res = requests.post(url=url,headers=Jdheader,verify=False,data=json.dumps(bd),timeout=60).json()
         #print(res)
    if 'coins' in res:
        print(f"{res['coins']}-{res['user_coins']}")
    else:
         print(res['message'])
             
    
def add_product(m):
    print('商品加车id:'+str(m))
    url = 'https://xinruimz1-isv.isvjcloud.com/mlyjyapi/add_product'
    bd={"product_id":m}
    res = requests.post(url=url,headers=Jdheader,verify=False,data=json.dumps(bd),timeout=60).json()
         #print(res)
    if 'coins' in res:
         print(f"{res['coins']}-{res['user_coins']}")
    else:
         print(res['message'])
             
def meili618():
   print('\n美丽研究618集卡开始做任务.........')
   get_user_info(1)
   if Taskdo==1:
     meetingplace_view()
     beauty_view()
     task_state()
   else:
       print('\n【你已经关闭任务模块.需要开启功能，请在代码开始处将Taskdo=1】\n')
   invite()
   get_user_info(2)
#=============================
def pushmsg(title,txt):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   try:
     if Card_telegram.strip():
         print("\n【Telegram消息】")
         id=Card_telegram[Card_telegram.find('@')+1:len(Card_telegram)]
         botid=Card_telegram[0:Card_telegram.find('@')]

         turl=f'''https://api.telegram.org/bot{botid}/sendMessage?chat_id={id}&text={title}\n{txt}'''

         response = requests.get(turl,verify=False,timeout=5)
   except Exception as e:
      print(str(e))
    


def watch(flag,list):
   vip=''
   if flag in osenviron:
      vip = osenviron[flag]
   if flag in os.environ:
      vip = os.environ[flag]
   if vip:
       if Formatcookie==1:
         print('\n【你选择的是换行连接cookies】')
         for line in vip.split('\n'):
            if not line:
              continue
            list.append(line.strip())
         return list
       elif Formatcookie==0:
         print('\n【你选择的是&连接cookies】')
         for line in vip.split('&'):
            if not line:
              continue
            list.append(line.strip())
         return list
         
         
   else:
       print(f'''【{flag}】 is empty,DTaskuset is over.''')
       exit()
       

JD_API_HOST = 'https://api.m.jd.com/client.action'
headers={
       "origin": "https://h5.m.jd.com",
      "referer": "https://h5.m.jd.com/",
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'jdpingou;iPhone;3.15.2;12.4;fccee6e5e9f146fcedd9be68ef5807568f000c12;network/4g;model/iPhone11,8;appBuild/100365;ADID/B38160D2-DC94-4414-905B-D15F395FD787;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/11;pap/JA2015_311210;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

def TotalBean(cookies,checkck):
   print('\n开始检验数据是否过期=====')
   signmd5=False
   headers= {
        "Cookie": cookies,
        "Referer": 'https://home.m.jd.com/myJd/newhome.action?',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
      }
   try:
       
       ckresult= requests.get('https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New',headers=headers,verify=False,timeout=10).json()
       if json.dumps(ckresult,ensure_ascii=False).find(checkck)>0:
           signmd5=True
           print('用户数据正确====')
           loger(f'''用户名【{checkck}】''')
       else:
       	  signmd5=False
       	  msg=f'''【京东账号{checkck}】cookie已失效,请重新登录京东获取'''
          print(msg)
          pushmsg('ck过期',msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5
def islogon(j,count):
    JD_islogn=False
    jd_name=''
    for i in count.split(';'):
       if i.find('pin=')>=0:
          jd_name=i.strip()[i.find('pin=')+4:len(i)]
          jd_name=urllib.parse.unquote(jd_name)
          print(f">>>>>>【账号{str(j)}开始】{jd_name}")
          if(TotalBean(count,jd_name)):
             JD_islogn=True
    return JD_islogn
def loger(m):
   global result
   result +=m+'\n'
    
def start():
       global jd_cookie,cookiesList,Jdheader,result,Bearer
       scriptHeader = """
════════════════════════════════════════
║                                      ║
║     京东美丽618-公众号iosrule          ║
║                                      ║
════════════════════════════════════════
"""+f"【versions:{versions}】"
       print(scriptHeader)
      # watch('Card_telegram',telelist)
      #Card_telegram=telelist[0]
       watch('JD_COOKIE',cookiesList)
       if Chosecount==0:
          print(f"\n你配置的是{len(cookiesList)}个账号执行任务\n")
       n=0
       for count in cookiesList:
         n+=1
         if Chosecount>0 and n!=Chosecount:
            continue
         result+=str(n)+'-'
         Jdheader['Cookie']=count
         token=get_token()
         if not token:
            return 
         Bearer=access_token(token)
         if not Bearer:
            return 
         Jdheader['Authorization']='Bearer '+Bearer
         
         if(islogon(n,count)):
            meili618()
            result+='\n'
       print('════════════════════════通知═══════════════')
       print(result)

if __name__ == '__main__':
    print('Localtime', datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
    start()
