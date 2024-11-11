document.addEventListener("DOMContentLoaded", () => {
    const signedUp = localStorage.getItem("signed_up") === "true";
    if (!signedUp) {
        window.location.href = "index.html";
    } else {
        loadGroupManagement();
    }
});

// 加载群组管理内容
function loadGroupManagement() {
    fetch('groups.csv')
        .then(response => response.text())
        .then(text => {
            const groups = parseCSV(text);
            const groupContainer = document.getElementById('group-management-content');
            groupContainer.innerHTML = '';

            groups.forEach(group => {
                const div = document.createElement('div');
                div.textContent = group.name;
                groupContainer.appendChild(div);
            });
        });
}

// 返回主聊天页面
document.getElementById("back-to-chat").addEventListener("click", function() {
    window.location.href = "main.html";
});
