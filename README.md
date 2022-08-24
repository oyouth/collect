# 采集脚本

树洞开源行动：https://github.com/oyouth/shudong

## 微博
```
git clone https://github.com/oyouth/collect.git
```
```
cd weibo
```
安装脚本所依赖的python模块
```
pip install -r requirements.txt
```
### 1.用户微博采集
通过微博`uid`，批量采集用户的所发布的微博（仅采集card_type=9类型）。

#### 任务列表
文件`mblog.csv`，示例：
|uid|tag|status|
|---|---|---|
|1648007681|tag1|0|
|6275961723|tag2|0|

其中`tag`可在采集微博时作批量标注用途。状态`status`的值：`0`表示未采集；`1`表示已采集，下次运行将会跳过。
#### 采集设置
```
config = {
    'max_page': 30,
    'task_file': 'mblog.csv'
}
```
#### 运行
```
python mblog.py
```
#### 保存
默认保存于`mblogs`目录下，每个uid对应一个csv文件，如：
```
./mblogs/1648007681.csv
```

### 2.微博超话采集
通过微博话题id，批量采集超话帖子（可单独设置页数限制）。

#### 任务列表
文件`topics.csv`，示例：
|id|name|limit|status|
|---|---|---|---|
|10080807930c974401ee7d0d242aed3c6d19ca|抑郁超话|2|0|
|100808e056951c0679ee95c6eb872a589c0744|抑郁症患者超话|2|0||

- `id`可在超话主页连接中找到，也可自行拼凑。规则是：100808+超话的md5加密串，比如`抑郁`的32位加密结果是：`07930c974401ee7d0d242aed3c6d19ca`）。
- `name`用作采集微博数据保存文件名。
- `limit`为采集该超话的最大页数
- `status`为任务状态：`0`表示未采集；`1`表示已采集，下次运行将会跳过。

#### 运行
```
python topic.py
```
#### 保存
默认保存于`topics`目录下，每个name对应一个csv文件，如：
```
./topics/抑郁超话.csv
```


