# ChatApp

## 展示

![show](./assets/show.gif)

## TODO

TODO List:

```cpp
.
├── utils
│   └── core.py (#1)
├── client
│   ├── (ignored)data(#New，存放记录数据库)
│   │   └── ${USER NAME}
│   ├── front
│   │   ├── css
│   │   │   ├── group_management.css (*)
│   │   │   ├── login.css
│   │   │   ├── main.css
│   │   │   └── style.css
│   │   ├── (ignored)data
│   │   │   ├── file
│   │   │   │   └── files
│   │   │   ├── picture
│   │   │   │   └── pictures
│   │   │   ├── groups.csv
│   │   │   ├── current_groups.csv (#New，存放当前所有的群组名，用于加入权@1)
│   │   │   ├── message.csv
│   │   │   └── users.csv
│   │   ├── js
│   │   │   ├── group_management.js (*)
│   │   │   ├── login.js
│   │   │   └── main.js
│   │   ├── group_management.html (*)
│   │   ├── index.html
│   │   └── main.html
│   ├── ClientDatabase.py (#DOING)
│   ├── ClientNetwork.py (*)
│   └── ClientManager.py (*)
├── server
│   ├── (ignored)data(New，存放记录数据库)
│   │   └── ${USER NAME}
│   ├── ServerDatabase.py (*)
│   ├── ServerNetwork.py (*)
│   └── ServerManager.py (*, #3)
├── setup.py (#2)
├── .gitignore
├── LICENSE
└── README.md
```

```c
* = TODO all

#New = 新添加的部分
#DOING = 按照数据包格式写入本地消息队列，这里不用保存文件因为这是CB-NetWork的任务。
#1:(@1) = 把命令做成枚举类
#2:(all) = 完善交互式命令行入口。
#3 = 将用户更新命令省去，用Server发出的json流代替传输(json: 减少读写文件带来的磁盘IO，
     因为要根据不同的用户确定不同的群组发送内容)。

@1 = 聊天室模型：
   1，聊天室设置密码。
   2，聊天室只有创建权，销毁权（创建者）和进出权（所有人），没有编辑权「主动使人加入的权限」。
   3，只有一个人有所有权，可以主动转移；
      在所有者退出的时候会自动从用户列表中选取一个人来继承权限；
      如果群组没有人会被自动销毁。
   4，公共聊天室无密码，所有用户可无密码加入，所有人不具有所有权。
   5，（创建权）：添加在线成员；设置密码（不可以空）；设置聊天室名称（不可以空）；
      （销毁权）：删除聊天室。
   7，（进出权）：加入，退出聊天室。
@2 = 完善错误处理列表。

%1(release v1.0.0): 完善文档
```
