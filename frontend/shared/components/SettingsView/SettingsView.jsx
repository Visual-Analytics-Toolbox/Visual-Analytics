import { useState, useEffect } from 'react';
import styles from './SettingsView.module.css';

export async function getToken() {
  if (await electronAPI.get_value('useDev')) {
    return await electronAPI.get_value("devToken");
  } else {
    return await electronAPI.get_value("apiToken");
  }
};

export async function getUrl() {
  if (await electronAPI.get_value('useDev')) {
    return 'http://127.0.0.1:8000'
  } else {
    return 'https://vat.berlin-united.com';
  }
};

const SettingsView = () => {
  const [token, setToken] = useState('');
  const [log_root, setlogRoot] = useState('');
  const [dev_token, setDevToken] = useState('');
  const [use_dev, setUseDev] = useState(false);

  useEffect(() => {
    async function loadSavedToken() {
      const savedToken = await electronAPI.get_value("apiToken");
      if (savedToken) {
        setToken(savedToken);
      }
    }
    async function loadSavedLogRoot() {
      const savedLogRoot = await electronAPI.get_value("logRoot");
      if (savedLogRoot) {
        setlogRoot(savedLogRoot);
      }
    }
    async function loadSavedDevToken() {
      const savedDevToken = await electronAPI.get_value("devToken");
      if (savedDevToken) {
        setDevToken(savedDevToken);
      }
    }
    async function loadUseDev() {
      const savedUseDev = await electronAPI.get_value("useDev");
      if (savedUseDev) {
        setUseDev(savedUseDev);
      }
    }
    loadSavedToken();
    loadSavedLogRoot();
    loadSavedDevToken();
    loadUseDev();
  }, []);

  const handleSave = async () => {
    await electronAPI.set_value("apiToken", token);
    await electronAPI.set_value("logRoot", log_root);
    await electronAPI.set_value("devToken", dev_token);
    await electronAPI.set_value("useDev", use_dev);
  };

  return (
    <div className="view-content">
      <div className="panel-header">
        <h3>⚙️ Settings</h3>
      </div>
      <div className="panel-content">
        <div className={styles.info_card}>
          <h2>Backend Settings</h2>
          <div className={styles.form_group}>
            <label>Api Token: </label>
            <input
              type="password"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Enter API token"
            />
          </div>
          <div className={styles.form_group}>
            <label>Log Folder: </label>
            <input
              type="text"
              value={log_root}
              onChange={(e) => setlogRoot(e.target.value)}
              placeholder="Enter Root of log folder"
            />
          </div>
        </div>
        <div className={styles.info_card}>
          <h2>Dev Settings</h2>
          <div className={styles.form_group}>
            <label>Dev Token</label>
            <input
              type="password"
              value={dev_token}
              onChange={(e) => setDevToken(e.target.value)}
              placeholder="Enter Dev API Token"
            />
          </div>
          <div className={styles.form_group}>
            <label>Use Dev Settings</label>
            <input
              type="checkbox"
              checked={use_dev}
              onChange={(e) => setUseDev(e.target.checked)}
            />

          </div>
          <div className={styles.form_group}>
            <button onClick={handleSave}>Save</button>
          </div>

        </div>

      </div>
    </div>
  );
};

export default SettingsView;