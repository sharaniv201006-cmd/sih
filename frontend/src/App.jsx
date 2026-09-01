import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { Animals } from './pages/Animals';
import { AnimalDetail } from './pages/AnimalDetail';
import { AnimalRegistration } from './pages/AnimalRegistration';
import { LiveSensorMonitoring } from './pages/LiveSensorMonitoring';
import { Alerts } from './pages/Alerts';
import { ModelPerformance } from './pages/ModelPerformance';
import { Login } from './pages/Login';
import { fetchHealth, fetchDashboard } from './services/api';

export function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('bovine_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [selectedAnimalId, setSelectedAnimalId] = useState(null);
  const [simulatedCowData, setSimulatedCowData] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [isBackendOnline, setIsBackendOnline] = useState(false);

  const initData = async () => {
    try {
      const health = await fetchHealth();
      if (health.status === 'online') {
        setIsBackendOnline(true);
      }
      const dash = await fetchDashboard();
      setDashboardData(dash);
    } catch (err) {
      console.error('API connection warning:', err);
      setIsBackendOnline(false);
    }
  };

  useEffect(() => {
    if (user) {
      initData();
      const interval = setInterval(initData, 30000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    localStorage.setItem('bovine_user', JSON.stringify(userData));
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('bovine_user');
  };

  const handleSelectAnimal = (animalId) => {
    setSelectedAnimalId(animalId);
    setActiveTab('animal-detail');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSimulateWithCow = (cow) => {
    setSimulatedCowData(cow);
    setActiveTab('live-monitoring');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleRegistrationSuccess = (newCow) => {
    initData();
  };

  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-100/70 flex text-slate-900 font-sans selection:bg-emerald-500 selection:text-white">
      
      {/* Left Vertical Collapsible Sidebar */}
      <Sidebar 
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          if (tab !== 'animal-detail') setSelectedAnimalId(null);
        }}
        isCollapsed={isSidebarCollapsed}
        setIsCollapsed={setIsSidebarCollapsed}
        user={user}
        onLogout={handleLogout}
        isBackendOnline={isBackendOnline}
      />

      {/* Main Content Area on Right */}
      <div className="flex-1 flex flex-col min-w-0 overflow-x-hidden">
        
        {/* Top Header */}
        <Header 
          activeTab={activeTab} 
          setActiveTab={setActiveTab}
        />

        {/* Focused Dedicated Page View */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto space-y-6 animate-fadeIn">
          
          {activeTab === 'dashboard' && (
            <Dashboard 
              data={dashboardData} 
              onSelectAnimal={handleSelectAnimal}
              onNavigate={(tab) => setActiveTab(tab)}
            />
          )}

          {activeTab === 'register-animal' && (
            <AnimalRegistration 
              onRegistrationSuccess={handleRegistrationSuccess}
              onInspectAnimal={handleSelectAnimal}
            />
          )}

          {activeTab === 'animals' && (
            <Animals onSelectAnimal={handleSelectAnimal} />
          )}

          {activeTab === 'animal-detail' && selectedAnimalId && (
            <AnimalDetail 
              animalId={selectedAnimalId} 
              onBack={() => setActiveTab('animals')}
              onSimulateWithCow={handleSimulateWithCow}
            />
          )}

          {activeTab === 'live-monitoring' && (
            <LiveSensorMonitoring initialCowData={simulatedCowData} />
          )}

          {activeTab === 'alerts' && (
            <Alerts onSelectAnimal={handleSelectAnimal} />
          )}

          {activeTab === 'model-performance' && (
            <ModelPerformance />
          )}

        </main>

        {/* Footer */}
        <footer className="border-t border-slate-200 bg-white py-4 px-6 text-xs text-slate-500 mt-12 flex flex-col sm:flex-row items-center justify-between gap-2 shadow-xs">
          <span>BovineGuard AI &bull; Bovine Mastitis Early Forecasting Platform</span>
          <span>Logged in as <strong className="text-slate-800 font-bold">{user.name}</strong> ({user.role})</span>
        </footer>

      </div>

    </div>
  );
}

export default App;
