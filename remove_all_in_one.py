# -*- coding: utf-8 -*-
# 1. Update Sidebar.jsx (Remove All-In-One view)
with open("frontend/src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  LayoutDashboard, 
  PlusCircle, 
  Activity, 
  Sliders, 
  BellRing, 
  Cpu, 
  LogOut, 
  ChevronLeft, 
  ChevronRight,
  ShieldCheck
} from 'lucide-react';
import { InstallAppButton } from './InstallAppButton';

export const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  isCollapsed, 
  setIsCollapsed, 
  user, 
  onLogout,
  isBackendOnline 
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
    { id: 'register-animal', label: 'Register Animal', icon: PlusCircle, badge: 'New' },
    { id: 'animals', label: 'Herd Surveillance', icon: Activity },
    { id: 'live-monitoring', label: 'Live IoT Simulator', icon: Sliders },
    { id: 'alerts', label: 'Decision Alerts', icon: BellRing },
    { id: 'model-performance', label: 'ML Performance', icon: Cpu },
  ];

  return (
    <aside
      className={`sticky top-0 h-screen bg-white border-r border-slate-200 shadow-[4px_0_24px_rgba(0,0,0,0.03)] flex flex-col justify-between transition-all duration-300 z-40 ${
        isCollapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Top Header & Brand */}
      <div>
        <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100">
          <div 
            className="flex items-center gap-3 cursor-pointer overflow-hidden"
            onClick={() => setActiveTab('dashboard')}
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-md shadow-emerald-500/25 shrink-0">
              <span className="text-xl font-black text-white">BM</span>
            </div>
            {!isCollapsed && (
              <div className="animate-fadeIn">
                <span className="font-extrabold text-base tracking-tight text-slate-900 block leading-tight">
                  BovineGuard
                </span>
                <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-wider block">
                  AI Surveillance
                </span>
              </div>
            )}
          </div>

          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-500 hover:text-slate-800 transition"
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Menu Items */}
        <nav className="p-3 space-y-1.5 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                title={isCollapsed ? item.label : undefined}
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-2xl text-xs font-bold transition-all duration-200 group ${
                  isActive
                    ? 'btn-3d-emerald text-white shadow-md shadow-emerald-600/30'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                }`}
              >
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-white' : 'text-slate-500 group-hover:text-slate-800'}`} />
                
                {!isCollapsed && (
                  <div className="flex-1 flex items-center justify-between overflow-hidden animate-fadeIn">
                    <span className="truncate">{item.label}</span>
                    {item.badge && (
                      <span className={`px-1.5 py-0.5 text-[9px] font-bold rounded uppercase ${
                        isActive ? 'bg-white/20 text-white' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom User Card & Status */}
      <div className="p-3 border-t border-slate-100 space-y-2.5">
        <InstallAppButton isCollapsed={isCollapsed} />

        <div className={`p-2.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center gap-2">
            <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${isBackendOnline ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            {!isCollapsed && (
              <span className="text-[11px] font-bold text-slate-700">
                {isBackendOnline ? 'AI Model Online' : 'Connecting API'}
              </span>
            )}
          </div>
          {!isCollapsed && (
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          )}
        </div>

        {user && (
          <div className={`p-2 rounded-2xl bg-white border border-slate-200/90 shadow-2xs flex items-center ${isCollapsed ? 'justify-center' : 'justify-between gap-2'}`}>
            <div className="flex items-center gap-2 overflow-hidden">
              <div className="w-8 h-8 rounded-xl bg-emerald-100 border border-emerald-200 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0">
                {user.name ? user.name.charAt(0) : 'U'}
              </div>
              {!isCollapsed && (
                <div className="overflow-hidden">
                  <span className="text-xs font-bold text-slate-900 block truncate">{user.name || user.username}</span>
                  <span className="text-[10px] text-slate-500 font-medium block truncate">{user.role || 'Veterinarian'}</span>
                </div>
              )}
            </div>
            {!isCollapsed && (
              <button
                onClick={onLogout}
                title="Log out"
                className="p-1.5 rounded-xl hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition shrink-0"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        )}
      </div>
    </aside>
  );
};
""")

# 2. Update Header.jsx (Remove All-In-One view button)
with open("frontend/src/components/Header.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { PlusCircle, Search } from 'lucide-react';

export const Header = ({ activeTab, setActiveTab }) => {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'dashboard': return { title: 'Executive Herd Dashboard', sub: 'Real-time herd risk segmentation & analytics' };
      case 'register-animal': return { title: 'Animal Registration', sub: 'Enroll new bovine into active AI surveillance' };
      case 'animals': return { title: 'Herd Surveillance Master Inventory', sub: 'Surveillance across 12,000+ cattle records' };
      case 'live-monitoring': return { title: 'Live IoT Sensor Simulator', sub: 'Interactive biometric & milking telemetry testing' };
      case 'alerts': return { title: 'Decision-Support Alert Center', sub: 'Threshold alerts & California Mastitis Test (CMT) guidance' };
      case 'model-performance': return { title: 'XGBoost ML Performance Analytics', sub: 'Accuracy, confusion matrix & feature importance' };
      case 'animal-detail': return { title: 'Individual Bovine Profile', sub: '7-day sensor telemetry & AI risk diagnostics' };
      default: return { title: 'Herd Surveillance', sub: 'Bovine Mastitis Early Forecasting' };
    }
  };

  const { title, sub } = getTabTitle();

  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      <div>
        <h1 className="text-base font-black text-slate-900 leading-tight">{title}</h1>
        <p className="text-xs text-slate-500 font-medium">{sub}</p>
      </div>

      <div className="flex items-center gap-3">
        {activeTab !== 'register-animal' && (
          <button
            onClick={() => setActiveTab('register-animal')}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl btn-3d-emerald text-white text-xs font-bold shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Register Animal</span>
          </button>
        )}
      </div>
    </header>
  );
};
""")

# 3. Update App.jsx (Single focused page per tab)
with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
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
""")

print("Removed All-in-One view. App is now pure page-by-page.")
