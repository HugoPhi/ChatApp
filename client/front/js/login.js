let currentUserName = "";

// 处理登录表单提交
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // 获取用户输入的信息
    const serverIp = document.getElementById("serverIp").value;
    const serverPort = document.getElementById("serverPort").value;
    currentUserName = document.getElementById("username").value;

    // 构造请求数据
    const loginData = {
        username: currentUserName,
        server_ip: serverIp,
        server_port: serverPort
    };

    // 向后端发送登录请求
    fetch('/login', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // 登录成功，保存状态到 localStorage
            localStorage.setItem("signed_up", "true");
            localStorage.setItem("currentUserName", currentUserName);
            localStorage.setItem("serverIp", serverIp);
            localStorage.setItem("serverPort", serverPort);

            // 重定向到主聊天页面
            window.location.href = "main.html";
        } else {
            // 显示登录失败信息
            document.getElementById("loginMessage").textContent = data.message;
        }
    })
    .catch(error => {
        console.error("Login failed:", error);
        document.getElementById("loginMessage").textContent = "Failed to login. Please try again.";
    });
});
