import logo from '@shared/assets/logo_mini.svg';
import styles from './SidebarLogo.module.css';
import { useUser } from "../UserContext/UserContext";

const SidebarLogo = ({ appVersion }) => {
  const { isAdmin, loading, user } = useUser();
  return (
    <div className={styles.sidebar_header}>
      <img src={logo} className={styles.logo} alt="logo" />
      <p className={styles.version}>v{appVersion}</p>
      <p className={styles.username}>Logged in as {user}</p>
    </div>
  );
};

export default SidebarLogo;