# -*- coding: utf-8 -*-
with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
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
  Layers,
  ArrowUp
} from 'lucide-react';

export function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('bovine_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [activeTab, setActiveTab] = useState('all-in-one'); // Default to clean All-in-One view as requested
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
    if (activeTab !== 'all-in-one') {
      setActiveTab('all-in-one');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  const slideNavItems = [
    { id: 'all-in-one', label: 'All-In-One Unified View', icon: Layers },
    { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard, anchor: 'sec-dashboard' },
    { id: 'register-animal', label: 'Register Animal', icon: PlusCircle, anchor: 'sec-register' },
    { id: 'animals', label: 'Herd Surveillance', icon: Activity, anchor: 'sec-herd' },
    { id: 'live-monitoring', label: 'IoT Simulator', icon: Sliders, anchor: 'sec-iot' },
    { id: 'alerts', label: 'Decision Alerts', icon: BellRing, anchor: 'sec-alerts' },
    { id: 'model-performance', label: 'ML Analytics', icon: Cpu, anchor: 'sec-ml' },
  ];

  return (
    <div className="min-h-screen bg-slate-100/70 text-slate-900 flex flex-col selection:bg-emerald-500 selection:text-white font-sans">
      
      {/* Top Navbar */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          setActiveTab(tab);
          if (tab !== 'animal-detail') setSelectedAnimalId(null);
        }} 
        isBackendOnline={isBackendOnline}
        user={user}
        onLogout={handleLogout}
      />

      {/* 3D Modern Toggle Slide Bar */}
      <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-2">
        <div className="bg-white/95 border border-slate-200/90 rounded-2xl p-1.5 shadow-[0_8px_20px_-4px_rgba(15,23,42,0.06),inset_0_1px_0_rgba(255,255,255,1)] flex items-center gap-1.5 overflow-x-auto">
          {slideNavItems.map((item) => {
            const Icon = item.icon;
            const isSelected = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.anchor && activeTab === 'all-in-one') {
                    scrollToSection(item.anchor);
                  } else {
                    setActiveTab(item.id);
                    if (item.id !== 'animal-detail') setSelectedAnimalId(null);
                  }
                }}
                className={`flex shrink-0 items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 ${
                  isSelected
                    ? 'btn-3d-emerald text-white shadow-md'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isSelected ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4 space-y-12">
        
        {/* VIEW A: UNIFIED ALL-IN-ONE SINGLE PAGE */}
        {activeTab === 'all-in-one' && (
          <div className="space-y-14">
            
            {/* Section 1: Dashboard Overview & KPI Metrics */}
            <section id="sec-dashboard" className="space-y-4 pt-2">
              <div className="flex items-center justify-between pb-1 border-b border-slate-200/80">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
                    <LayoutDashboard className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl font-black text-slate-900 tracking-tight">Executive Dashboard</h2>
                    <p className="text-xs text-slate-500">Real-time herd risk segmentation and sensor telemetry overview</p>
                  </div>
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
              <div className="flex items-center gap-2.5 pb-1 border-b border-slate-200/80">
                <div className="p-2 rounded-xl icon-3d-sky text-sky-700">
                  <PlusCircle className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-black text-slate-900 tracking-tight">Animal Registration</h2>
                  <p className="text-xs text-slate-500">Enroll new animals with automated sample presets and instant AI evaluation</p>
                </div>
              </div>
              <AnimalRegistration 
                onRegistrationSuccess={handleRegistrationSuccess}
                onInspectAnimal={handleSelectAnimal}
              />
            </section>

            {/* Section 3: Herd Surveillance Table */}
            <section id="sec-herd" className="space-y-4 pt-4 border-t border-slate-200">
              <div className="flex items-center gap-2.5 pb-1 border-b border-slate-200/80">
                <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-black text-slate-900 tracking-tight">Herd Surveillance Master Inventory</h2>
                  <p className="text-xs text-slate-500">Live surveillance over 12,000+ cattle loaded directly from Excel</p>
                </div>
              </div>
              <Animals onSelectAnimal={handleSelectAnimal} />
            </section>

            {/* Section 4: Live IoT Simulator */}
            <section id="sec-iot" className="space-y-4 pt-4 border-t border-slate-200">
              <div className="flex items-center gap-2.5 pb-1 border-b border-slate-200/80">
                <div className="p-2 rounded-xl icon-3d-amber text-amber-700">
                  <Sliders className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-black text-slate-900 tracking-tight">Live IoT Hardware Simulator</h2>
                  <p className="text-xs text-slate-500">Interactive sensor telemetry simulation triggering real-time ML inference</p>
                </div>
              </div>
              <LiveSensorMonitoring initialCowData={simulatedCowData} />
            </section>

            {/* Section 5: Decision Alerts */}
            <section id="sec-alerts" className="space-y-4 pt-4 border-t border-slate-200">
              <div className="flex items-center gap-2.5 pb-1 border-b border-slate-200/80">
                <div className="p-2 rounded-xl icon-3d-rose text-rose-700">
                  <BellRing className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-black text-slate-900 tracking-tight">Decision Alerts & Screening Guidance</h2>
                  <p className="text-xs text-slate-500">Configurable risk thresholds and California Mastitis Test (CMT) alerts</p>
                </div>
              </div>
              <Alerts onSelectAnimal={handleSelectAnimal} />
            </section>

            {/* Section 6: Model Performance & Analytics */}
            <section id="sec-ml" className="space-y-4 pt-4 border-t border-slate-200">
              <div className="flex items-center gap-2.5 pb-1 border-b border-slate-200/80">
                <div className="p-2 rounded-xl icon-3d-sky text-sky-700">
                  <Cpu className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-black text-slate-900 tracking-tight">XGBoost ML Performance Analytics</h2>
                  <p className="text-xs text-slate-500">Model evaluation metrics, feature importance rankings, and confusion matrix</p>
                </div>
              </div>
              <ModelPerformance />
            </section>

          </div>
        )}

        {/* VIEW B: INDIVIDUAL TAB VIEWS */}
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
      <footer className="border-t border-slate-200 bg-white py-5 text-center text-xs text-slate-500 mt-12 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>BovineGuard AI &bull; Bovine Mastitis Early Forecasting Platform</span>
          </div>
          <span>Logged in as <strong className="text-slate-800 font-bold">{user.name}</strong> ({user.role})</span>
        </div>
      </footer>

    </div>
  );
}

export default App;
""")

print("App.jsx updated with Toggle Slide Bar and All-In-One Unified layout.")
