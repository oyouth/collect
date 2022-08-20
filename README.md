# 采集脚本

## 微博
### 1.用户微博采集
通过微博`uid`，批量采集用户的所发布的微博（仅采集card_type=9类型）。
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
```

```
