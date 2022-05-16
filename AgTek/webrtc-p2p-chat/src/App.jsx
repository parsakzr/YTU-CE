import { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const ws = new WebSocket("ws://localhost:9090");
const config = {
  iceServers: [
    {
      urls: "stun:stun.l.google.com:19302"
    }
  ]
};
var newRoom;
const peerConnection = new RTCPeerConnection(config, {optional: [{RtpDataChannels: true}]});
ws.onopen = () => {
  console.log("Connected to signalling server");
};
ws.onmessage = async (event) => {
  console.log(event.data);
  const data = JSON.parse(event.data);
  switch (data.type) {
    case "offer":
      console.log("Got offer. Sending answer to peer.");
      await peerConnection.setRemoteDescription(new RTCSessionDescription({type:data.type, sdp: data.sdp}))
      let answer = await peerConnection.createAnswer()
      await peerConnection.setLocalDescription(answer)
      console.log(newRoom);
      await ws.send(JSON.stringify({type:"answer", sdp:answer.sdp, room:"aaa"}));
      break;
    case "answer":
      console.log("Got answer");
      peerConnection.setRemoteDescription(new RTCSessionDescription(data));
      break;
    case "candidate":
      console.log("Got ICE candidate");
      peerConnection.addIceCandidate(new RTCIceCandidate(data));
      break;
    case "login":
      let dataChannel = peerConnection.createDataChannel("channel1", {reliable:true}); 
      console.log("Got login");
      if (data.action == "join") {
        let offer = peerConnection.createOffer().then((offer) => {
          peerConnection.setLocalDescription(offer).then(() => {
            newRoom = data.room;
            console.log("nre", newRoom);
            ws.send(
              JSON.stringify({ type: "offer", room: data.room, sdp: offer.sdp })
            );
          });
        });
      }
    default:
      console.error("Unrecognized message type:", data.type);
  }
};

function App() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState("");
  const handleForm = (e) => {
    e.preventDefault();
    ws.send(JSON.stringify({ type: "login", room: name }));
  };

  return (
    <div className="App">
      <h1 class="text-3xl font-bold underline">Hello world!</h1>
      <form onSubmit={handleForm}>
        <input
          type="text"
          placeholder="Enter room name"
          onChange={(e) => setName(e.target.value)}
          class="border border-gray-400 rounded-lg py-2 px-4 block w-full"
        />
        <button
          type="submit"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
        >
          Join
        </button>
      </form>
    </div>
  );
}

export default App;
