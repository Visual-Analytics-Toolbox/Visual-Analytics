import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { getToken, getUrl } from '@shared/components/SettingsView/SettingsView';
import styles from './AdminView.module.css';


const AdminView = ({ }) => {
    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>Admin View</h3>
            </div>
            <div className="panel-content">
                <div className={styles.info_card}>
                    <h2>Update Teams</h2>
                </div>
                <div className={styles.info_card}>
                    <h2>Other Admin Actions</h2>
                </div>
            </div>

        </div>
    );
};

export default AdminView;