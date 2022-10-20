import requests
import re
import json
import time
import datetime
from datetime import date, timedelta

s=requests.session()
def login():
    data={
        "id": username,
        "pwd": password,
        "act": "login"
    }
    head={
        "Connection": "keep-alive",
        "Host": "libic.sicnu.edu.cn",
        "Origin": "http://libic.sicnu.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    r=s.post("http://libic.sicnu.edu.cn/ClientWeb/pro/ajax/login.aspx",data=data,headers=head)
    login_information=json.loads(r.text)
    if login_information['msg']=="ok":
        print("登录成功，请确认登录信息"+str(login_information['data']))
    else:
        print("登录失败，可能导致此原因的因素有：\n1.网络问题，请确认在校园网环境运行此程序，具体检测方法为打开http://lib.sicnu.edu.cn/查看是否能正常打开\n2.账号密码错误，请确认账号密码输入正确，且没有输入错误的字符标点等\n3.其余问题可以联系管理员\n(特别提示：多次登录失败可能导致IP封禁)")
        exit()
def liberary_location():
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    location=input("请指定位置,目前仅支持二楼自习室[A2001-A2170]：")
    head={
        "Connection": "keep-alive",
        "Host": "libic.sicnu.edu.cn",
        "Origin": "http://libic.sicnu.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    data2={
        "byType": "devcls",
        "classkind": "8",
        "display": "fp",
        "md": "d",
        "room_id": "102171927",
        "purpose": "",
        "selectOpenAty": "",
        "cld_name": "default",
        "date": today,
        "fr_start": "08:00",
        "fr_end": "12:00",
        "act": "get_rsv_sta",
        "_": "1665935644078"
    }
    r=s.get("http://libic.sicnu.edu.cn/ClientWeb/pro/ajax/device.aspx",data=data2,headers=head)
    data=json.loads(r.text)
    if data['msg']=="ok":
        data=data['data']
        locate=re.findall(r'\d+',location)
        locate_num=int(locate[0])-2001
        if locate_num > 169 or locate_num < 0:
            print("查询成功，输入错误，请仔细核对座位号")
            liberary_location()
        l_infor=data[locate_num]['devId']
        print("座位查询成功，devid="+l_infor)
        return l_infor   
    else:
        print("查询图书馆座位位置出错，可能由于图书馆网页更换导致，请及时联系管理员。")
        exit()
def task():
    login()
    times=0
    tomorrow = (date.today() + timedelta(days= 1)).strftime("%Y-%m-%d")
    while True:
        r=s.get("http://libic.sicnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dialogid=&dev_id="+location_number+"&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&number=&classkind=&test_name=&start="+tomorrow+"+08%3A00&end="+tomorrow+"+11%3A30&up_file=&memo=&act=set_resv&_=1665936592796")
        data=json.loads(r.text)
        print(data['ret'])
        if data['ret'] == 1:
            break
        print(r.text)
        times=times+1
        if times>100:
            break
        time.sleep(1);
username=input("请输入用户名：")
password=input("请输入密码：")
login()
location_number=liberary_location()
model=input("是否立即进行抢课（1.立即抢座位  2.在计划时间抢座位（计划时间为7：00））：")
if model=='2':  
    print("已进入计划模式，预计将在今日七点开始，如果需要抢次日座位，请在次日重新打开本程序") 
    while True:
        date2 = datetime.datetime.now().strftime("%H:%M")
        if date2 == '07:00':
            task()
            break
        time.sleep(1)
elif model=='1':
    task()
else:
    print("无语拉这也能输错，重启试试吧。。")
    exit()