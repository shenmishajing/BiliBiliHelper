# BiliBiliHelper.conf 配置文件说明  

## [Function] 功能区域
``CAPSULE`` 扭蛋功能,**True**开启**False**关闭  
``CASEJUDGER`` 风纪委员仲裁,**True**开启**False**关闭 **为了维护风纪委员社区的公平性，请慎重使用此功能**  
``COIN2SILVER`` 硬币换银瓜子,**True**开启**False**关闭  
``GIFTSEND`` 自动送出礼物,**True**开启**False**关闭  
``GROUP`` 应援团签到功能,**True**开启**False**关闭  
``SILVER2COIN`` 银瓜子兑换硬币功能,**True**开启**False**关闭  
``SILVERBOX`` 自动领取银瓜子宝箱,**True**开启**False**关闭  
``TASK`` 自动领取每日任务,**True**开启**False**关闭  
``RAFFLE_HANDLER``小电视之类抽奖,**True**开启**False**关闭  
``MainDailyTask``主站日常任务,**True**开启**False**关闭  
``MatchTask``赛事相关任务,**True**开启**False**关闭  

## [Coin2Silver] 硬币兑换银瓜子设置区域
``COIN`` 每天需要兑换多少枚硬币为银瓜子(数字)

## [Live] 直播区域
``ROOM_ID`` 房间号,用于心跳包

## [GiftSend] 自动送礼区域
``ROOM_ID`` 房间号,用于送出礼物,用,分隔  
``TIME`` 什么时候送出礼物，单位为H，例如23时送出礼物，如果为-1脚本运行后立即执行，且每天固定执行
``GIFTTiME`` 时间,送出还有多少秒过期的礼物，如果为-1不受时间限制

## [Raffle_Handler] 小电视之类的抽奖功能设置区域(细分)
``TV`` 是否参与小电视类抽奖,**True**开启**False**关闭  
``PK`` 是否参与PK抽奖,**True**开启**False**关闭  
``GUARD`` 是否参与大航海抽奖,**True**开启**False**关闭  
``STORM`` 是否参与节奏风暴抽奖,**True**开启**False**关闭  

## [MainDailyTask] 主站日常任务区域
``ROOM_ID`` up主id号,用于要观看投币分享的up主,用,分隔   
``Watch`` 观看任务开关,**1**开启**0**关闭  
``Coin`` 投币开关,**1**开启**0**关闭  
``Share`` 分享开关,**1**开启**0**关闭  

## [MatchTask] 赛事相关区域
`` OpenCapsule``赛事抽奖开关,**True**开启**False**关闭  
``Message``发送的弹幕

## [Log] 日志设置区域
``LOG_LEVEL`` 日志等级
> debug : 最全,用与调试和排除Bug(如果不进行开发不推荐)
>> info : 除了调试的信息其他的都有(强烈推荐)
>>> warning : 警告,几乎没有什么信息(强烈不推荐)
>>>> error : 错误,同上(强烈不推荐)
>>>>> critical : 严重错误,同上(强烈不推荐)

## [Other] 其他设置区域
``INFO_MESSAGE`` 欢迎信息,**True**开启**False**关闭  
``SENTENCE`` 名句,强烈推荐开启,**True**开启**False**关闭  

## [Proxy] 代理设置区域
``PROXY_TYPE`` 代理类型,支持None,Http和Socks5  
``PROXY_ADDRESS`` 代理服务器地址(配置见下)  
socks5填写:  
``socks5://用户名:密码@IP地址:端口``  
没有用户名密码:  
``socks5://IP地址:端口``  
http填写:  
``http://用户名:密码@IP地址:端口``  
没有用户名密码:  
``http://IP地址:端口``  

## [API] API服务器设置区域
``ENABLE`` 是否开启API服务器,**True**开启**False**关闭  
``LISTEN_PORT`` API服务器的监听端口,取值``1-65535``  
``ALLOW_LAN`` 允许局域网连接

## [Server] 舰长监听服务器设置区域
``ADDRESS`` 舰长服务器地址,可以是IP或者域名,**无需**``ws://``协议前缀  
``PASSWORD`` 舰长服务器密码

## [pcheaders] pc请求头 (该区域无需填写)
``Accept`` 接受类型  
``User-Agent`` 用户代理  
``Accept-Language`` 接受语言  
``accept-encoding`` 接受编码  
``cookie`` cookie  
