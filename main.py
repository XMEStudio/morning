from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time

today = datetime.now()
year = datetime.now().year
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_week():
  week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
  d = datetime.today()  # 获取当前日期时间
  week = week_list[d.isoweekday() - 1]
  return week

def get_today():
  delta = time.strftime("%Y-%m-%d", time.localtime())
  return delta

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
data ={"weather":{"value":wea,"color":get_random_color()},"highest":{"value":highest,"color":get_random_color()},"lowest":{"value":lowest,"color":get_random_color()},"city":{"value":city,"color":get_random_color()},"week":{"value":get_week(),"color":get_random_color()},"today":{"value":get_today(),"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
