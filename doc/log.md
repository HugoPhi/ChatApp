# branch front

## 2024.12.05, by Yunming Hu

- \[Bug Fixed] main里面的左边侧栏和顶部栏在字体太多或不是Mono的时候容易被压缩。用CSS设置成固定。
```css
#sidepanel {
  width: 350px;
  flex-shrink: 0; /* 禁止缩小 */
  background: #ecf0f1;
  background-image: url("../assets/pictures/3.png");
  background-size: cover;
  color: #333;
  overflow-y: auto;
  padding: 20px;
  border-right: 2px solid #000;
}
```
- \[Bug Fixed] 右边用户的聊天框的文字右边对齐改成左对齐。
- \[Code Format] 把所有的字体放在一个文件里面，方便管理；同时定义全局字体。
- \[New Function] 增加了一个搜索功能，可以在群聊列表中搜索群聊。只支持全匹配。
- \[New Function] 做了group_manager的前端部分，主要设计思想如下：
1，顶层三个按钮:创建群聊，加入群聊，退出群聊
2，当前群聊列表用列表的形式显示出来，每一项中间是Quit, Join, Delete，Transform Ownership，
最后显示public/private.
3，新加了一个数据库：
在线群聊列表：./data/current_groups.csv，包含两个字段：name,type(public/private).
