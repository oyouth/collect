# -*- coding: utf-8 -*-
from distutils.command.config import config
from bs4 import BeautifulSoup
import sys
import os
import json
import csv
import math
import random
import requests
import time
import pandas as pd

class Mblog(object):
    def __init__(self, config):
        self.headers = {
            'Referer': 'http:www.weibo.com',
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7,pl;q=0.6",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
        self.max_page = config['max_page']
        self.task_file = config['task_file']
        self.page = 1
        self.page_number = 1
        self.uid = 0
        self.tag = ''

    # 读取任务 
    def get_tasks(self, file_path):
        csv_file = open(file_path,  encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        rows = []
        for row in csv_reader:
          rows.append(row)
        return rows

    # 接口解析
    def get_mblog_urls(self):
        # 接口地址
        delay = random.uniform(1.5, 2.5)
        time.sleep(delay)
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}&containerid=107603{0}&page={1}'.format(str(self.uid), str(self.page))
        print('api', url)
        rsp = requests.get(url=url, headers=self.headers)
        rsp = json.loads(rsp.text)
        data = rsp['data']
        # 解析meta信息
        if 'cardlistInfo' in data:
            # 计算页数
            if  self.page == 1:
                  total = data['cardlistInfo']['total']
                  count = math.ceil(total/10)
                  # 判断最大
                  if count > self.max_page:
                      count = self.max_page
                  print('total', total, count)
                  # 多页：开始循环采集
                  if  count > 1:
                      self.page_number = count
                      self.get_mblog_loop()
            # 提取card信息
            rows = self.extract(data['cards'])
            # 保存到csv，每页保存一次
            if len(rows) > 0:
                self.save(rows)

    # 循环采集
    def get_mblog_loop(self):
        if  self.page <= self.page_number:
            pages = range(self.page, self.page_number, 1)
            for page in pages:
                self.page = int(page) + 1
                print('[page/total]',  self.page, self.page_number)
                self.get_mblog_urls()

    # 长微博
    def get_long_text(self, mid):
        url = 'https://m.weibo.cn/statuses/extend?id={0}'.format(mid)
        try:
            rsp = requests.get(url=url, headers=self.headers)
            rsp = json.loads(rsp.text)
            text = rsp['data']['longTextContent']
            return text
        except Exception as e:
            print('get long text err', e)
            return ''

    # 提取微博        
    def extract(self, cards):
      rows = []
      for k, card in enumerate(cards):
          print('card-{0} , card_type: {1}, {2}'.format(k+1, card['card_type'], 0))
          if not card['card_type'] == 9:
            continue
          mblog = card['mblog']
          text  = mblog['text']
          # 长微博
          if mblog['isLongText'] == True:
              longtext = self.get_long_text(mblog['mid'])
              if not longtext == '':
                  text = longtext
          # 过滤html
          text = BeautifulSoup(text, 'html.parser').get_text()
          row = (self.tag, mblog['mid'], text, mblog['source'], mblog['created_at'])
          # print('row', row)
          rows.append(row)
      return rows

    # 写入csv
    def save(self, rows):
        dir = 'mblogs'
        if not os.path.isdir(dir):
            os.makedirs(dir)
        file_path = dir + os.sep + str(self.uid) + '.csv'
        csv_file = open(file_path, 'a', encoding='utf-8', newline="")
        csv_writer = csv.writer(csv_file)
        if not os.path.isfile(file_path):
            header = ('tag', 'mid', 'text', 'source', 'created_at')
            csv_writer.writerow(header)
        csv_writer.writerows(rows)
        csv_file.close()
        print('[saved] {0}条数据'.format(len(rows)))
     
    # 执行采集
    def start(self):
        task_file = self.task_file
        tasks = self.get_tasks(task_file)
        # 循环执行任务
        for i, task in enumerate(tasks):
            # 检测状态
            print('--- '*6)
            print('[No]', i, task)
            if task[2] == '1':
              print('[pass]', i)
              continue
            # 切换用户停顿
            delay = random.uniform(2.5, 10.5)
            time.sleep(delay)
            # 初始化基本参数
            self.page = 1
            self.page_number = 1
            self.uid = int(task[0])
            self.tag = task[1]
            # 开始采集
            self.get_mblog_urls()
            # # 更改任务状态
            df = pd.read_csv(task_file)
            df.iloc[i, 2] = 1
            df.to_csv(task_file, index=False)

def main():
    # 配置文件
    config = {
        'max_page': 30,  # 最大采集页数
        'task_file': 'list.csv' #任务列表（3列： uid, 自定义tag,状态）
    }
    spider = Mblog(config)
    spider.start()

if __name__ == "__main__":
    main()
