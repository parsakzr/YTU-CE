/* SideBar.js */
import {
  FaUserCircle,
  FaFire,
  FaRegHeart,
  FaRegMoon,
  FaRegGem,
  FaRadiation,
} from "react-icons/fa";
import { FiSettings, FiHome } from "react-icons/fi";

const SideBar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-top-fixed">
        <SideBarIcon icon={<FiHome size="28" />} />
        <Divider />
      </div>

      <div className="sidebar-mid scrollable">
        <SideBarIcon icon={<FaFire size="28" />} />
        <SideBarIcon icon={<FaRegHeart size="28" />} />
        <SideBarIcon icon={<FaRegMoon size="28" />} />
        <SideBarIcon icon={<FaRegGem size="28" />} />
        <SideBarIcon icon={<FaRadiation size="28" />} />

        <SideBarIcon icon={<FaFire size="28" />} />
        <SideBarIcon icon={<FaRegHeart size="28" />} />
        <SideBarIcon icon={<FaRegMoon size="28" />} />
        <SideBarIcon icon={<FaRegGem size="28" />} />
        <SideBarIcon icon={<FaRadiation size="28" />} />

        <SideBarIcon icon={<FaFire size="28" />} />
        <SideBarIcon icon={<FaRegHeart size="28" />} />
        <SideBarIcon icon={<FaRegMoon size="28" />} />
        <SideBarIcon icon={<FaRegGem size="28" />} />
        <SideBarIcon icon={<FaRadiation size="28" />} />

        <SideBarIcon icon={<FaFire size="28" />} />
        <SideBarIcon icon={<FaRegHeart size="28" />} />
        <SideBarIcon icon={<FaRegMoon size="28" />} />
        <SideBarIcon icon={<FaRegGem size="28" />} />
        <SideBarIcon icon={<FaRadiation size="28" />} />
      </div>
      <div className="sidebar-bottom-fixed">
        <Divider />
        <ProfileButton />
        <SideBarIcon icon={<FiSettings size="28" />} />
      </div>
    </div>
  );
};

const SideBarIcon = ({ icon, text = "tooltip ✨" }) => (
  <div className="sidebar-icon group">
    {icon}
    <span className="sidebar-tooltip group-hover:scale-100">{text}</span>
  </div>
);



const ProfileButton = () => {
  //const username = `parsa`;
  //const password = `123456`;
  //const [token, loading, error] = useLoginUser(username, password);

  // const handleMode = () => console.log(token);
  // return <a href="/login/"><SideBarIcon icon={<FaUserCircle size="28" />} text={token} /></a>;
  return <div><SideBarIcon icon={<FaUserCircle size="28" />} text={"Profile"} /></div>;
};

const Divider = () => <hr className="sidebar-hr" />;

export default SideBar;
