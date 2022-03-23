# ----------------------------------------------------------
# coding=utf-8
# Copyright © 2021 Komorebi660 All rights reserved.
# ----------------------------------------------------------

import requests
import re
import datetime
from requests.sessions import session
requests.packages.urllib3.disable_warnings()

# ------ 用户在运行前需更改的变量 ------ #
USR = ''  # 学号
PWD = ''  # 密码
LOCATION = ''  # 所在校区, 用中文表示
EMERGENCY_CONTACT = ''  # 紧急联系人姓名
RELATIONSHIP = ''  # 本人与紧急联系人关系
PHONE_NUMBER = ''  # 紧急联系人电话
# ------------------------------------ #


# 需要在同一session下执行
session = requests.Session()

# Step1: 获取CAS_LT
CAS_LT_url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
CAS_LT_res = session.get(CAS_LT_url)
CAS_LT_html = CAS_LT_res.content.decode()
CAS_LT = re.findall('(?<=name="CAS_LT" value=")(.*?)(?=")', CAS_LT_html)[0]
# print(CAS_LT)


#Step2: 获取token
login_url = 'https://passport.ustc.edu.cn/login'
login_data = {
    'model': 'uplogin.jsp',
    'CAS_LT': CAS_LT,
    'service': 'https://weixine.ustc.edu.cn/2020/caslogin',
    'warn': '',
    'showCode': '',
    'username': USR,
    'password': PWD,
    'button': ''
}
login_res = session.post(login_url, data=login_data)
login_html = login_res.content.decode('utf-8')
token_temp = re.findall('(?<=name="_token" value=")(.*?)(?=")', login_html)
# 检查返回值是否正确
if (len(token_temp) == 0):
    print("UserName or Password ERROR!")
    exit(0)
_token = token_temp[0]
# print(token)


#Step3: 上报
post_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
post_data = {
    '_token': _token,
    'juzhudi': LOCATION,
    'body_condition': '1',
    'body_condition_detail': '',
    'now_status': '1',
    'now_status_detail': '',
    'has_fever': '0',
    'last_touch_sars': '0',
    'last_touch_sars_date': '',
    'last_touch_sars_detail': '',
    'is_danger': '0',
    'is_goto_danger': '0',
    'jinji_lxr': EMERGENCY_CONTACT,
    'jinji_guanxi': RELATIONSHIP,
    'jiji_mobile': PHONE_NUMBER,
    'other_detail': ''
}
res = session.post(post_url, data=post_data)
html = res.content.decode('utf-8')
alert = re.findall('(?<=<p class="alert alert-success">)(.*?)(?=<a)', html)
if (len(alert) == 0):
    print("Health Check-in ERROR!")
    exit(0)
else:
    print(alert[0])


# Step4: 出校报备
curr_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
next_date = datetime.datetime.now()+" 23:59:59"
report_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/post'
report_data = {
    '_token': _token,
    'start_date': curr_date,
    'end_date': next_date,
    'return_college[]': '东校区',
    'return_college[]': '西校区',
    'return_college[]': '中校区',  # 可设置跨哪些校区
    't': '3'
}
report_res = session.post(report_url, data=report_data)
report_html = report_res.content.decode('utf-8')
report_alert = re.findall(
    '(?<=<p class="alert alert-success">)(.*?)(?=<a)', report_html)
if (len(report_alert) == 0):
    print("Out of School Report ERROR!")
    exit(0)
else:
    print(report_alert[0])
