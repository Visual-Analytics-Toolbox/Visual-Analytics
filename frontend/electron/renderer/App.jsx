
import { HashRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MainLayout from '@shared/components/MainLayout/MainLayout';

const queryClient = new QueryClient();

function App() {
  // TODO maybe we can get the versions here same as in rust
  const appVersion = "0.0.1"

  return (
    <QueryClientProvider client={queryClient}>
      <HashRouter>
        <MainLayout appVersion={appVersion} />
      </HashRouter>
    </QueryClientProvider>
  );
}

export default App;