// Conversation history
let conversationHistory = [];

function sendMessage(message = null){
  let input = message !== null ? message : document.getElementById("userInput").value;
  
  if (!input || !input.trim()) {
    return;
  }

  let chatbox = document.getElementById("chatbox");

  // Add user message to UI
  chatbox.innerHTML += `<div class="chat-message user-message">
    <strong>You:</strong> ${escapeHtml(input)}
  </div>`;

  // Add to history
  conversationHistory.push({
    role: "user",
    message: input,
    timestamp: new Date()
  });

  // Scroll to bottom
  chatbox.scrollTop = chatbox.scrollHeight;

  // Show typing indicator
  chatbox.innerHTML += `<div class="chat-message bot-message typing-indicator">
    <strong>Bot:</strong> <span>Analyzing your symptoms...</span>
  </div>`;
  chatbox.scrollTop = chatbox.scrollHeight;

  // Update to your backend address (Flask server) if needed
  fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: input })
  })
  .then(res => res.json())
  .then(data => {
    // Remove typing indicator
    const typingIndicator = chatbox.querySelector('.typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }

    // Display bot response
    displayBotResponse(chatbox, data);

    // Add to history
    conversationHistory.push({
      role: "bot",
      data: data,
      timestamp: new Date()
    });
  })
  .catch(err => {
    console.error("Error talking to backend:", err);
    
    // Remove typing indicator
    const typingIndicator = chatbox.querySelector('.typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }

    chatbox.innerHTML += `<div class="chat-message bot-message error-message">
      <strong>Bot:</strong> I apologize, the service is temporarily unavailable. Please try again in a moment.
    </div>`;
  });

  if (message === null) {
    document.getElementById("userInput").value = "";
  }
  document.getElementById("userInput").focus();
}

function displayBotResponse(chatbox, data) {
  const reply = data.reply || "I couldn't process your request.";
  
  // Create main response container
  let responseHtml = `<div class="chat-message bot-message">
    <strong>Healthcare Assistant:</strong>
    <div class="bot-response-content">`;

  // Add main reply with formatting
  responseHtml += `<div class="response-text">${formatResponse(reply)}</div>`;

  // Add symptoms found
  if (data.symptoms_found && data.symptoms_found.length > 0) {
    responseHtml += `<div class="symptoms-found">
      <strong>Symptoms identified:</strong>
      <div class="tags">
        ${data.symptoms_found.map(s => `<span class="tag">${escapeHtml(s)}</span>`).join('')}
      </div>
    </div>`;
  }

  // Add severity indicator
  if (data.severity && data.severity !== 'unknown') {
    const severityClass = `severity-${data.severity}`;
    responseHtml += `<div class="severity-indicator ${severityClass}">
      <i class="bi bi-exclamation-circle"></i> Severity: <strong>${data.severity.toUpperCase()}</strong>
    </div>`;
  }

  // Add primary doctors
  if (data.primary_doctors && data.primary_doctors.length > 0) {
    responseHtml += `<div class="doctors-recommendation">
      <strong>Recommended Doctors (${data.primary_department.toUpperCase()}):</strong>
      <div class="doctors-list">`;
    
    data.primary_doctors.forEach(doc => {
      responseHtml += `<div class="doctor-card">
        <div class="doctor-name">👨‍⚕️ ${escapeHtml(doc)}</div>
        <div class="doctor-spec">${escapeHtml(data.primary_department.replace('_', ' ').toUpperCase())}</div>
        <button class="btn btn-sm btn-primary book-btn" onclick="bookAppointment('${escapeHtml(doc)}', '${escapeHtml(data.primary_department)}')">
          Book Appointment
        </button>
      </div>`;
    });
    
    responseHtml += `</div></div>`;
  }

  // Add alternative doctors if available
  if (data.alternative_doctors && data.alternative_doctors.length > 0) {
    responseHtml += `<div class="alternative-doctors">
      <strong>Alternative Specialists:</strong>
      <div class="alternatives-list">`;
    
    data.alternative_doctors.forEach(doc => {
      responseHtml += `<div class="alt-doctor">
        <span class="doctor-name">${escapeHtml(doc)}</span>
        <button class="btn btn-sm btn-outline-primary" onclick="bookAppointment('${escapeHtml(doc)}', 'general')">
          Book
        </button>
      </div>`;
    });
    
    responseHtml += `</div></div>`;
  }

  // Add follow-up questions
  if (data.follow_up_questions && data.follow_up_questions.length > 0) {
    responseHtml += `<div class="follow-up-section">
      <strong>To better understand your condition, could you tell me:</strong>
      <div class="follow-up-questions">`;
    
    data.follow_up_questions.forEach(q => {
      responseHtml += `<button class="follow-up-btn" onclick="sendMessage('${escapeHtml(q)}')">${escapeHtml(q)}</button>`;
    });
    
    responseHtml += `</div></div>`;
  }

  // Add next action
  if (data.next_action) {
    responseHtml += `<div class="next-action">
      <em>${escapeHtml(data.next_action)}</em>
    </div>`;
  }

  responseHtml += `</div></div>`;

  chatbox.innerHTML += responseHtml;
  chatbox.scrollTop = chatbox.scrollHeight;
}

function formatResponse(text) {
  // Replace **text** with <strong>text</strong>
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Replace line breaks with <br>
  text = text.replace(/\n/g, '<br>');
  return text;
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function bookAppointment(doctor, department) {
  // Store the selected doctor and department in localStorage
  localStorage.setItem('selectedDoctor', doctor);
  localStorage.setItem('selectedDepartment', department);
  
  // Redirect to appointment page
  window.location.href = 'appointment.html';
}

function sendSuggestion(suggestion) {
  document.getElementById('userInput').value = suggestion;
  sendMessage();
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
  const userInput = document.getElementById('userInput');
  if (userInput) {
    userInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    });
  }
});