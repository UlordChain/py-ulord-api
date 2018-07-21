# 一、概述

SDK项目根目录有十个文件，文件对应的简要功能如下表所示：

| 文件名 |  | 功能说明 |
| --- | --- | --- |
| udfs |  | UDFS模块，涵盖UDFS的一些配置和操作接口 |
| config |  | 项目配置文件 |
| daemonCLI |  | 命令行文件 |
| errcode |  | 错误码文件 |
| manage |  | 数据库管理文件 |
| up |  | ulord平台相关http接口封装 |
| user |  | 用户角色分类，包括初级开发者以及中级开发者 |
| utils |  | 工具文件 |
| version |  | 版本文件 |
| webServer |  | web服务文件 |

SDK根据用户的角色提供不同的接口功能。用户角色包含初级开发者角色与中级开发者角色两类。中级开发者仅对UDFS与UP进行了封装和继承。提供一些数据上链的必要操作接口。初级开发者SDK为其设计了默认数据库，根据数据库提供了一些更丰富的操作接口，中级开发者也可以通过模仿设计自己的数据库形式。下文分别列出中级开发者和初级开发者接口调用说明。

# 二、中级开发者接口

其中9-26为封装平台层接口，用户可以访问[https://github.com/UlordChain/Ulord-platform/blob/master/ulord/API.md](https://github.com/UlordChain/Ulord-platform/blob/master/ulord/API.md)查询对应请求参数类型。

## 1、初始化

**描述：**

    根据appkey与secret初始化中级开发者角色。appkey与secret均可以通过在平台层注册登录创建应用程序获得。每个应用程序可以获得一对appkey与secret。

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| appkey | 是    | string | 开发者生成应用的账户 |
| secret | 是    | string | 开发者生成应用的密码 |

**代码示例：**

```py
develop = Senior(
    appkey='8326648868ad11e8b894fa163e37b4c3',
    secret='8326648968ad11e8b894fa163e37b4c3'
    )
```

## 2、解密

**描述：**

    利用公私钥对参数进行解密。参数为被公钥加密过的形式。可以是加密信息数组或单个加密信息。采用RSA加密。加密完需要使用base64进行编码。解密过程为将参数进行base64解码，然后使用私钥进行解密。如果参数为不可解密信息，则返回None。

**方法名：**

*decrypt*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| args | 是    | string/list | 加密信息或加密信息数组 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| string/list  | 解密信息或解密信息数组 |

**代码示例：**

```py
>>>develop.rsahelper._encry("test")
I9FrluvSwrtmmd7MIZgvfNlbwHU2g4R/v88eoU28cfHXt0x/wWWHNeEAJenFPEc76fmDgcvASHPMUXYAkeJlzqsq5MhleFQMRaxR6dpsVL3rCAd9feOQbl3kMg4oaJqpAKcJ71v8J2EGAOf4suTnGEmj2kYshrR1PdxSsThRLc8=
>>>
>>>develop.decrypt(
    args='wyB7HL56fGFHd53e8WZdfFQipBcVqej1/+TApbq9qduIoGRfGbzHEayHIwNbfEPq1WLj00x9Qa3CyW2RMo6ZRXbC0wzKc/6RClPvq6TTQ2oxSt/pPy5sEbfrJj57ozfh+nVhNSGAa1p1cHMj3pTN5j+J+7pUSLLtaMTCWWBOPK8=')
test
```

**备注：**
    加密部分采用RSA加密，调用时会在当前文件夹下生成对应的公私钥文件，可以调用develop.rsahelper._encry(要加密的信息[string])加密得到加密信息再验证此方法。

## 3、配置编辑

**描述：**

根据输入修改配置，如果为数组则转化成字典，配置为一个字典，实现方式为配置字典与参数字典合并。

**方法名：**

*config_edit*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| args | 是    | list/dict | 需要修改的数组或字典 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| dict  | 传入的参数在配置中的形式显示 |

**代码示例：**

```py
>>>develop.config_edit(['dbconfig','JSON_AS_ASCII', True])
{'dbconfig': {'JSON_AS_ASCII': True}}
```

## 4、配置展示

**描述：**

根据输入展示配置，如果为数组则转化成字典，配置为一个字典，实现方式为配置字典与参数字典合并。

**方法名：**

*config_show*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| args | 是    | list/dict | 展示的关键字（默认为所有） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| dict  | 传入的参数在配置中的形式显示 |

**代码示例：**

```py
>>>develop.config_show(['dbconfig'])
{'JSON_AS_ASCII': False, 'IsCreated': False, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///sqlite.db', 'SQLALCHEMY_TRACK_MODIFICATIONS': True, 'SQLALCHEMY_COMMIT_ON_TEARDOWN': True, 'SECRET_KEY': 'ulord platform is good'}
```

## 5、UDFS下载

**描述：**

根据输入去下载对应的资源，将结果组成字典返回。

**方法名：**

*udfs_download*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| udfshashs | 是    | list | udfs哈希列表 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| dict  | 对应的哈希字典，下载成功为true，失败为false |

**代码示例：**

```py
>>>develop.udfs_download(['QmQng3FX98mSe34z3jM1QFQ7XVsoEDWPbKg25ygPaWzgv4'])
Udfs has started!
Now you can use it to download or upload!
{'QmQng3FX98mSe34z3jM1QFQ7XVsoEDWPbKg25ygPaWzgv4': True}
```

## 6、UDFS上传

**描述：**

根据输入将内容上传至UDFS中，判断参数类型去调用对应的内置方法实现上传。

**方法名：**

*udfs_upload*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| fileinfos | 是    | list | 需要上传的文件名或者文件流或者对应的列表 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| dict  | 上传结果，对应文件名、文件流或者列表字典，上传成功为true，失败为false |

**代码示例：**

```py
>>>develop.udfs_upload('E:\ulord\py-ulord-api\ulordapi\udfs\upapi.log')
Udfs has started!
Now you can use it to download or upload!
{'E:\\ulord\\py-ulord-api\\ulordapi\\udfs\\upapi.log': u'QmRtvbkn8sa47rhxf6ujUYJFxhinNVkh5LH2iCsgvNJVKe'}
```

## 7、UDFS内容查看

**描述：**

根据输入遍历哈希值在UDFS上查阅对应的内容，已字符串形式返回。

**方法名：**

*udfs_cat*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| udfshashs | 是    | list | 需要查看的udfs哈希值列表 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| dict  | 对应哈希值内容字典。成功为内容字符串，失败为0 |

**代码示例：**

```py
>>>develop.udfs_cat(['QmRtvbkn8sa47rhxf6ujUYJFxhinNVkh5LH2iCsgvNJVKe'])
Udfs has started!
Now you can use it to download or upload!
{'QmRtvbkn8sa47rhxf6ujUYJFxhinNVkh5LH2iCsgvNJVKe': "[2018-07-11 11:19:11,586] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:24:21,368] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:24:39,167] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:24:56,463] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:30:16,339] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:30:24,226] INFO     Udfs: Udfs has started!\r\nNow you can use it to download or upload!\r\n[2018-07-11 11:31:08,524] INFO     Udfs: stop daemon\r\n[2018-07-11 11:31:08,664] ERROR    Udfs: remove self.lock([WinError 32] \xc1\xed\xd2\xbb\xb8\xf6\xb3\xcc\xd0\xf2\xd5\xfd\xd4\xda\xca\xb9\xd3\xc3\xb4\xcb\xce\xc4\xbc\xfe\xa3\xac\xbd\xf8\xb3\xcc\xce\xde\xb7\xa8\xb7\xc3\xce\xca\xa1\xa3: 'E:\\\\ulord\\\\py-ulord-api\\\\ulordapi\\\\udfs\\\\config\\\\repo.lock') failed!\r\n[2018-07-11 11:34:30,166] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:34:36,498] INFO     Udfs: Udfs has started!\r\nNow you can use it to download or upload!\r\n[2018-07-11 11:34:42,899] ERROR    FileHelper saveFile error:not readable\r\n[2018-07-11 11:35:02,015] INFO     Udfs: stop daemon\r\n[2018-07-11 11:35:02,069] ERROR    Udfs: remove self.lock([WinError 32] \xc1\xed\xd2\xbb\xb8\xf6\xb3\xcc\xd0\xf2\xd5\xfd\xd4\xda\xca\xb9\xd3\xc3\xb4\xcb\xce\xc4\xbc\xfe\xa3\xac\xbd\xf8\xb3\xcc\xce\xde\xb7\xa8\xb7\xc3\xce\xca\xa1\xa3: 'E:\\\\ulord\\\\py-ulord-api\\\\ulordapi\\\\udfs\\\\config\\\\repo.lock') failed!\r\n[2018-07-11 11:35:17,023] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:35:22,917] INFO     Udfs: Udfs has started!\r\nNow you can use it to download or upload!\r\n[2018-07-11 11:36:51,734] INFO     Udfs: Current os is Windows\r\n[2018-07-11 11:36:56,695] INFO     Udfs: Udfs has started!\r\nNow you can use it to download or upload!\r\n[2018-07-11 11:37:34,111] INFO     UdfsHelper: upload stream cost:33.957062005996704\r\n[2018-07-11 11:37:35,367] INFO     Udfs: stop daemon\r\n[2018-07-11 11:37:35,433] ERROR    Udfs: remove self.lock([WinError 32] \xc1\xed\xd2\xbb\xb8\xf6\xb3\xcc\xd0\xf2\xd5\xfd\xd4\xda\xca\xb9\xd3\xc3\xb4\xcb\xce\xc4\xbc\xfe\xa3\xac\xbd\xf8\xb3\xcc\xce\xde\xb7\xa8\xb7\xc3\xce\xca\xa1\xa3: 'E:\\\\ulord\\\\py-ulord-api\\\\ulordapi\\\\udfs\\\\config\\\\repo.lock') failed!\r\n"}
```

## 8、自定义请求

**描述：**

根据输入向平台层请求。此方法考虑到平台层向后兼容，用户可自己添加SDK未提供而平台层提供的接口。

**方法名：**

*request*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| method | 是    | string | 请求方法 |
| url | 是    | string | 请求url |
| data | 否    | dict | 请求参数字典 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 对应请求结果 |

**代码示例：**

```py
>>>develop.request(method='get',url='http://114.67.37.2:10583/v1/content/list/1/1')
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 27,
             u'records': [{u'author': u'\u7b2c\u56db\u65b9',
                           u'claim_id': u'ebd3e0496e14d942c77f0e2ee30b433377a38902',
                           u'content_type': u'.txt',
                           u'create_timed': u'2018-06-30 11:38:33',
                           u'create_timed_timestamp': 1530329913,
                           u'currency': u'UT',
                           u'des': u'\u6d4b',
                           u'enabled': True,
                           u'id': 37,
                           u'price': -0.001,
                           u'status': 1,
                           u'tags': [u'\u7ecf\u6d4e',
                                     u'\u519b\u4e8b',
                                     u'\u65c5\u6e38'],
                           u'title': u'\u6d4b\u8bd5',
                           u'update_timed': None,
                           u'update_timed_timestamp': None}],
             u'total': 27}}
```

## 9、生成钱包

**描述：**

根据输入创建一个托管ulord钱包。

**方法名：**

*regist*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| args | 是    | string | 用户名 |
| args | 是    | string | 密码 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.regist(username='tests',password='123')
{u'reason': u'success', u'errcode': 0}
```

## 10、资源发布

**描述：**

将字典内容上链，发布到ulord链上。

**方法名：**

*publish*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| data | 是    | dict | 发布数据字典 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.publish(data={
        "author": "tests",
        'pay_password': '123',
        "title": "第一篇技术博客",
        "tags": ["blockchain", "UDFS"],
        "udfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
        "price": 0.1,
        "content_type": ".txt",
        "des": "这是使用UDFS和区块链生成的第一篇博客的描述信息"
    })
{u'reason': u'success', u'errcode': 0, u'result': {u'claim_id': u'dbfbb5eb3a9365d2609a3f5a510a7395cef88f15', u'id': 38}}
```

**备注：**
　发布资源会消耗0.01个ulord测试币，初始用户余额为0，应该首先调用接口14（为用户转账）。

## 11、资源更新

**描述：**

根据输入更新ulord链上数据

**方法名：**

*update*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| data | 是    | dict | 更新数据字典 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>result = develop.update(data={
        "id": "38",  # 资源在db中的id
        "pay_password": "123",  # 支付密码
        "tags": ["update"],
        "price": 1.2,
        "content_type": ".exe",
        "des": "update blog description"
    })
{u'reason': u'success', u'errcode': 0, u'result': {u'claim_id': u'dbfbb5eb3a9365d2609a3f5a510a7395cef88f15', u'id': 38}}
```

## 12、资源删除

**描述：**

根据输入更新ulord链上数据

**方法名：**

*delete*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| id | 是    | int | 平台层数据ID |
| password | 是    | string | 钱包密码 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 根据输入删除ulord链上数据 |

**代码示例：**

```py
>>>develop.delete(id=1,password='123')
{u'reason': u'success', u'errcode': 0, u'result': {u'num': 1}}
```

## 13、资源付费

**描述：**

根据输入对资源进行消费。如果为广告则需要传入作者的钱包密码。

**方法名：**

*transaction*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| payer | 是    | string | 支付者钱包名 |
| claim_id | 是    | string | 资源链上ID(claim_id) |
| pay_password | 是    | string | 钱包密码 |
| isads | 是    | bool | 资源是否为广告（默认不是） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.transaction(
        payer='tests',
        claim_id='6af5772b0887ce1a92b0123d4c8e098b2d73ad55',
        pay_password='123',
        isads=False
    )
{u'reason': u'success', u'errcode': 0, u'result': {u'udfs_hash': u'QmRVGqCGo2uwewVoNKWq5NXNN1sYhKvDnFATkSWcDSuqQK'}}
```

**备注：**
　返回UDFS哈希后通过SDK下载或者前端调用ipfs的js包连接到udfs网络中(网关入口:114.67.37.2:20418)从而获取到内容。

## 14、向用户转账

**描述：**

开发者给用户转账。

**方法名：**

*paytouser*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是    | string | 转账的用户钱包名 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.paytouser('tests')
{u'reason': u'success', u'errcode': 0}
```

**备注：**
　转账操作设计为活动的形式，即新用户注册赠送一定数量的ulord测试币，数量可以在配置文件中自行定义，默认为10。

## 15、资源列表

**描述：**

根据输入返回资源列表。

**方法名：**

*queryresource*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| page | 否 | int | 第几页(默认为第一页) |
| num | 否 | int | 每页几条数据（默认十条） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryresource(page=1,num=1)
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 27,
             u'records': [{u'author': u'\u7b2c\u56db\u65b9',
                           u'claim_id': u'ebd3e0496e14d942c77f0e2ee30b433377a38902',
                           u'content_type': u'.txt',
                           u'create_timed': u'2018-06-30 11:38:33',
                           u'create_timed_timestamp': 1530329913,
                           u'currency': u'UT',
                           u'des': u'\u6d4b',
                           u'enabled': True,
                           u'id': 37,
                           u'price': -0.001,
                           u'status': 1,
                           u'tags': [u'\u7ecf\u6d4e',
                                     u'\u519b\u4e8b',
                                     u'\u65c5\u6e38'],
                           u'title': u'\u6d4b\u8bd5',
                           u'update_timed': None,
                           u'update_timed_timestamp': None}],
             u'total': 27}}
```

## 16、余额查询

**描述：**

根据输入查询余额。

**方法名：**

*querybalance*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| payer | 是    | string | 钱包名 |
| pay_password | 是    | string | 钱包密码 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.querybalance(payer='tests', pay_password='123')
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'confirmed': u'9.990715',
             u'total': u'9.990013',
             u'unconfirmed': u'-0.000702',
             u'unmatured': u'0'}}
```

## 17、资源是否已购买

**描述：**

根据输入查询资源是否已经购买。

**方法名：**

*queryisbought*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| payer | 是    | string | 钱包名 |
| claim_ids | 是    | list | 资源链上ID（claim\_id）列表 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.checkisbought(payer='tests', claim_ids=['6af5772b0887ce1a92b0123d4c8e098b2d73ad55'])
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'6af5772b0887ce1a92b0123d4c8e098b2d73ad55': u'QmRVGqCGo2uwewVoNKWq5NXNN1sYhKvDnFATkSWcDSuqQK'}}
```

**备注：**
　验证是否已购买该资源，若已购买则返回对应的udfs哈希值，未购买则返回False.

## 18、查询用户已发布资源

**描述：**

根据输入查询用户已发布的资源列表。

**方法名：**

*queryuserpublished*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| wallet_username | 是  | string | 钱包名 |
| page | 否 | int | 第几页（默认为第一页） |
| num | 否 | int | 每页多少条数据（默认十条） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryuserpublished(wallet_username='tests',page=1,num=1)
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 0, u'records': [], u'total': 0}}
```

## 19、根据ID查询资源详情

**描述：**

根据输入查询资源的详细情况。

**方法名：**

*query_resource_by_ID*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| ids | 是    | list | 资源在平台层中的ID列表,字符串列表，入["1"] |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.query_resourc_by_ID(ids=["1","2"])
{u'errcode': 0,
 u'reason': u'success',
 u'result': [{u'author': u'ulord',
              u'claim_id': u'6af5772b0887ce1a92b0123d4c8e098b2d73ad55',
              u'content_type': u'.txt',
              u'create_timed': u'2018-06-06 17:35:22',
              u'create_timed_timestamp': 1528277722,
              u'currency': u'UT',
              u'des': u'\u63aa\u65bd\u4e0d\u65ad\u52a0\u7801\uff0c\u529b\u5ea6\u4e0d\u65ad\u52a0\u5927\uff0c\u91ca\u653e\u4fdd\u62a4\u77e5\u8bc6\u4ea7\u6743\u7684\u5f3a\u70c8\u51b3\u5fc3\u4e0e\u4fe1\u5fc3\uff0c\u8d4b\u4e88\u521b\u65b0\u53d1\u5c55\u4e4b\u821f\u66f4\u52a0\u5f3a\u5927\u7684\u8fdc\u822a\u52a8\u529b',
              u'enabled': True,
              u'id': 1,
              u'price': 0.01,
              u'status': 1,
              u'tags': [u'\u77e5\u8bc6\u4ea7\u6743',
                        u'\u4eba\u6c11\u7f51',
                        u'\u4eba\u6c11\u65e5\u62a5'],
              u'title': u'\u4fdd\u62a4\u77e5\u8bc6\u4ea7\u6743\uff0c\u51dd\u805a\u521b\u65b0\u529b\u91cf\uff08\u8bc4\u8bba\u5458\u89c2\u5bdf\uff09',
              u'update_timed': None,
              u'update_timed_timestamp': None},
             {u'author': u'yinhaibo',
              u'claim_id': u'b357caf6f6de4ab68334ea8ebc661323d3dc8e2a',
              u'content_type': u'.txt',
              u'create_timed': u'2018-06-06 18:20:53',
              u'create_timed_timestamp': 1528280453,
              u'currency': u'UT',
              u'des': u'Node.js Programmer Need',
              u'enabled': True,
              u'id': 2,
              u'price': 0.001,
              u'status': 1,
              u'tags': [u'node.js'],
              u'title': u'Hello, Node.js Programmer, We need you!',
              u'update_timed': None,
              u'update_timed_timestamp': None}]}
```

## 20、根据ID查询交易详情

**描述：**

根据输入查询资源的交易情况。

**方法名：**

*queryBillingDetailByID*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| claim_id | 是 | string | 资源在链上的ID（claim\_id） |
| page | 否 | int | 第几页（默认为第一页） |
| num | 否 | int | 每页多少条数据（默认十条） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryBillingDetailByID(claim_id='6af5772b0887ce1a92b0123d4c8e098b2d73ad55', page=1,num=1)
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 5,
             u'records': [{u'create_timed': u'2018-07-21 09:06:09',
                           u'create_timed_timestamp': 1532135169,
                           u'customer': u'tests',
                           u'price': 0.01,
                           u'txid': u'90035d39e4a8dd65c378efb033a003f3adc2ead7595695225b149f96e26e5415'}],
             u'total': 5}}
```

## 21、根据ID查询单资源消费情况

**描述：**

根据输入查询资源的消费情况。

**方法名：**

*queryStatisticsByID*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| claim_ids | 是 | list | 资源在链上的ID（claim\_id）列表 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryStatisticsByID(claim_ids=['6af5772b0887ce1a92b0123d4c8e098b2d73ad55'])
{u'errcode': 0,
 u'reason': u'success',
 u'result': [{u'claim_id': u'6af5772b0887ce1a92b0123d4c8e098b2d73ad55',
              u'count': 5,
              u'sum': 0.05}]}
```

## 22、查询收入账单

**描述：**

根据输入查询这段时间收入账单，收入类型为0，1，2。对应类型为普通资源，广告，以及所有。

**方法名：**

*queryincomebillings*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| author | 是    | string | 作者钱包名 |
| start | 是    | string | 开始时间 |
| end | 是    | string | 结束时间 |
| page | 否  | string | 第几页（默认第一页） |
| num | 否  | string | 每页显示多少条数据（默认10条） |
| category | 否  | string | 收入类型（默认为2） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryincomebillings(
        author='tests',
        start='2018-03-29',
        end='2018-07-21'
    )
{u'reason': u'success', u'errcode': 0, u'result': {u'records': [], u'total': 0, u'pages': 0}}
```

## 23、查询支出账单

**描述：**

根据输入查询这段时间支出账单，收入类型为0，1，2。对应类型为普通资源，广告，以及所有。

**方法名：**

*queryoutgobillings*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| author | 是    | string | 作者钱包名 |
| start | 是    | string | 开始时间 |
| end | 是    | string | 结束时间 |
| page | 否  | string | 第几页（默认第一页） |
| num | 否  | string | 每页显示多少条数据（默认10条） |
| category | 否  | string | 收入类型（默认为2） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.queryoutgobillings(
        author='tests',
        start='2018-03-29',
        end='2018-07-21'
    )
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 1,
             u'records': [{u'author': u'ulord',
                           u'claim_id': u'6af5772b0887ce1a92b0123d4c8e098b2d73ad55',
                           u'create_timed': u'2018-07-21 09:06:09',
                           u'create_timed_timestamp': 1532135169,
                           u'customer': u'tests',
                           u'price': 0.01,
                           u'title': u'\u4fdd\u62a4\u77e5\u8bc6\u4ea7\u6743\uff0c\u51dd\u805a\u521b\u65b0\u529b\u91cf\uff08\u8bc4\u8bba\u5458\u89c2\u5bdf\uff09',
                           u'txid': u'90035d39e4a8dd65c378efb033a003f3adc2ead7595695225b149f96e26e5415'}],
             u'total': 1}}
```

## 24、查询收支账单详情

**描述：**

根据输入查询收支账单详情。

**方法名：**

*querybillingsdetail*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| author | 是    | string | 作者钱包名 |
| page | 否   | string | 第几页（默认第一页） |
| num | 否    | string | 每页显示多少条数据（默认10条） |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.querybillingsdetail(
        author='tests'
    )
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'pages': 1,
             u'records': [{u'author': u'ulord',
                           u'claim_id': u'6af5772b0887ce1a92b0123d4c8e098b2d73ad55',
                           u'create_timed': u'2018-07-21 09:06:09',
                           u'create_timed_timestamp': 1532135169,
                           u'customer': u'tests',
                           u'price': 0.01,
                           u'title': u'\u4fdd\u62a4\u77e5\u8bc6\u4ea7\u6743\uff0c\u51dd\u805a\u521b\u65b0\u529b\u91cf\uff08\u8bc4\u8bba\u5458\u89c2\u5bdf\uff09',
                           u'txid': u'90035d39e4a8dd65c378efb033a003f3adc2ead7595695225b149f96e26e5415'}],
             u'total': 1}}
```

## 25、查询收支账单概览

**描述：**

根据输入查询这段时间内的收支账单概览。

**方法名：**

*querybillings*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是    | string | 作者钱包名 |
| start | 是    | string | 开始时间 |
| end | 是    | string | 结束时间 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.querybillings(
        username='tests',
        start='2018-03-29',
        end='2018-07-21'
    )
{u'errcode': 0,
 u'reason': u'success',
 u'result': {u'customer_in': {u'count': 0, u'sum': None},
             u'customer_out': {u'count': 1, u'sum': 0.01},
             u'publisher_in': {u'count': 0, u'sum': None},
             u'publisher_out': {u'count': 0, u'sum': None}}}
```

## 26、已发布资源总数

**描述：**

根据输入查询这段时间内的已发布的资源总数。

**方法名：**

*querypublishnum*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| author | 是    | string | 作者钱包名 |
| start | 是    | string | 开始时间 |
| end | 是    | string | 结束时间 |

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层json结果 |

**代码示例：**

```py
>>>develop.querypublishnum(
        author='tests',
        start='2018-03-29',
        end='2018-07-21'
    )
{u'errcode': 0, u'reason': u'success', u'result': {u'count': 1}}
```

# 三、初级开发者接口

初级开发者接口继承与中级开发者接口，故中级开发者的所有接口初级开发者均可使用。初级开发者与中级开发者的主要区别在于为初级开发者提供了一些基本的数据库结构存储，一些接口调用直接使用内置的数据库去调用，是开发者可以快速开发简单应用，如果需要更复杂的数据结构则需要使用中级开发者创建自己的数据库，或者直接修改SDK的内容丰富自己的数据库结构。

加密部分采用RSA加密，公私钥自动生成，也可以第三方生成在配置文件中指定到对应的公私钥文件地址。

## 27、用户注册

**描述：**

根据输入注册新用户。

**方法名：**

*user_regist*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是    | string | 用户名 |
| password | 是    | string | 密码 |
| cellphone | 否  | string | 手机号（默认为空） |
| email | 否    | string | 邮箱（默认为空） |
| wallet |否  | string | 钱包名（默认和用户名相同） |
| pay_password | 否  | string | 钱包密码（默认和密码相同）|
| encrypted | 否    | string | 密码是否加密（默认不加密）|

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功返回用户有效登录的token。错误则返回平台层创建钱包错误。 |

**代码示例：**

```py
>>>junior = Junior(
        appkey='8326648868ad11e8b894fa163e37b4c3',
        secret='8326648968ad11e8b894fa163e37b4c3'
    )
    junior.create_database()
    junior.user_regist(
        username='3',
        password='1'
    )
```

## 28、用户登录

**描述：**

根据输入登录。

**方法名：**

*user_login*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是    | string | 用户名 |
| password | 是    | string | 密码 |
| encrypted | 否    | string | 密码是否加密（默认不加密）|

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功返回用户有效登录的token。错误则返回对应的错误码。 |

**代码示例：**

```py
>>>junior.user_login(
        username='3',
        password='1'
    )
{'errcode': 0,
 'reason': 'success',
 'result': {'token': u'2b94fd00-8c8a-11e8-920b-f48e388c65be'}}
```

## 29、用户登出

**描述：**

根据输入查询这段时间内的已发布的资源总数。

**方法名：**

*user_logout*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| token | 是/否    | string | token（默认为none） |
| username | 否/是    | string | username（默认为none） |

（token与username需要填写一个即可。）

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功则返回用户名，错误则返回对应的错误码。|

**代码示例：**

```py
>>>junior.user_logout(
        token='2b94fd00-8c8a-11e8-920b-f48e388c65be'
    )
{'reason': 'success', 'errcode': 0, 'result': {'username': u'3'}}
```

## 30、优惠活动

**描述：**

根据输入给用户赠送一定数量的ulord。由开发者账户赠送，数量可以在配置文件中修改，默认为10个。

**方法名：**

*user_activity*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| token | 是/否    | string | token（默认为none） |
| username | 否/是    | string | username（默认为none） |

（token与username需要填写一个即可。）

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功则返回优惠赠送的ulord数量，错误则返回对应的错误码。|

**代码示例：**

```py
>>>junior.user_activity(
        token='7fa38b00-8c8a-11e8-8085-f48e388c65be'
    )
{'reason': 'success', 'errcode': 0, 'result': {'username': u'3'}}
```

## 31、资源发布

**描述：**

根据输入发布资源，将资源上链。

**方法名：**

*resource_publish*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| title | 是    | string | 资源标题|
| udfshash | 是    | string | 资源的udfs哈希值 |
| amount | 是    | string | 定价价格|
| tags | 是    | string | 资源标签列表 |
| des | 是    | string | 资源描述|
| usercondition | 是    | dict | 用户条件 |

(用户条件为一个字典，key值可以为userid，username或usertoken，根据其中之一在本地数据库查找对应用户)

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层资源发布json结果|

**代码示例：**

```py
略
```

## 32、资源更新

**描述：**

根据输入更新对应资源。根据传入的参数更新对应的字段。

**方法名：**

*resource_update*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| id | 是    | string | 资源在平台层中的ID|
| pay_password | 是    | string | 用户钱包密码 |
| encrypted | 是    | string | 密码是否加密（默认加密）|
| title | 是    | string | 标题（默认为空） |
| body | 是    | string | 内容（默认为空）|
| price | 是    | dict | 价格（默认为空） |
| tags | 是    | dict | 标签列表（默认为空）|
| des | 是    | string | 资源描述（默认为空） |

(根据后面的参数更新资源的对应值。为空则不更新该字段。)

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层更新资源的json结果|

**代码示例：**

```py
略
```

## 33、添加资源访问量

**描述：**

根据输入向资源的访问量增加1。

**方法名：**

*resouce_views*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| title | 是    | string | 资源标题|

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 资源的访问量|

**代码示例：**

```py
略
```

## 34、支付资源

**描述：**

根据输入支付资源以获取资源的udfs哈希值。

**方法名：**

*pay_resources*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| payer | 是    | string | 用户类|
| claim_id | 是    | string | 资源在链上的ID（claim\_id）|
| password | 是    | string | 用户密码(不是钱包密码)|
| encrypted | 否   | string | 密码是否加密（默认不加密）|

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层支付接口json结果|

**代码示例：**

```py
略
```

## 35、支付广告

**描述：**

根据输入支付广告，作者对用户进行支付。

**方法名：**

*pay_ads*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是    | string | 用户钱包名|
| userid | 是    | string | 资源在链上的ID|
| usertoken | 是    | string | 作者名|

(根据后面的参数更新资源的对应值。为空则不更新该字段。)

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 平台层支付接口json结果|

**代码示例：**

```py
略
```

## 36、用户信息查询

**描述：**

根据输入查询用户信息。注意，数据库中密码为密文存储，故不可知密码。所以无法返回。

**方法名：**

*user_info_query*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是/否 | string | 用户名（默认为none）|
| token | 否/是 | string | token（默认为none）|

(根据后面的参数更新资源的对应值。为空则不更新该字段。)

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功则返回用户用户名、手机、邮箱，失败则返回对应的错误码。|

**代码示例：**

```py
>>>junior.user_info_query(
        username='3'
    )
{'errcode': 0,
 'reason': 'success',
 'result': {'Email': None, 'cellphone': u'15237548624', 'username': u'3'}}
```

## 37、用户信息修改

**描述：**

根据输入中的用户名或者token（二者传一个即可）查询出对应的用户信息，然后根据传入的参数修改对应值，不传或传空则表示不修改。

**方法名：**

*user_infor_modify*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| username | 是/否 | string | 用户名（默认为none,username与token需要其中一个）|
| token | 否/是 | string | token（默认为none，username与token需要其中一个）|
| encrypted | 否 | string | 密码是否加密（默认不加密,对新旧密码均加密）|
| password | 是 | string | 用户密码（默认为空）|
| cellphone | 否 | string | 手机号（默认为空）|
| email | 否 | string | 邮箱（默认为空）|
| new_password | 否 | string | 新密码（默认为空）|

(根据后面的参数更新资源的对应值。为空则不更新该字段。)

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | 成功则修改后的用户名、手机、邮箱，失败则返回对应的错误码。|

**代码示例：**

```py
>>>junior.user_infor_modify(
        username='3',
        password='1',
        cellphone='15237548624'
    )
{'errcode': 0,
 'reason': 'success',
 'result': {'Email': None, 'cellphone': u'15237548624', 'username': u'3'}}
```

## 38、创建数据库

**描述：**

创建数据库

**方法名：**

*create_database*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| args | 否 | string | 数据库地址(默认为空，地址为角色初始化文件位置)|

**返回说明：**

无

**代码示例：**

```py
>>>junior.create_database()
```

## 39、开启web

**描述：**

开启web服务。

**方法名：**

*start_web*

**参数：**

无

**返回说明：**

无

**代码示例：**

```py
>>>junior.start_web()
```

**备注：**
　启动守护进程

## 40、高级查询

**描述：**

根据输入对数据库执行操作。

**方法名：**

*query*

**参数：**

| 参数名  | 必选   | 类型     | 说明   |
| ---- | ---- | ------ | ---- |
| sql | 是 | string | sql语句|

**返回说明：**

| 类型   | 说明          |
| ---- | ----------- |
| json  | sql执行结果|

**代码示例：**

```py
>>> result = junior.query("select * from users ")
>>> for  i in result:
        print(i)
(u'81d79e81-8c89-11e8-9b83-f48e388c65be', u'3', u'$5$rounds=535000$BVxw4KDybwsFKIjW$AvOv7D1QCogO5G7ZD04cb3sIn4t3Jz5oDR4HDUkUy9B', None, None, u'7fa38b00-8c8a-11e8-8085-f48e388c65be', u'1532225110', None, u'3', u'$5$rounds=535000$BVxw4KDybwsFKIjW$AvOv7D1QCogO5G7ZD04cb3sIn4t3Jz5oDR4HDUkUy9B', 0.0)

```
