# 一款基于python的在线两步验证工具web版
## 软件支持steam 以及 战网

## 使用方法:

### Steam  

使用root的安卓手机,提取 steam_uuid.xml

具体路径为 /data/data/com.valvesoftware.android.steam.community

示例

```
{"shared_secret":"xxxxxxxxxxxxx=","serial_number":"xxxxxxxxxxxxx","revocation_code":"xxxxxxxxxxxxx","uri":"otpauth:\/\/totp\/Steam:xxxxxxxxxxxxx?secret=xxxxxxxxxxxxx&issuer=Steam","server_time":"xxxxxxxxxxxxx","account_name":"xxxxxxxxxxxxx","token_gid":"xxxxxxxxxxxxx","identity_secret":"xxxxxxxxxxxxx+xxxxxxxxxxxxx=","secret_1":"xxxxxxxxxxxxx","status":null,"steamguard_scheme":2,"steamid":"xxxxxxxxxxxxx"}
```



### 战网

提供 战网的令牌串号  以及 重置编码 即可

示例

串号

```
CN-1234-1234-1234
```

重置编码

```
xxxxxxxxxx
```



获得以上信息后,将配置复制到instance 目录下的 config.py 中即可

先安装steam,flask依赖库

运行

```
pip install steam flask
```



最后 运行 

```
python main.py 
```



访问 ` http://localhost:5000`



# 目录说明:



bna :战网令牌库

instance:配置文件

