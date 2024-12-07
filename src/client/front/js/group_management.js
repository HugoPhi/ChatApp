// group_management.js

let allGroups = []; // 全局变量用于存储所有群组数据

// Parse simple CSV data into JSON objects
function parseCSV(data) {
    const lines = data.trim().split('\n');
    const headers = lines[0].split(',').map(header => header.trim());
    const result = [];

    for (let i = 1; i < lines.length; i++) {
        // Skip empty lines
        if (lines[i].trim() === '') continue;

        const obj = {};
        const currentline = lines[i].split(',').map(item => item.trim());

        headers.forEach((header, index) => {
            obj[header] = currentline[index] || '';
            // Handle specific fields
            if (header === 'members' && obj[header]) {
                obj[header] = obj[header].split(';').map(member => member.trim());
            }
        });

        result.push(obj);
    }

    return result;
}

// Get the current user (set to the last line of users.csv)
async function getCurrentUser() {
    try {
        const response = await fetch('data/users.csv');
        if (!response.ok) {
            throw new Error('Failed to fetch users.csv');
        }
        const text = await response.text();
        const users = parseCSV(text);
        if (users.length === 0) {
            return 'Anonymous';
        }
        return users[users.length - 1].name; // Set to the last user
    } catch (error) {
        console.error('Error fetching users:', error);
        return 'Anonymous';
    }
}

// Render the group list based on provided groups
function renderGroupList(groups, currentUser, groupTypes, groupOwners) {
    const groupContainer = document.getElementById('groups-ul');
    groupContainer.innerHTML = '';

    if (groups.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No groups found.';
        groupContainer.appendChild(li);
        return;
    }

    groups.forEach(group => {
        const groupName = group.name;
        const groupType = groupTypes[groupName] || 'public'; // Default to public

        const owner = groupOwners[groupName] || 'Unknown';
        const isPublic = groupType === 'public';
        const isOwner = owner === currentUser;

        const li = document.createElement('li');

        // Pad group name to 15 characters
        let paddedGroupName = groupName;
        const STD_LEN = 15;
        paddedGroupName = paddedGroupName.padEnd(STD_LEN, ' ');
        li.textContent = '󰡉  ' + paddedGroupName;
        li.classList.add(isPublic ? 'public' : 'private');

        // Create action buttons container
        const actionsDiv = document.createElement('div');
        actionsDiv.classList.add('group-actions');

        // Add Join button
        const joinBtn = document.createElement('button');
        joinBtn.textContent = 'Join';
        joinBtn.classList.add('btn-join');
        joinBtn.addEventListener('click', () => {
            showJoinGroupFormWithName(groupName);
        });
        actionsDiv.appendChild(joinBtn);

        // Add Quit button
        const quitBtn = document.createElement('button');
        quitBtn.textContent = 'Quit';
        quitBtn.classList.add('btn-quit');
        quitBtn.addEventListener('click', () => {
            showQuitGroupForm(groupName);
        });
        actionsDiv.appendChild(quitBtn);

        // If current user is the group owner, add Delete and Transfer Ownership buttons
        if (isOwner) {
            // Add Delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.classList.add('btn-delete');
            deleteBtn.addEventListener('click', () => {
                showDeleteGroupForm(groupName);
            });
            actionsDiv.appendChild(deleteBtn);

            // Add Transfer Ownership button
            const transferBtn = document.createElement('button');
            transferBtn.textContent = 'Transfer Ownership';
            transferBtn.classList.add('btn-transfer');
            transferBtn.addEventListener('click', () => {
                showTransferOwnershipForm(groupName);
            });
            actionsDiv.appendChild(transferBtn);
        }

        li.appendChild(actionsDiv);
        groupContainer.appendChild(li);
    });
}

// Display the group list
async function loadGroupManagement(searchQuery = '') {
    try {
        const currentUser = await getCurrentUser();

        // Fetch groups.csv
        const groupsResponse = await fetch('data/groups.csv');
        if (!groupsResponse.ok) {
            throw new Error('Failed to fetch groups.csv');
        }
        const groupsText = await groupsResponse.text();
        const groups = parseCSV(groupsText);
        allGroups = groups; // 存储所有群组数据

        // Fetch current_groups.csv
        const currentGroupsResponse = await fetch('data/current_groups.csv');
        if (!currentGroupsResponse.ok) {
            throw new Error('Failed to fetch current_groups.csv');
        }
        const currentGroupsText = await currentGroupsResponse.text();
        const currentGroupsData = parseCSV(currentGroupsText);

        // Create an object to store group types
        const groupTypes = {};
        currentGroupsData.forEach(group => {
            groupTypes[group.name] = group.type.toLowerCase();
        });

        // Create an object to store group owners
        const groupOwners = {};
        groups.forEach(group => {
            groupOwners[group.name] = group.owner;
        });

        // Filter groups based on search query
        let filteredGroups = currentGroupsData;
        if (searchQuery.trim() !== '') {
            const query = searchQuery.trim().toLowerCase();
            filteredGroups = currentGroupsData.filter(group => 
                group.name.toLowerCase().includes(query)
            );
        }

        // Render the filtered group list
        renderGroupList(filteredGroups, currentUser, groupTypes, groupOwners);
    } catch (error) {
        console.error('Error loading group management:', error);
        alert('An error occurred while loading group management.');
    }
}

// Show Create Group Modal
function showCreateGroupForm() {
    document.getElementById('create-group-form').classList.remove('hidden');
}

// Hide Create Group Modal
function hideCreateGroupForm() {
    document.getElementById('create-group-form').classList.add('hidden');
    document.getElementById('create-group').reset();
}

// Show Join Group Modal with pre-filled group name
function showJoinGroupFormWithName(groupName) {
    showJoinGroupForm();
    document.getElementById('join-group-name').value = groupName;
}

// Show Join Group Modal
function showJoinGroupForm() {
    document.getElementById('join-group-form').classList.remove('hidden');
}

// Hide Join Group Modal
function hideJoinGroupForm() {
    document.getElementById('join-group-form').classList.add('hidden');
    document.getElementById('join-group').reset();
}

// Show Quit Group Modal
function showQuitGroupForm(groupName) {
    document.getElementById('quit-group-name').value = groupName;
    document.getElementById('quit-group-display-name').textContent = groupName;
    document.getElementById('quit-group-form').classList.remove('hidden');
}

// Hide Quit Group Modal
function hideQuitGroupForm() {
    document.getElementById('quit-group-form').classList.add('hidden');
    document.getElementById('quit-group').reset();
}

// Show Delete Group Modal
function showDeleteGroupForm(groupName) {
    document.getElementById('delete-group-name').value = groupName;
    document.getElementById('delete-group-display-name').textContent = groupName;
    document.getElementById('delete-group-form').classList.remove('hidden');
}

// Hide Delete Group Modal
function hideDeleteGroupForm() {
    document.getElementById('delete-group-form').classList.add('hidden');
    document.getElementById('delete-group').reset();
}

// Show Transfer Ownership Modal
function showTransferOwnershipForm(groupName) {
    document.getElementById('transfer-group-name').value = groupName;
    document.getElementById('transfer-ownership-form').classList.remove('hidden');
}

// Hide Transfer Ownership Modal
function hideTransferOwnershipForm() {
    document.getElementById('transfer-ownership-form').classList.add('hidden');
    document.getElementById('transfer-ownership').reset();
}

// Handle Create Group
async function handleCreateGroup(event) {
    event.preventDefault();
    const groupName = document.getElementById('group-name').value.trim();
    const groupMaxPeople = document.getElementById('group-max-people').value.trim();
    const groupPassword = document.getElementById('group-password').value.trim();

    if (groupName === '') {
        alert('Group name cannot be empty.');
        return;
    }

    // Send create group request to server
    try {
        const response = await fetch('/api/groups', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // Add Authorization header if needed
            },
            body: JSON.stringify({
                name: groupName,
                password: groupPassword
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Group created successfully.');
            hideCreateGroupForm();
            loadGroupManagement(); // 重新加载群组列表
        } else {
            alert('Error creating group: ' + (data.message || 'Unknown error.'));
        }
    } catch (error) {
        console.error('Error creating group:', error);
        alert('An error occurred while creating the group.');
    }
}

// Handle Join Group
async function handleJoinGroup(groupName) {
    // Send join group request to server
    try {
        const groupPassword = document.getElementById('join-group-password').value.trim();
        const response = await fetch('/api/groups/join', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // Add Authorization header if needed
            },
            body: JSON.stringify({
                name: groupName,
                password: groupPassword // Include if password is required
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Successfully joined the group.');
            hideJoinGroupForm();
            loadGroupManagement(); // 重新加载群组列表
        } else {
            alert('Error joining group: ' + (data.message || 'Unknown error.'));
        }
    } catch (error) {
        console.error('Error joining group:', error);
        alert('An error occurred while joining the group.');
    }
}

// Handle Quit Group
async function handleQuitGroup(groupName) {
    // Send quit group request to server
    try {
        const response = await fetch('/api/groups/quit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // Add Authorization header if needed
            },
            body: JSON.stringify({
                name: groupName
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Successfully quit the group.');
            hideQuitGroupForm();
            loadGroupManagement(); // 重新加载群组列表
        } else {
            alert('Error quitting group: ' + (data.message || 'Unknown error.'));
        }
    } catch (error) {
        console.error('Error quitting group:', error);
        alert('An error occurred while quitting the group.');
    }
}

// Handle Delete Group
async function handleDeleteGroup(groupName) {
    // Send delete group request to server
    try {
        const response = await fetch(`/api/groups/${encodeURIComponent(groupName)}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
                // Add Authorization header if needed
            }
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Group deleted successfully.');
            hideDeleteGroupForm();
            loadGroupManagement(); // 重新加载群组列表
        } else {
            alert('Error deleting group: ' + (data.message || 'Unknown error.'));
        }
    } catch (error) {
        console.error('Error deleting group:', error);
        alert('An error occurred while deleting the group.');
    }
}

// Handle Transfer Ownership
async function handleTransferOwnership(groupName, newOwner) {
    if (newOwner === '') {
        alert('New owner username cannot be empty.');
        return;
    }

    // Send transfer ownership request to server
    try {
        const response = await fetch('/api/groups/transfer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // Add Authorization header if needed
            },
            body: JSON.stringify({
                name: groupName,
                newOwner: newOwner
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert(`Ownership of group "${groupName}" has been transferred to ${newOwner}.`);
            hideTransferOwnershipForm();
            loadGroupManagement(); // 重新加载群组列表
        } else {
            alert('Error transferring ownership: ' + (data.message || 'Unknown error.'));
        }
    } catch (error) {
        console.error('Error transferring ownership:', error);
        alert('An error occurred while transferring ownership.');
    }
}

// Handle Search
function handleSearch() {
    const query = document.getElementById('group-search').value;
    loadGroupManagement(query);
}

// Handle Reset Search
function handleResetSearch() {
    document.getElementById('group-search').value = '';
    loadGroupManagement();
}

// Initialize and bind events
document.addEventListener('DOMContentLoaded', () => {
    loadGroupManagement();

    // Bind main action buttons
    document.getElementById('new').addEventListener('click', showCreateGroupForm);
    document.getElementById('join').addEventListener('click', showJoinGroupForm);
    document.getElementById('back-to-chat').addEventListener('click', () => {
        window.location.href = 'main.html';
    });

    // Bind Create Group form
    document.getElementById('create-group').addEventListener('submit', handleCreateGroup);
    document.getElementById('cancel-create').addEventListener('click', hideCreateGroupForm);

    // Bind Join Group form
    document.getElementById('join-group').addEventListener('submit', (event) => {
        event.preventDefault();
        const groupName = document.getElementById('join-group-name').value.trim();
        handleJoinGroup(groupName);
    });
    document.getElementById('cancel-join').addEventListener('click', hideJoinGroupForm);

    // Bind Quit Group form
    document.getElementById('quit-group').addEventListener('submit', (event) => {
        event.preventDefault();
        const groupName = document.getElementById('quit-group-name').value;
        handleQuitGroup(groupName);
    });
    document.getElementById('cancel-quit').addEventListener('click', hideQuitGroupForm);

    // Bind Delete Group form
    document.getElementById('delete-group').addEventListener('submit', (event) => {
        event.preventDefault();
        const groupName = document.getElementById('delete-group-name').value;
        handleDeleteGroup(groupName);
    });
    document.getElementById('cancel-delete').addEventListener('click', hideDeleteGroupForm);

    // Bind Transfer Ownership form
    document.getElementById('transfer-ownership').addEventListener('submit', (event) => {
        event.preventDefault();
        const groupName = document.getElementById('transfer-group-name').value;
        const newOwner = document.getElementById('new-owner-username').value.trim();
        handleTransferOwnership(groupName, newOwner);
    });
    document.getElementById('cancel-transfer').addEventListener('click', hideTransferOwnershipForm);

    // Bind Search functionality
    document.getElementById('search-button').addEventListener('click', handleSearch);
    document.getElementById('reset-search-button').addEventListener('click', handleResetSearch);

    // Optional: Allow pressing Enter to trigger search
    document.getElementById('group-search').addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            handleSearch();
        }
    });
});
