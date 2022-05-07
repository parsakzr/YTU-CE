// import logo from './logo.svg';
import "./App.css";
import React from "react";
import axios from "axios";
import Moment from "react-moment";

import SideBar from "./components/SideBar";
import ChannelBar from "./components/ChannelBar";
import ContentContainer from "./components/ContentContainer";

// import useLoginUser from "./hooks/user/";
// import getAll from "./hooks/user/";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      token: "",
      messagebox: "",
      messages: [],
      userids: {},
      channelIds: [],
      currentChannelId: "",
      displayChannel: "",
    };
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  changeChannel(channelId) {
    this.setState({
      displayChannel: this.state.channelIds.filter(
        (channel) => channel.channelId === channelId
      )[0].channelName,
    });
    this.setState({
      currentChannelId: channelId,
      messages: [],
    });

    this.getAllMessages();
  }

  signup = async () => {
    var url = "http://localhost:23451/user/create";
    var msgData = {
      username: this.state.username,
      password: this.state.password,
    };
    console.log(msgData);
    axios.post(url, msgData).then((response) => {
      console.log(response);
      this.setState({
        token: response.data.token,
      });
      this.getChannels();
      this.getAllMembers();
      this.changeChannel(this.state.channelIds[0].channelId);
    });
    setInterval(this.getAllMessages, 1000);
    setInterval(this.getAllMembers, 5000);
  };

  getAllMembers = async () => {
    var url = "http://localhost:23451/user/getAll";
    await fetch(url, {
      method: "GET",
    }).then((response) => {
      response.json().then((data) => {
        //console.log(data);
        this.setState({
          userids: data,
        });
      });
    });
  };

  getChannels = async () => {
    var url = "http://localhost:23451/channel/guildChannels?guildId=4";
    console.log(this.state.token);
    await fetch(url, {
      method: "GET",
      headers: {
        Token: this.state.token,
      },
    }).then((response) => {
      response.json().then((data) => {
        console.log(data);
        this.setState({
          channelIds: data,
          currentChannelId: data[0].channelId,
        });
        console.log(this.state.currentChannelId);
      });
    });
  };

  gettoken = async () => {
    var url =
      "http://localhost:23451/user/login?username=" +
      this.state.username +
      "&password=" +
      this.state.password;
    fetch(url, {
      method: "GET",
    }).then((response) => {
      response.json().then((data) => {
        //console.log(data.token);
        this.setState({
          token: data.token,
        });
        console.log(this.state.token);
        this.getChannels();
        this.getAllMembers();
      });
    });

    setInterval(this.getAllMessages, 1000);
    setInterval(this.getAllMembers, 5000);
  };

  getAllMessages = async () => {
    var url =
      "http://localhost:23451/message/getMessages?channelId=" +
      this.state.currentChannelId;

    await fetch(url, {
      method: "GET",
      headers: {
        Token: this.state.token,
      },
    }).then((response) => {
      response.json().then((data) => {
        //console.log(data);
        this.setState({
          messages: data,
        });
        //console.log("state'ten", this.state.messages);
      });
    });
  };

  handleInputChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value,
    });
  }

  sendMessage = async () => {
    if (this.state.messagebox === "") {
      return;
    }
    var msgData = {
      message: this.state.messagebox,
      channelId: this.state.currentChannelId,
    };
    console.log(msgData);
    axios.post("http://localhost:23451/message/send", msgData, {
      headers: {
        Token: this.state.token,
      },
    });
    this.setState({
      messagebox: "",
    });

    document.getElementsByClassName("messagebox")[0].value = "";
    await this.getAllMessages();
  };

  render() {
    return (
      <div className="App">
        {this.state.token === "" || this.state.token === -1 ? (
          <div>
            <div className="sign">
              <input
                name="username"
                type="text"
                onChange={this.handleInputChange}
              />
              <input
                name="password"
                type="password"
                onChange={this.handleInputChange}
                placeholder={this.state.text}
              />
              <button
                onClick={
                  () => this.gettoken(this.state.username, this.state.password)
                }
              >
                Giriş
              </button>
              <button
                onClick={
                  () => this.signup()
                }
              >
                Kaydol
              </button>
            </div>
          </div>
        ) : (
          <div>
            {/* The Main UI */}
            {/* <div className="flex">
              <SideBar />
              <ChannelBar />
              <ContentContainer messages={this.state.messages} userIDs={this.state.userids}/>
            </div> */}



            <input
              placeholder="Enter Message"
              autoComplete="off"
              type="text"
              name="messagebox"
              className="messagebox"
              onChange={this.handleInputChange}
            />
            <button onClick={this.sendMessage}>Send message</button>

            <div className="channels">
              {this.state.channelIds.map((channel) => (
                <button onClick={() => this.changeChannel(channel.channelId)}>
                  {channel.channelName}
                </button>
              ))}
            </div>

            <h1>MESAJLAR</h1>
            {this.state.messages.length === 0 ? (
              <div>Loading...</div>
            ) : (
              <div></div>
            )}
            {this.state.messages.map((message) => (
              <p key={message.id}>
                <span className="messagetime">
                  <Moment format="DD.MM.YYYY hh:mm" unix>
                    {message.time}
                  </Moment>
                </span>
                {this.state.userids[message.senderId]}: {message.content}
              </p>
            ))}
          </div>
        )}
      </div>
    );
  }
}

export default App;
