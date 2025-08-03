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