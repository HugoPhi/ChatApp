
// 从 localStorage 获取登录状态
let signed_up = localStorage.getItem("signed_up") === "true";
let currentUserName = localStorage.getItem("currentUserName");

// 当前聊天环境（默认示例）
let currentChat = { type: 'user', name: 'Chat Name' };

// 页面加载时检查登录状态
document.addEventListener("DOMContentLoaded", () => {
    if (!signed_up || !currentUserName) {
        window.location.href = "index.html"; // 未登录则重定向到登录页面
    } else {
        loadUserGroupLists(); // 加载用户和群组列表
        loadMessages();       // 加载聊天消息
    }

    // 绑定发送按钮点击事件
    document.getElementById("send-btn").addEventListener("click", sendMessage);
});

// Log Out 按钮点击事件
document.getElementById("logout-btn").addEventListener("click", () => {
    // 清除 localStorage 中的登录状态
    localStorage.removeItem("signed_up");
    localStorage.removeItem("currentUserName");
    localStorage.removeItem("serverIp");

    // 重定向到登录页面
    window.location.href = "index.html";
});

// 发送消息到后端
function sendMessage() {
    const messageContent = document.getElementById("message-input").value.trim();
    if (!messageContent) {
        alert("Please enter a message to send.");
        return;
    }

    // 准备发送的数据
    const messageData = {
        source: currentUserName,
        target: currentChat.name,
        message: messageContent,
        message_type: currentChat.type === 'user' ? "personal" : "group",
        type: "text"
    };

    // 调试信息
    console.log("Sending message data:", messageData);

    // 向后端发送消息
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(messageData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Message sent:", data);
        document.getElementById("message-input").value = ""; // 清空输入框
        loadMessages(); // 刷新消息列表
    })
    .catch(error => console.error('Error sending message:', error));
}

// 加载用户列表和群组列表
function loadUserGroupLists() {
    fetch('data/users.csv')
        .then(response => response.text())
        .then(text => {
            const users = parseCSV(text);
            displayUserList(users);
        })
        .catch(error => console.error('Error loading users:', error));

    fetch('data/groups.csv')
        .then(response => response.text())
        .then(text => {
            const groups = parseCSV(text);
            displayGroupList(groups);
        })
        .catch(error => console.error('Error loading groups:', error));
}

// 显示用户列表
function displayUserList(users) {
    const usersList = document.getElementById('users');
    usersList.innerHTML = '';

    const currentUserLi = document.createElement('li');
    currentUserLi.textContent = currentUserName;
    currentUserLi.classList.add('current-user');
    usersList.appendChild(currentUserLi);

    users.forEach(user => {
        if (user.name !== currentUserName) {
            const li = document.createElement('li');
            li.textContent = user.name;
            li.addEventListener('click', () => switchChat('user', user.name));
            usersList.appendChild(li);
        }
    });
}

// 显示群组列表
function displayGroupList(groups) {
    const groupsList = document.getElementById('groups');
    groupsList.innerHTML = '';

    groups.forEach(group => {
        const li = document.createElement('li');
        li.textContent = group.name;

        // 如果群组是由当前用户创建，应用特定样式
        if (group.created_by_user === 'true') {
            li.classList.add('user-created-group');
        }

        li.addEventListener('click', () => switchChat('group', group.name));
        groupsList.appendChild(li);
    });
}

// 加载消息队列
function loadMessages() {
    fetch('data/message.csv')
        .then(response => response.text())
        .then(csvText => {
            const messages = parseCSV(csvText);
            displayMessages(messages);
        })
        .catch(error => console.error('Error loading messages:', error));
}

// 显示消息
function displayMessages(messages) {
    const chatBox = document.querySelector('.messages ul');
    chatBox.innerHTML = ''; // 清空现有消息

    const filteredMessages = messages.filter(msg => {
        if (msg.message_type === 'personal') {
            return (
                currentChat.type === 'user' &&
                ((msg.source === currentUserName && msg.target === currentChat.name) ||
                 (msg.source === currentChat.name && msg.target === currentUserName))
            );
        } else if (msg.message_type === 'group') {
            return currentChat.type === 'group' && msg.target === currentChat.name;
        }
        return false;
    });

    filteredMessages.forEach(msg => {
        const li = document.createElement('li');
        li.className = msg.source === currentUserName ? 'sent' : 'replies';

        // 解析 timestamp 并格式化为用户名、日期和时间
        const timestamp = new Date(msg.timestamp);
        const dateString = timestamp.toLocaleDateString('en-CA'); // 格式为 YYYY-MM-DD
        const timeString = timestamp.toLocaleTimeString('en-GB'); // 格式为 HH:MM:SS
        const userInfo = `${msg.source}, ${dateString}, ${timeString}`;

        // 创建显示用户名、日期和时间的元素
        const infoElement = document.createElement('small');
        infoElement.textContent = userInfo;

        // 添加头像和消息内容
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = msg.source[0]; // 显示首字母

        const messageContent = document.createElement('p');

        // 根据消息类型动态显示内容
        if (msg.type === 'text') {
            messageContent.textContent = msg.content;
        } else if (msg.type === 'file') {
            // 仅显示文件名
            const fileName = msg.content.split('/').pop(); // 提取文件名
            const fileLink = document.createElement('a');
            fileLink.href = `data/file/${msg.content}`;
            fileLink.textContent = fileName;
            fileLink.target = "_blank";
            messageContent.appendChild(fileLink);
        } else if (msg.type === 'picture') {
            // 仅显示图片文件名，点击可查看图片
            const imageName = msg.content.split('/').pop(); // 提取图片文件名
            const imageLink = document.createElement('a');
            imageLink.href = `data/picture/${msg.content}`;
            imageLink.textContent = imageName;
            imageLink.target = "_blank";

            const image = document.createElement('img');
            image.src = `data/picture/${msg.content}`;
            image.alt = `Image: ${imageName}`;
            image.style.maxWidth = "200px"; // 限制图片最大宽度

            messageContent.appendChild(imageLink); // 显示图片文件名作为链接
            messageContent.appendChild(document.createElement('br')); // 换行
            messageContent.appendChild(image); // 显示图片
        }

        // 将用户信息放在消息内容的上方
        messageContent.appendChild(infoElement);

        // 根据消息方向调整位置
        if (li.className === 'sent') {
            li.appendChild(messageContent);
            li.appendChild(avatar);
        } else {
            li.appendChild(avatar);
            li.appendChild(messageContent);
        }

        chatBox.appendChild(li);
    });
}

// 切换聊天环境
function switchChat(type, name) {
    currentChat = { type, name };
    document.querySelector('.contact-profile p').textContent = name;
    loadMessages();
}

// 群组管理按钮跳转
document.getElementById("group-settings-btn").addEventListener("click", function() {
    window.location.href = "group_management.html";
});

// 解析 CSV 数据
function parseCSV(csvText) {
    const parsedData = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true
    });
    return parsedData.data;
}
