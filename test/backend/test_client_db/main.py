from ClientDatabase import dops
import core

db = dops(dbpath="./db/")

db.write_message({
    'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
    'source': "ZQX",  # Sender's nickname
    'target': "ChatBox",  # Receiver's nickname
    'timestamp': "2024-12-05T13:46:04.462684",  # Timestamp
    'message_type': "group",  # "single" or "group"
    'content': "hello"  # Message content
})

db.write_message({
    'type': core.FullDuplex.ProtocalHead.FILE,  # Message type
    'source': "ZQX",  # Sender's nickname
    'target': "ChatBox",  # Receiver's nickname
    'timestamp': "2024-12-05T13:46:13.479885",  # Timestamp
    'message_type': "group",  # "single" or "group"
    'content': "./pictures/show.gif"  # Message content
})

# db.write_message({
#     'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
#     'source': "Yunming Hu",  # Sender's nickname
#     'target': "Public",  # Receiver's nickname
#     'timestamp': "2024-12-05T15:44:24.666147",  # Timestamp
#     'message_type': "group",  # "single" or "group"
#     'content': "公式范德萨发送实得分数大幅度萨菲士大夫实得分数的分尸案分身乏术方式方法士大夫撒旦放大算法撒放大说法的三番四复大师傅第三方额附加阿斯顿里飞鸟时代封建时代卡拉福克斯的参数拿出来你积分考虑到萨满蚕蛾农夫呢为您服务那里积分卡拉三年搭茬儿；。发送单发"  # Message content
# })

db.write_message({
    'type': core.FullDuplex.ProtocalHead.IMAGE,  # Message type
    'source': "Yunming Hu",  # Sender's nickname
    'target': "Public",  # Receiver's nickname
    'timestamp': "2024-12-05T15:51:54.684300",  # Timestamp
    'message_type': "group",  # "single" or "group"
    'content': "./pictures/develop.gif"  # Message content
})

db.write_message({
    'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
    'source': "Yunming Hu",  # Sender's nickname
    'target': "ChatBox",  # Receiver's nickname
    'timestamp': "2024-12-05T16:02:50.648827",  # Timestamp
    'message_type': "group",  # "single" or "group"
    'content': "hello"  # Message content
})

db.write_message({
    'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
    'source': "Yunming Hu",  # Sender's nickname
    'target': "ChatBox",  # Receiver's nickname
    'timestamp': "2024-12-05T16:07:58.434143",  # Timestamp
    'message_type': "group",  # "single" or "group"
    'content': "hello"  # Message content
})
