# ChatApp

TODO List:

```
.
├── utils
│   └── core.py (#1)
├── client
│   ├── front
│   │   ├── css
│   │   │   ├── group_management.css (*)
│   │   │   ├── login.css
│   │   │   ├── main.css
│   │   │   └── style.css
│   │   ├── data
│   │   │   ├── file
│   │   │   │   └── files
│   │   │   ├── picture
│   │   │   │   └── pictures
│   │   │   ├── groups.csv
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
│   ├── ServerDatabase.py (*)
│   ├── ServerNetwork.py (*)
│   └── ServerManager.py (*, #3)
├── setup.py (#2)
├── .gitignore (#4)
├── LICENSE
└── README.md
```

- = TODO all
  #DOING = 按照数据包格式写入本地消息队列，这里不用保存文件因为这是CB-NetWork的任务。
  #1 = test CMD sent of networkCore
  #2 = 将这里做成命令行交互式入口，根据传入参数确定启动服务器or客户端。
  #3 = 将用户更新命令省去，用Server发出的json流代替传输(json: 减少读写文件带来的磁盘IO，因为要根据不同的用户确定不同的群组发送内容)。
  #4 = remove dir 'data' in client/front
