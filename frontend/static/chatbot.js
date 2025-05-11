document.getElementById('send').addEventListener('click', function(event) {
    event.preventDefault(); 

    const question = document.getElementById('question').value;

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    // Display the user message in the chatbox
    const chatbox = document.getElementById('chatbox');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = question;
    chatbox.appendChild(userMessageDiv);

    document.getElementById('question').value = '';

    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('message', 'loading');
    loadingMessage.textContent = 'Bot is typing...';
    chatbox.appendChild(loadingMessage);

    chatbox.scrollTop = chatbox.scrollHeight;

    const jsonData = JSON.stringify({ question: question });

    fetch('/query/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
        },
        body: jsonData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch response');
        }
        return response.json();
    })
    .then(data => {
        chatbox.removeChild(loadingMessage);

        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message', 'bot-message');
        botMessageDiv.textContent = data.response || "I cannot answer this question.";  // Default response if no answer
        chatbox.appendChild(botMessageDiv);

        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        chatbox.removeChild(loadingMessage);

        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.classList.add('message', 'bot-message');
        errorMessageDiv.textContent = 'Error: ' + error.message;
        chatbox.appendChild(errorMessageDiv);

        chatbox.scrollTop = chatbox.scrollHeight;
    });
});

document.getElementById('question').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('send').click();
    }
});

window.addEventListener('DOMContentLoaded', function () {
    const chatbox = document.getElementById('chatbox');
    const welcomeMessageDiv = document.createElement('div');
    welcomeMessageDiv.classList.add('message', 'bot-message');
    welcomeMessageDiv.textContent = 'Hi, how can I help you?';
    chatbox.appendChild(welcomeMessageDiv);
});
