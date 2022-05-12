
//our username 
var username; 
var connectedUser;
  
//connecting to our signaling server 
var conn = new WebSocket('ws://localhost:9090');
  
conn.onopen = function () { 
   console.log("Connected to the signaling server");
}; 
 
//when we got a message from a signaling server 
conn.onmessage = function (msg) { 
   console.log("Got message", msg.data);
	
   var data = JSON.parse(msg.data);
	
   switch(data.type) { 
      case "login": 
         handleLogin(data.success); 
         break; 
      //when somebody wants to call us 
      case "offer": 
         handleOffer(data.offer, data.name); 
         break; 
      case "answer": 
         handleAnswer(data.answer); 
         break; 
      //when a remote peer sends an ice candidate to us 
      case "candidate":
         handleCandidate(data.candidate); 
         break; 
      case "leave": 
         handleLeave(); 
         break; 
      default: 
         break; 
   } 
};
  
conn.onerror = function (err) { 
   console.log("Got error", err); 
};
  
//alias for sending JSON encoded messages 
function send(message) { 
   //attach the other peer username to our messages 
   if (connectedUser) { 
      message.name = connectedUser; 
   } 
	
   conn.send(JSON.stringify(message)); 
};

// DOM selectors --------------------------------------------------------------
var lobbyPage = document.getElementById("lobby-page");
var chatPage = document.getElementById("chat-page");
chatPage.style.display = "none";
// ---- login page
var loginBtn = document.getElementById("login-button");
var userInpt = document.getElementById("username-input");

// ---- index page
var chatBox = document.getElementById("chat-box");

loginBtn.addEventListener("click", function () {
    
    username = userInpt.value;
    if (username) {
        chatBox.append("You joined as ", username);
        send({
         type: "login",
         name: username
      });
   }

});

// handlers -------------------------------------------------------------------
function handleLogin(success) {
   if(success === false) {
      alert("Login failed, please try a different name.");
      return;
   }
   // switch to the chat page
   lobbyPage.style.display = "none"; 
   chatPage.style.display = "block";

   // ----
   // RTC Peer Connection
   // ----
}

