# -*- coding: utf-8 -*-
# 1. Create components/Header.jsx
with open("frontend/src/components/Header.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { PlusCircle, Search, Sparkles, Bell, Layers } from 'lucide-react';

export const Header = ({ activeTab, setActiveTab, onQuickRegister }) => {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'all-in-one': return { title: 'All-In-One Unified Surveillance', sub: 'Complete end-to-end monitoring overview' };
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
        {/* Quick Action Button */}
        {activeTab !== 'register-animal' && (
          <button
            onClick={() => setActiveTab('register-animal')}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl btn-3d-emerald text-white text-xs font-bold shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Register Animal</span>
          </button>
        )}

        {activeTab !== 'all-in-one' && (
          <button
            onClick={() => setActiveTab('all-in-one')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl btn-3d-slate text-slate-700 text-xs font-bold hover:border-slate-300"
          >
            <Layers className="w-3.5 h-3.5 text-emerald-600" />
            <span className="hidden sm:inline">All-in-One View</span>
          </button>
        )}
      </div>
    </header>
  );
};
""")

# 2. Update App.jsx with Left Sidebar + Top Header + Main Layout
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
import { 
  LayoutDashboard, 
  PlusCircle, 
  Activity, 
  Sliders, 
  BellRing, 
  Cpu, 
  Layers
} from 'lucide-react';

export function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('bovine_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [activeTab, setActiveTab] = useState('all-in-one');
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
    setActiveTab('all-in-one');
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

  const scrollToSection = (sectionId) => {
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
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
          onQuickRegister={() => setActiveTab('register-animal')}
        />

        {/* Content Body with Proper Balanced Alignment */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto space-y-8">
          
          {/* VIEW A: UNIFIED ALL-IN-ONE VIEW */}
          {activeTab === 'all-in-one' && (
            <div className="space-y-12">
              
              {/* Section 1: Executive Dashboard */}
              <section id="sec-dashboard" className="space-y-4">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
                    <LayoutDashboard className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Executive Dashboard</h2>
                    <p className="text-xs text-slate-500">Real-time herd risk segmentation & sensor averages</p>
                  </div>
                </div>
                <Dashboard 
                  data={dashboardData} 
                  onSelectAnimal={handleSelectAnimal}
                  onNavigate={(tab) => {
                    if (tab === 'alerts') scrollToSection('sec-alerts');
                    else if (tab === 'animals') scrollToSection('sec-herd');
                    else setActiveTab(tab);
                  }}
                />
              </section>

              {/* Section 2: Animal Registration */}
              <section id="sec-register" className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-sky text-sky-700">
                    <PlusCircle className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Animal Registration</h2>
                    <p className="text-xs text-slate-500">Enroll new bovine with 1-click sample presets & instant AI risk calculation</p>
                  </div>
                </div>
                <AnimalRegistration 
                  onRegistrationSuccess={handleRegistrationSuccess}
                  onInspectAnimal={handleSelectAnimal}
                />
              </section>

              {/* Section 3: Herd Surveillance Master Inventory */}
              <section id="sec-herd" className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
                    <Activity className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Herd Surveillance Master Inventory</h2>
                    <p className="text-xs text-slate-500">Surveillance over 12,000+ cattle records loaded directly from Excel</p>
                  </div>
                </div>
                <Animals onSelectAnimal={handleSelectAnimal} />
              </section>

              {/* Section 4: Live IoT Simulator */}
              <section id="sec-iot" className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-amber text-amber-700">
                    <Sliders className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Live IoT Hardware Simulator</h2>
                    <p className="text-xs text-slate-500">Interactive telemetry testing triggering real-time ML inference</p>
                  </div>
                </div>
                <LiveSensorMonitoring initialCowData={simulatedCowData} />
              </section>

              {/* Section 5: Decision Alerts */}
              <section id="sec-alerts" className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-rose text-rose-700">
                    <BellRing className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Decision Alerts & Screening Center</h2>
                    <p className="text-xs text-slate-500">Configurable risk thresholds & California Mastitis Test (CMT) alerts</p>
                  </div>
                </div>
                <Alerts onSelectAnimal={handleSelectAnimal} />
              </section>

              {/* Section 6: Model Performance Analytics */}
              <section id="sec-ml" className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2.5 pb-2 border-b border-slate-200">
                  <div className="p-2 rounded-xl icon-3d-sky text-sky-700">
                    <Cpu className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">XGBoost ML Performance Analytics</h2>
                    <p className="text-xs text-slate-500">Accuracy metrics, feature importance rankings & confusion matrix</p>
                  </div>
                </div>
                <ModelPerformance />
              </section>

            </div>
          )}

          {/* VIEW B: INDIVIDUAL FOCUSED VIEWS */}
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
              onBack={() => setActiveTab('all-in-one')}
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

print("Header.jsx created and App.jsx updated with proper sidebar alignment.")
