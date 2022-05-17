import { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const ws = new WebSocket("ws://localhost:9090");

var room; // current room name, accessed via window.room

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

ws.onopen = () => {
  console.log("Connected to signalling server");
};

ws.onmessage = async (event) => {
  console.log(event.data); // #LOG
  const data = JSON.parse(event.data);

  switch (data.type) {
    // handle actions for each data type
    case "login":
      let dataChannel = peerConnection.createDataChannel("message", {
        reliable: true,
      });
      console.log("Got login");
      if (data.action == "join") {
        let offer = peerConnection.createOffer().then((offer) => {
          peerConnection.setLocalDescription(offer).then(() => {
            console.log("room is:", window.room); // #LOG
            ws.send(
              JSON.stringify({ type: "offer", room: data.room, sdp: offer.sdp })
            );
          });
        });
      }
      break;

    case "offer":
      console.log("Got offer. Sending answer to peer.");
      await peerConnection.setRemoteDescription(
        new RTCSessionDescription({
          type: data.type,
          sdp: data.sdp,
          room: window.room,
        })
      );
      let answer = await peerConnection.createAnswer();
      await peerConnection.setLocalDescription(answer);

      await ws.send(
        JSON.stringify({ type: "answer", sdp: answer.sdp, room: window.room })
      );
      break;

    case "answer":
      console.log("Got answer");
      peerConnection.setRemoteDescription(new RTCSessionDescription(data));
      break;

    case "candidate":
      console.log("Got ICE candidate");
      peerConnection.addIceCandidate(new RTCIceCandidate(data));
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
    setMessage("");
    peerConnection.send();
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
          <div className="flex flex-col">
            <div className="h-32 w-64 bg-slate-400">Hello world!</div>
            <form onSubmit={handleSend}>
              <input
                type="text"
                id="message"
                placeholder="Enter message"
                onChange={(e) => setMessage(e.target.value)}
                className="border border-gray-400 rounded-lg py-2 px-4 block w-full"
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
