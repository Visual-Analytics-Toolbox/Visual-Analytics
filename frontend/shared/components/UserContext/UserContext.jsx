import { createContext, useState, useEffect, useContext } from "react";
import { getToken, getUrl } from "@shared/components/SettingsView/SettingsView";

const UserContext = createContext({
  isAdmin: false,
  loading: true,
  user: '',
  refreshAdminStatus: () => {}
});

export const UserProvider = ({ children }) => {
  const [user,setUser] = useState(false);
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
        throw new Error(`HTTP error! status: ${response.status}`);
      } 
      const data = await response.json();
      setIsAdmin(data.is_admin);
      setUser(data.username);
      setLoading(false);
  };

  // Function to refresh admin status
  const refreshUser = () => {
    checkUser();
  };

  // Check admin status on initial load
  useEffect(() => {
    checkUser();
  }, []);

  // Provide the context value
  const value = {
    isAdmin,
    user,
    loading,
    refreshUser: refreshUser
  };
  // ??? why ?
  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

// why do we do this hook ? 
export const useUser = () => {
  return useContext(UserContext);
};

export default UserContext;