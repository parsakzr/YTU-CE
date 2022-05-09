let localStream;
let remoteStream;

const servers = {
    iceServers: [{
        urls: [
            'stun:stun.l.google.com:19302',
            'stun:stun1.l.google.com:19302',
            'stun:stun2.l.google.com:19302'
        ]
    }]
}

let peerConnection;

const init = async () => {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    document.getElementById('localVideo').srcObject = localStream;

    createOffer();
}

const createOffer = async () => {
    // peerConnection = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
    peerConnection = new RTCPeerConnection(servers);

    remoteStream = new MediaStream();
    document.getElementById('remoteVideo').srcObject = remoteStream;  

    
    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    })

    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
            remoteStream.addTrack(track);
        });
    }


    peerConnection.onicecandidate = async (event) => {
        if (event.candidate) {
            console.log('icecandidate', event.candidate);
        }
    }

    let offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    console.log('offer:', offer);
}

 init();