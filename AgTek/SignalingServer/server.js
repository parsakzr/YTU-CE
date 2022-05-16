//require our websocket library 
var WebSocketServer = require('ws').Server;
 
//creating a websocket server at port 9090 
var wss = new WebSocketServer({port: 9090}); 

//all rooms currently available in the lobby
// #TODO: room architecture:

// var room = getRoom()
// if(socket === room[0]){
      // other = room[1];
      // send(other, {
      //    ...
      // })
//    

// rooms = {
//    "room1": [
//       'wdjd-ewrewr-erwr': // WebSocket Connections
//       'rewr-rewrer-erew':
//    ],
//    "room2": [
//          p1,
//          p2
//    ],
//  }

// offer():
// P2 sends P1 json;
// p2.otherPeer = p1


var rooms = {};

  
//when a user connects to our sever 
wss.on('connection', function(socket) {

   console.log("User connected");
	
   //when server gets a message from a connected user
   socket.on('message', function(message) { 
	
      var data; 
      // only JSON messages 
      try {
         data = JSON.parse(message); 
      } catch (e) { 
         console.log("Invalid JSON"); 
         data = {}; 
      } 
		
      //switching type of the user message 
      switch (data.type) { 
         //when a user tries to login
         case "login": 
            console.log("logging in room:", data.room); 
				
            //if the given room exists
            if(rooms[data.room]) {
               // if two peers are connected and third one wants to join
               // --> reject the third peer
               console.log('room length:',rooms[data.room].length);
               if(rooms[data.room].length == 2) {
                  sendTo(socket, { 
                     type: "login",
                     success: false,
                     action: "reject", // #TODO: @Security potential bypass
                  });
                  break;
               }
               // if remote peer is joining
               // --> signal to join() room
               joinRoom(socket, data.room);
               sendTo(socket, { 
                  type: "login", 
                  success: true,
                  action: "join",
                  room: data.room,
               }); 
            } else { 
               // --> signal to create() room
               createRoom(socket, data.room);
					
               sendTo(socket, { 
                  type: "login",
                  success: true,
                  action: "create"
               }); 
            } 
				
            break; 
				
         case "offer": 
            //for ex. UserA wants to call UserB 
            console.log("Sending offer to join: ", data.room); 
				
            //if UserB exists then send him offer details 
            var otherConn = rooms[data.room] != undefined ? rooms[data.room][0] : null;
				
            if(otherConn != null) { 
               //setting that UserA connected with UserB 
               sendTo(otherConn, { 
                  type: "offer", 
                  sdp: data.sdp, 
                  // name: socket.name 
               }); 
            }
				
            break;  
				
         case "answer": 
            console.log("Sending answer to: ", data.room); 
            //for ex. UserB answers UserA 
            var otherConn = getOther(socket, rooms[data.room]);
				
            if(otherConn) { 
               // connection established
               
               sendTo(otherConn, {
                  type: "answer", 
                  body: data.body 
               });
            } 
				
            break;  
				
         case "candidate": 
            console.log("Sending candidate to:",data.room); 
            var other = getOther(socket, data.room); 
				
            if(other != null) { 
               sendTo(other, { 
                  type: "candidate", 
                  body: data.body 
               });
            } 
				
            break;  
				
         case "leave": 
            console.log("Disconnecting from", data.room); 
            var otherConn = getOther(socket, data.room);
				
            if(otherConn) { 
                  // signal the other user so he can disconnect his peer connection 
                  sendTo(otherConn, { 
                     type: "leave" 
                  });
               } else { // only one person in room
                  delete rooms[data.room];  // remove room
               }
               
               
            break;  
               
         default: 
            sendTo(socket, { 
               type: "error", 
               body: "Command not found: " + data.type 
            }); 
				
            break; 
      }  
   });  
	
   //when user exits, for example closes a browser window 
   //this may help if we are still in "offer","answer" or "candidate" state 
   socket.on("close", function() { 
	
      if(socket.room) { // if user was connected 
         console.log("Disconnecting from ", socket.room);
         var conn = rooms[socket.room];

         if(conn != null) {
            conn.room = null; 
            
            if(conn.isFull){ // notify the other user to disconnect from peer
               sendTo(conn, { 
                  type: "leave" 
               });
            }  
         }
         // remove room
         delete rooms[socket.room]; 
      }
   });  
	
   // socket.send("Hello world"); 
	
});  


// Utility functions .........................
// alias to send stringified json to socket
function sendTo(socket, message) { 
   socket.send(JSON.stringify(message)); 
}

function createRoom(socket, roomName){
   rooms[roomName] = [];
   rooms[roomName].push(socket);
   socket.indx = 0; // index of the peer in the room, index 0 = creator
   socket.room = roomName;
   
}

function joinRoom(socket, roomName){
   socket.roomName = roomName; // socket holds room name needed .on('close')
   var otherConn = (rooms != undefined) ? rooms[roomName][0] : null;

   if(otherConn != null) {
      rooms[roomName].push(socket);
      socket.indx = 1; // index = 1 joinee.
   }
}


function getOther(socket, room){
   var other = (socket.indx == 0) ? 1 : 0;
   return room[other];
}