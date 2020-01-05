# BiliBili抽奖API解析

## 目录:
- 1.小电视,摩天大楼类抽奖
- 2.PK类抽奖
- 3.大航海抽奖(舰长,提督,总督)
- 4.节奏风暴类抽奖

### 1.小电视,摩天大楼类抽奖

#### 1.检测API

地址: https://api.live.bilibili.com/xlive/lottery-interface/v3/smalltv/Check?roomid=

请求方法: **GET**

参数: roomid=房间号

不需要带headers,也不需要带cookies

#### 2.加入API

地址: https://api.live.bilibili.com/xlive/lottery-interface/v5/smalltv/join

请求方法: **POST**

参数如下:

| 参数 | 值 |
| ---- | --- |
| id   | 礼物的id |
|roomid |房间的真实id(不能是短号码) |
|type | 礼物的类型|
|csrf | 在cookie中获取|
|csrf_token| 跟csrf一样的值|
|visit_id| 留空即可|

#### ~~3.通知API(已废弃)~~

地址: https://api.live.bilibili.com/xlive/lottery-interface/v3/smalltv/Notice?type=&raffleId=

请求方法: **GET**

参数: type=礼物类型&raffleId=礼物Id