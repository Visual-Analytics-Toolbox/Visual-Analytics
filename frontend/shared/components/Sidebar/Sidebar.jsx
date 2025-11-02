import { NavLink } from "react-router-dom";
import { useUser } from "../UserContext/UserContext";
import SidebarLogo from '@shared/components/SidebarLogo/SidebarLogo'
import SidebarBottom from '@shared/components/SidebarBottom/SidebarBottom'
import styles from './Sidebar.module.css';

const Sidebar = ({ appVersion }) => {
  const { isAdmin, loading } = useUser();

  const getNavLinkClass = (styles) => {
    return ({ isActive }) =>
      isActive ? `${styles.sidebar_item} ${styles.active}` : styles.sidebar_item;
  };

  return (
    <div className={styles.sidebar}>
      <SidebarLogo appVersion={appVersion} />

      <div className={styles.sidebar_content}>
        <nav className={styles.sidebar_nav}>
          <NavLink to="/" className={getNavLinkClass(styles)}>Home</NavLink >
          <NavLink to="/events" className={getNavLinkClass(styles)}>Events</NavLink >
          <NavLink to="/debug" className={getNavLinkClass(styles)}>Debugger</NavLink >
          <NavLink to="/test" className={getNavLinkClass(styles)}>Test</NavLink >
          <NavLink to="/validation" className={getNavLinkClass(styles)}>Validation</NavLink>
          <NavLink to="/teams" className={getNavLinkClass(styles)}>Teams</NavLink>
          {!loading && isAdmin && <NavLink to="/admin" className={getNavLinkClass(styles)}>Admin</NavLink>}
        </nav>
        <SidebarBottom />
      </div>
    </div>
  );
};

export default Sidebar;