function sendMessage(){

let input = document.getElementById("userInput").value;

let chatbox = document.getElementById("chatbox");

chatbox.innerHTML += "<p><b>You:</b> " + input + "</p>";

// Update to your backend address (Flask server) if needed
fetch("http://localhost:5000/chat", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({message:input})
})

.then(res=>res.json())
.then(data=>{

chatbox.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";

})
.catch(err=>{
    console.error("Error talking to backend:", err);
    chatbox.innerHTML += "<p><b>Bot:</b> Sorry, service temporarily unavailable.</p>";
})

document.getElementById("userInput").value="";
}