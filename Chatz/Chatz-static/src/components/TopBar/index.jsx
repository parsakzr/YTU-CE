import {
    FaSearch,
    FaHashtag,
    FaRegBell,
    FaMoon,
    FaSun,
} from 'react-icons/fa';
import useDarkMode from '../../hooks/useDarkMode';

  
const ThemeIcon = () => {
  const [darkTheme, setDarkTheme] = useDarkMode();
  const handleMode = () => setDarkTheme(!darkTheme);
  return (
    <span onClick={handleMode}>
      {darkTheme ? (
        <FaSun size='24' className='topbar-icon' />
      ) : (
        <FaMoon size='24' className='topbar-icon' />
      )}
    </span>
  );
};

const TopNavigation = () => {
  return (
    <div className='topbar'>
      <div className='topbar-container'>
        <HashtagIcon />
        <Title />
        <ThemeIcon />
        <Search />
        <BellIcon />
      </div>
    </div>
  );
};


const Search = () => (
  <div className='search'>
    <input className='search-input' type='text' placeholder='Search...' />
    <FaSearch size='18' className='text-secondary my-auto' />
  </div>
);

const BellIcon = () => <FaRegBell size='24' className='topbar-icon' />;
const HashtagIcon = () => <FaHashtag size='20' className='title-hashtag' />;
const Title = () => <h5 className='title-text'>tailwind-css</h5>;

export default TopNavigation;
