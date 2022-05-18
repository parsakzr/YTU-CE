//require our websocket library
var ws = require("ws");
var WebSocketServer = ws.Server;

//creating a websocket server at port 9090
var wss = new WebSocketServer({ port: 9090 });

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
wss.on("connection", function (socket) {
  console.log("User connected");

  //when server gets a message from a connected user
  socket.on("message", function (message) {
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
        if (rooms[data.room]) {
          // if two peers are connected and third one wants to join
          // --> reject the third peer

          if (rooms[data.room].length == 2) {
            sendTo(socket, {
              type: "login",
              success: false,
              action: "reject", // #TODO: @Security potential bypass
            });
          } else {
            // room is not full and peer can join
            // --> join() room
            joinRoom(socket, data.room);
            sendTo(socket, {
              type: "login",
              success: true,
              action: "join",
            });
          }
        } else {
          // room does not exist
          // --> create() room and enter
          createRoom(socket, data.room);
          sendTo(socket, {
            type: "login",
            success: true,
            action: "create",
          });
        }

        break;

      case "offer": // #TODO: merge w/ case "answer"
        //for ex. UserA wants to call UserB
        if (socket.room != undefined && rooms[socket.room] != undefined) {
          console.log("Sending offer to join: ", socket.room);

          //if UserB exists then send him offer details
          var otherConn = getOther(socket, rooms[socket.room]);

          if (otherConn) {
            //setting that UserA connected with UserB
            sendTo(otherConn, {
              type: "offer",
              sdp: data.sdp,
            });
          }
        }

        break;

      case "answer":
        if (socket.room != undefined && rooms[socket.room] != undefined) {
          console.log("Sending answer to: ", socket.room);
          //for ex. UserB answers UserA
          var otherConn = getOther(socket, rooms[socket.room]);

          if (otherConn) {
            // connection established

            sendTo(otherConn, {
              type: "answer",
              sdp: data.sdp,
            });
          }
        }

        break;

      case "candidate": // #TODO: complete iceCandidate
        // to echo ICE candidates to other peer
        if (socket.room != undefined && rooms[socket.room] != undefined) {
          console.log("Sending candidate to:", socket.room);

          var otherConn = getOther(socket, rooms[socket.room]);

          if (otherConn) {
            sendTo(otherConn, {
              type: "candidate",
              candidate: data.candidate,
            });
          }
        }
        break;

      case "leave":
        //leave room
        // data: {"type":"leave"}
        if (rooms[socket.room]) {
          console.log("Disconnecting from", socket.room);

          var otherConn = getOther(socket, rooms[socket.room]);

          if (otherConn) {
            // signal the other user so he can disconnect his peer connection
            sendTo(otherConn, {
              type: "leave",
            });
          }
          // only one person in room
          delete rooms[socket.room]; // remove room
        }

        break;

      default:
        sendTo(socket, {
          type: "error",
          body: "Command not found: " + data.type,
        });

        break;
    }
  });

  //when user exits, for example closes a browser window
  //this may help if we are still in "offer","answer" or "candidate" state
  socket.on("close", function () {
    // the copy of roomName in socket comes handy here
    // since data is not available in on('close')
    if (socket.room) {
      // if user was connected to a room
      console.log("Disconnecting from ", socket.room);

      let room = rooms[socket.room];

      if (room) {
        if (room.length == 2) {
          let other = getOther(socket, room);
          // notify the other user to disconnect from peer
          sendTo(room, {
            type: "leave",
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
  // #TODO research why
  if (socket.readyState == ws.OPEN) {
    socket.send(JSON.stringify(message));
  } else console.log("ERR: Socket not open to send, message:", message);
}

function createRoom(socket, roomName) {
  rooms[roomName] = [];
  rooms[roomName].push(socket);
  // save room info in socket as well, (needed in on('close'))
  socket.indx = 0; // index of the peer in the room, index 0 = creator
  socket.room = roomName;
}

function joinRoom(socket, roomName) {
  socket.room = roomName; // socket holds room name needed .on('close')
  var otherConn = rooms[roomName] != undefined ? rooms[roomName][0] : null;

  if (otherConn != null) {
    rooms[roomName].push(socket);
    socket.indx = 1; // index = 1 joinee.

    console.log("Joined room:", roomName);
  }
}

function getOther(socket, room) {
  var other = socket.indx == 0 ? 1 : 0;
  return room[other];
}
