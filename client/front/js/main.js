
// From localStorage, retrieve login status and username
let signed_up = localStorage.getItem("signed_up") === "true";
let currentUserName = localStorage.getItem("currentUserName");

// Current chat environment (default example)
let currentChat = { type: 'user', name: 'Chat Name' };

// Check login status on page load
document.addEventListener("DOMContentLoaded", () => {
    if (!signed_up || !currentUserName) {
        window.location.href = "index.html"; // Redirect to login page if not logged in
    } else {
        loadUserGroupLists(); // Load user and group lists
        loadMessages();       // Load chat messages
    }

    // Bind send button click event
    document.getElementById("send-btn").addEventListener("click", sendMessage);
    document.getElementById("file-input").addEventListener("change", () => sendFileOrPicture("file"));
    document.getElementById("picture-input").addEventListener("change", () => sendFileOrPicture("picture"));

    // Log Out button click event
    document.getElementById("logout-btn").addEventListener("click", () => {
        localStorage.removeItem("signed_up");
        localStorage.removeItem("currentUserName");
        localStorage.removeItem("serverIp");
        window.location.href = "index.html"; // Redirect to login page
    });

    document.getElementById("group-settings-btn").addEventListener("click", () => {
        window.location.href = "group_management.html"
    })
});


// Send message to backend
function sendMessage() {
    const messageContent = document.getElementById("message-input").value.trim();
    if (!messageContent) {
        alert("Please enter a message to send.");
        return;
    }

    // Prepare data to send
    const messageData = {
        source: currentUserName,
        target: currentChat.name,
        message: messageContent,
        message_type: currentChat.type === 'group' ? "group" : "personal",
        type: "text"
    };

    console.log("Sending message data:", messageData);

    // Send message to backend
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
            document.getElementById("message-input").value = ""; // Clear input field
            loadMessages(); // Refresh messages
        })
        .catch(error => console.error('Error sending message:', error));
}

// Load user and group lists
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

// Display user list
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

// Display group list
function displayGroupList(groups) {
    const groupsList = document.getElementById('groups');
    groupsList.innerHTML = '';

    groups.forEach(group => {
        const li = document.createElement('li');
        li.textContent = group.name;

        if (group.created_by_user === 'true') {
            li.classList.add('user-created-group');
        }

        li.addEventListener('click', () => switchChat('group', group.name));
        groupsList.appendChild(li);
    });
}

// Load message queue
function loadMessages() {
    fetch('data/message.csv')
        .then(response => response.text())
        .then(csvText => {
            const messages = parseCSV(csvText);
            displayMessages(messages);
        })
        .catch(error => console.error('Error loading messages:', error));
}

// Display messages
function displayMessages(messages) {
    const chatBox = document.querySelector('.messages ul');
    chatBox.innerHTML = ''; // Clear existing messages

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

        const timestamp = new Date(msg.timestamp);
        const dateString = timestamp.toLocaleDateString('en-CA');
        const timeString = timestamp.toLocaleTimeString('en-GB');
        const userInfo = `${msg.source}, ${dateString}, ${timeString}`;

        const infoElement = document.createElement('small');
        infoElement.textContent = userInfo;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = msg.source[0];

        const messageContent = document.createElement('p');

        if (msg.type === 'text') {
            messageContent.textContent = msg.content;
        } else if (msg.type === 'file') {
            const fileName = msg.content.split('/').pop();
            const fileLink = document.createElement('a');
            fileLink.href = `data/file/${msg.content}`;
            fileLink.textContent = fileName;
            fileLink.target = "_blank";
            messageContent.appendChild(fileLink);
        } else if (msg.type === 'picture') {
            const imageName = msg.content.split('/').pop();
            const imageLink = document.createElement('a');
            imageLink.href = `data/picture/${msg.content}`;
            imageLink.textContent = imageName;
            imageLink.target = "_blank";

            const image = document.createElement('img');
            image.src = `data/picture/${msg.content}`;
            image.alt = `Image: ${imageName}`;
            image.style.maxWidth = "200px";

            messageContent.appendChild(imageLink);
            messageContent.appendChild(document.createElement('br'));
            messageContent.appendChild(image);
        }

        messageContent.appendChild(infoElement);

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

// Switch chat
function switchChat(type, name) {
    currentChat = { type, name };
    document.querySelector('.contact-profile p').textContent = name;
    loadMessages();
}

// Parse CSV data
function parseCSV(csvText) {
    const parsedData = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true
    });
    return parsedData.data;
}

// Send file or picture
function sendFileOrPicture(type) {
    const input = type === "file" ? document.getElementById("file-input") : document.getElementById("picture-input");
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("source", currentUserName);
    formData.append("target", currentChat.name);
    formData.append("type", type);
    formData.append("message_type", currentChat.type);

    const endpoint = type === "file" ? "/send_file" : "/send_picture";

    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(`${type.charAt(0).toUpperCase() + type.slice(1)} sent:`, data);
            loadMessages();
            input.value = ""; // Reset file input
        })
        .catch(error => console.error('Error uploading:', error));
}
