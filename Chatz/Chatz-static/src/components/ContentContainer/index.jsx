import TopNavigation from "../TopBar";
import { BsPlusCircleFill } from "react-icons/bs";
import Avatar from "boring-avatars";
import Moment from "react-moment";

const ContentContainer = ({messages, userIDs}) => {

  return (
    <div className="content-container">
      <TopNavigation />
      
      <div className="content-section scrollable">
        {/* {messages.map(message => (
          <Message
          name={userIDs[message.userID]}
          timestamp={<Moment format="DD.MM.YYYY hh:mm" unix>{message.time}</Moment>}
          text={message.content}
        />
        ))} */}
        <Message
          name="Ada"
          timestamp="one week ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur
            adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem
            ipsum dolor sit amet consectetur adipisicing elit.`}
        />
        <Message
          name="Leon"
          timestamp="one week ago"
          text={`Lorem ipsum dolor. `}
        />
        <Message name="Jill" timestamp="5 days ago" text={`Lorem.`} />
        <Message
          name="Ellie"
          timestamp="4 days ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. `}
        />
        <Message
          name="Chris"
          timestamp="4 days ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur
            adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem
            ipsum dolor sit amet consectetur adipisicing elit.
            
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem
            ipsum dolor sit amet consectetur adipisicing elit.`}
        />
        <Message
          name="Claire"
          timestamp="2 days ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur
            adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. `}
        />
        <Message
          name="Albert"
          timestamp="22 hours ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. ☺️ `}
        />
        <Message
          name="Rebecca"
          timestamp="3 hours ago"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit
            amet consectetur adipisicing elit.`}
        />
        <Message
          name="Claire"
          timestamp="Just now"
          text={`Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur
            adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem
            ipsum dolor sit amet consectetur adipisicing elit.`}
        />
      </div>
      <BottomBar />
    </div>
  );
};

const BottomBar = () => (
  <div className="bottom-bar">
    <PlusIcon />
    <input
      type="text"
      placeholder="Enter message..."
      className="bottom-bar-input"
    />
  </div>
);

const Message = ({ name, timestamp, text }) => (
    <div className={"message"}>
      <div className="avatar-wrapper">
        <Avatar className="avatar" size={40} name={name} variant="beam" />
      </div>

      <div className="message-content">
        <p className="message-owner">
          {name}
          <small className="timestamp">{timestamp}</small>
        </p>
        <p className="message-text">{text}</p>
      </div>
    </div>
);

const PlusIcon = () => (
  <BsPlusCircleFill
    size="22"
    className="text-green-500 dark:shadow-lg mx-2 dark:text-primary"
  />
);

export default ContentContainer;
