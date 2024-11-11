
let signed_up = false;
let currentUserName = "";

// 处理登录表单提交
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const serverIp = document.getElementById("serverIp").value;
    currentUserName = document.getElementById("username").value;

    registerUser(serverIp, currentUserName);
});


// 注册用户（模拟成功注册）
function registerUser(serverIp, username) {
    setTimeout(() => {
        signed_up = true;
        currentUserName = username;

        // 将状态存储到 localStorage
        localStorage.setItem("signed_up", "true");
        localStorage.setItem("currentUserName", currentUserName);
        localStorage.setItem("serverIp", serverIp);

        // 重定向到主聊天页面
        window.location.href = "main.html";
        console.log("Registered successfully (simulated)");
    }, 1000); // 模拟延迟1秒
}
