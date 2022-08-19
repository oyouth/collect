# 采集脚本

## 微博
### 微博采集
通过微博`uid`，批量采集用户的所发布的微博（仅采集card_type=9格式的）。
```
/weibo/mblog.py
```
#### 任务列表

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
