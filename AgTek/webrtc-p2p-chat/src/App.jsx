import { useState } from "react";
import "./App.css";

const ws = new WebSocket("ws://localhost:9090");

const config = {
  iceServers: [
    {
      urls: ["stun:stun2.l.google.com:19302"],
    },
  ],
};

const peerConnection = new RTCPeerConnection(config, {
  optional: [{ RtpDataChannels: true }],
});

ws.onopen = () => {
  console.log("Connected to signalling server");
};

ws.onmessage = async (event) => {
  console.log(event.data); // #LOG
  const data = JSON.parse(event.data);

  console.log(data); // #LOG

  switch (data.type) {
    // handle actions for each data type
    case "login":
      peerConnection.onicecandidate = function (event) {
        if (event.candidate) {
          ws.send(
            JSON.stringify({
              type: "candidate",
              candidate: event.candidate,
              room: window.room,
            })
          );
        }
      };

      console.log("Got login");
      if (data.action == "join") {
        window.dataChannel = peerConnection.createDataChannel(
          "messageChannel",
          {
            reliable: true,
          }
        );
        window.dataChannel.onmessage = function (event) {
          console.log(event.data, "message received");
          document.getElementById(
            "message-room"
          ).innerHTML += `<h3 class="text-left border-b-2 border-slate-500">${event.data}</h3>`;
        };
        window.dataChannel.onerror = function (error) {
          console.log("Ooops...error:", error);
        };

        peerConnection.createOffer().then((offer) => {
          peerConnection.setLocalDescription(offer).then(() => {
            ws.send(JSON.stringify({ type: "offer", sdp: offer.sdp }));
          });
        });
      }
      break;
    case "offer":
      console.log("Got offer. Sending answer to peer.");
      await peerConnection.setRemoteDescription({
        type: "offer",
        sdp: data.sdp,
      });
      peerConnection.ondatachannel = function (event) {
        window.dataChannel = event.channel;
        window.dataChannel.onopen = function () {
          console.log("data channel open");
          document.getElementById(
            "message-room"
          ).innerHTML += `<h3 class="text-center border-b-2 border-green-500">Peer Connected</h3>`;
        };
        window.dataChannel.onmessage = function (event) {
          // add to chat
          console.log(event.data, "message received");
          document.getElementById(
            "message-room"
          ).innerHTML += `<h3 class="text-left border-b-2 border-slate-500">${event.data}</h3>`;
        };
      };
      let answer = await peerConnection.createAnswer();
      await peerConnection.setLocalDescription(answer);
      ws.send(JSON.stringify({ type: "answer", sdp: answer.sdp }));
      break;
    case "answer":
      console.log("Got answer");
      peerConnection.setRemoteDescription(data);
      break;
    case "candidate":
      console.log("Got ICE candidate");
      peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
      break;
    case "leave":
      console.log("Remote left.");
      document.getElementById(
        "message-room"
      ).innerHTML += `<h3 class="text-center border-b-2 border-slate-500 text-orange-300">Your peer left!</h3>`;
      document.getElementById("message-box").style.display = "none";
      document.getElementById("send-button").style.display = "none";
    default:
      console.error("Unrecognized message type:", data.type);
      break;
  }
};

function App() {
  const [name, setName] = useState("");
  const [isLobby, setIsLobby] = useState(true);
  const [message, setMessage] = useState("");

  const handleJoin = (e) => {
    e.preventDefault();
    window.room = name; // #GLOBAL VAR
    ws.send(JSON.stringify({ type: "login", room: name }));

    setIsLobby(false);
  };

  const handleSend = (e) => {
    e.preventDefault();

    console.log("Sending message", message);

    window.dataChannel.send(message);
    document.getElementById(
      "message-room"
    ).innerHTML += `<h3 class="text-right border-b-2 border-slate-500">${message}</h3>`;

    // reset message and message-box
    setMessage("");
    document.getElementById("message-box").value = "";
  };
  return (
    <div className="App">
      {isLobby == true && (
        <div className="Lobby">
          <h1 className="header font-bold text-3xl mb-4">Lobby</h1>
          <form onSubmit={handleJoin}>
            <input
              type="text"
              placeholder="Enter room name"
              onChange={(e) => setName(e.target.value)}
              className="border border-gray-400 rounded-lg py-2 px-4 block w-64 text-center mx-auto"
            />
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-2 rounded-lg"
            >
              Join
            </button>
          </form>
        </div>
      )}
      {isLobby == false && (
        <div className="Chat">
          <h1 className="header font-bold ">Chat</h1>
          <h2
            className="rounded-t-md h-fit w-96 bg-slate-600 text-slate-50 font-bold mx-auto"
            id="message-title"
          >
            Room Name: {window.room}
          </h2>
          <div
            className="rounded-b-md h-72 w-96 bg-slate-400 text-black font-bold overflow-y-auto overflow-x-clip py-1 px-2 mx-auto"
            id="message-room"
          >
            {window.chat}
          </div>
          <div className="flex flex-col justify-center mx-auto my-2">
            <form onSubmit={handleSend} className="flex gap-2 justify-center">
              <input
                type="text"
                id="message-box"
                placeholder="Enter message"
                onChange={(e) => setMessage(e.target.value)}
                className="border w-72 border-gray-400 rounded-lg py-2 px-4 block"
              />
              <button
                id="send-button"
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 w-16 rounded-lg"
              >
                Send
              </button>
            </form>
            {/* leave button */}
            <button
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 w-32 rounded-lg mx-auto mt-2"
              onClick={() => {
                ws.send(JSON.stringify({ type: "leave", room: window.room }));
                location.reload();
              }}
            >
              Leave Room
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
