import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { getToken, getUrl } from '@shared/components/SettingsView/SettingsView';
import styles from './SettingsView.module.css';

const fetch_teams = async () => {
    const token = await getToken();
    const url = await getUrl();
    const response = await fetch(`${url}/api/teams/`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}


const TeamView = ({ }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const teams = useQuery({
        queryKey: ['results'],
        queryFn: () => fetch_teams(),
        staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
        cacheTime: 5 * 60 * 1000,
    });
    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>Team View</h3>
            </div>
            <div className="panel-content">
                <div className={styles.info_card}>
                    <table>
                        <tr>
                        <th>ID</th>
                        <th>Name</th>
                        </tr>
                    {teams.data.map((team) => (
                                <tr>
                                    <td>{team.team_id}</td>
                                    <td>{team.name}</td>
                                </tr>
                            ))}
                    </table>
                </div>
                
            
                

            </div>
                
        </div>
    );
};

export default TeamView;