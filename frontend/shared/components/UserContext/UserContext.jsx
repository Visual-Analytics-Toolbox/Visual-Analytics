import { createContext, useState, useEffect, useContext } from "react";
import { getToken, getUrl } from "@shared/components/SettingsView/SettingsView";

const UserContext = createContext({
  isAdmin: false,
  loading: true,
  user: '',
  refreshUser: () => { }
});

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkUser = async () => {
    setLoading(true);
    const token = await getToken();
    const url = await getUrl();

    const response = await fetch(`${url}/user`, {
      headers: {
        'Authorization': `Token ${token}`,
      }
    });

    if (!response.ok) {
      setLoading(false);
      console.log(`HTTP error while fetching user! status: ${response.status}`);
    }
    const data = await response.json();
    setIsAdmin(data.is_admin);
    setUser(data.username);
    setLoading(false);
  };

  const refreshUser = () => {
    checkUser();
  };

  useEffect(() => {
    checkUser();
  }, []);

  const value = {
    isAdmin,
    user,
    loading,
    refreshUser: refreshUser
  };
  // passing down values to all children
  return (
    <UserContext value={value}>
      {children}
    </UserContext>
  );
};

// easier way to access context data in components
export const useUser = () => {
  return useContext(UserContext);
};

export default UserContext;