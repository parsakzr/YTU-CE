import { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const ws = new WebSocket("ws://localhost:9090");

const config = {
  iceServers: [
    {
      urls: [
        "stun:stun.l.google.com:19302",
        "stun:stun1.l.google.com:19302",
        "stun:stun2.l.google.com:19302",
      ],
    },
  ],
};

const peerConnection = new RTCPeerConnection(config, {
  optional: [{ RtpDataChannels: true }],
});

var room; // current room name, accessed via window.room
var dataChannel;

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
      window.dataChannel = peerConnection.createDataChannel("messageChannel", {
        reliable: true,
      });
      console.log("Got login");
      if (data.action == "join") {
        let offer = peerConnection.createOffer().then((offer) => {
          peerConnection.setLocalDescription(offer).then(() => {
            ws.send(
              JSON.stringify({ type: "offer", room: data.room, sdp: offer.sdp })
            );
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

      let answer = await peerConnection.createAnswer();

      console.log("ON OFFER: \nanswer: \n", answer);
      console.log("data: \n", data); // #LOG

      await peerConnection.setLocalDescription(answer);

      await ws.send(JSON.stringify({ type: "answer", sdp: answer.sdp }));
      break;

    case "answer":
      console.log("Got answer");
      // peerConnection.setRemoteDescription(
      //   new RTCSessionDescription({ type: "answer", sdp: data.sdp })
      // ); // Serialized, so no need to new RTCSessionDescription()
      peerConnection.setRemoteDescription(data);

      break;

    case "candidate":
      console.log("Got ICE candidate");
      peerConnection.addIceCandidate(new RTCIceCandidate({ data }));
      break;

    default:
      console.error("Unrecognized message type:", data.type);
      break;
  }
};

function App() {
  const [count, setCount] = useState(0);
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
    // peerConnection.send();

    console.log("peerconnection state:", peerConnection.signalingState);
    console.log("datachannel state:", window.dataChannel.readyState);

    // window.dataChannel.send(message);

    // reset message and message-box
    setMessage("");
    document.getElementById("message-box").value = "";
  };

  const handleMessage = (e) => {
    //when we receive a message from the other peer, display it on the screen
    window.dataChannel.onmessage = (event) => {
      chatArea.innerHTML += event.data + "<br />";
    };

    window.dataChannel.onclose = () => {
      console.log("data channel is closed");
    };
  };
  return (
    <div className="App">
      {isLobby == true && (
        <div className="Lobby">
          <h1 className="header font-bold">Lobby</h1>
          <form onSubmit={handleJoin}>
            <input
              type="text"
              placeholder="Enter room name"
              onChange={(e) => setName(e.target.value)}
              className="border border-gray-400 rounded-lg py-2 px-4 block w-full"
            />
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
            >
              Join
            </button>
          </form>
        </div>
      )}
      {isLobby == false && (
        <div className="Chat">
          <h1 className="header font-bold ">Chat</h1>
          <h2 className="h-32 w-64 bg-slate-400">{window.room}</h2>
          <div className="flex flex-col">
            <form onSubmit={handleSend}>
              <input
                type="text"
                id="message-box"
                placeholder="Enter message"
                onChange={(e) => setMessage(e.target.value)}
                className="border border-gray-400 rounded-lg py-2 px-4 block w-1/3"
              />
              <button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
