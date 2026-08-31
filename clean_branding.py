# -*- coding: utf-8 -*-
import os

# 1. Update frontend/index.html
with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write("""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BovineGuard AI | Bovine Mastitis Early Forecasting System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-950 text-slate-100 antialiased selection:bg-emerald-500 selection:text-white font-sans">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

# 2. Update frontend/src/components/Navbar.jsx
with open("frontend/src/components/Navbar.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  LayoutDashboard, 
  Activity, 
  Sliders, 
  Binary, 
  BellRing, 
  Cpu, 
  PlusCircle,
  LogOut
} from 'lucide-react';

export const Navbar = ({ activeTab, setActiveTab, isBackendOnline, user, onLogout }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'register-animal', label: 'Register Animal', icon: PlusCircle, badge: 'New' },
    { id: 'animals', label: 'Herd Animals', icon: Activity },
    { id: 'live-monitoring', label: 'Live IoT Simulator', icon: Sliders },
    { id: 'alerts', label: 'Decision Alerts', icon: BellRing },
    { id: 'model-performance', label: 'ML Performance', icon: Cpu },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <span className="text-xl font-black text-slate-950">BM</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-base tracking-tight text-white">BovineGuard AI</span>
                <span className="px-1.5 py-0.5 text-[10px] font-bold uppercase rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  Surveillance
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Bovine Mastitis Early Forecasting System
              </p>
            </div>
          </div>

          {/* Nav Items */}
          <nav className="hidden lg:flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800/60">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="px-1 py-0.2 text-[9px] font-bold rounded bg-emerald-400/20 text-emerald-300 uppercase">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right: User & Status */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
              <div className={`w-2 h-2 rounded-full ${isBackendOnline ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-[11px] text-slate-300">
                {isBackendOnline ? 'AI Model Online' : 'Connecting'}
              </span>
            </div>

            {user && (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
                <div className="text-right hidden sm:block">
                  <span className="text-xs font-semibold text-white block">{user.name || user.username}</span>
                  <span className="text-[10px] text-emerald-400 block">{user.role || 'Veterinarian'}</span>
                </div>
                <button
                  onClick={onLogout}
                  title="Log out"
                  className="p-2 rounded-xl bg-slate-900 hover:bg-rose-500/20 hover:text-rose-400 border border-slate-800 hover:border-rose-500/30 text-slate-400 transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Mobile Nav */}
      <div className="lg:hidden flex overflow-x-auto px-4 py-2 gap-1 border-t border-slate-800/60 bg-slate-900/40">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex shrink-0 items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium ${
                isActive ? 'bg-emerald-600 text-white' : 'text-slate-300 bg-slate-800/40'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
};
""")

# 3. Update frontend/src/pages/Login.jsx
with open("frontend/src/pages/Login.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import { ShieldCheck, LogIn, User, Lock, AlertCircle } from 'lucide-react';
import { loginUser } from '../services/api';

export const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('password');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!username.trim()) {
      setError('Please enter a valid username');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const data = await loginUser({ username, password });
      if (data.success) {
        onLoginSuccess(data.user);
      } else {
        setError('Login failed. Please check credentials.');
      }
    } catch (err) {
      const demoUser = {
        username: username || 'admin',
        name: username === 'admin' ? 'Dr. Ramesh Sharma' : 'Dairy Farm Manager',
        role: username === 'admin' ? 'Chief Herd Veterinarian' : 'Farm Operations Lead',
        farm: 'Dairy Research Station'
      };
      onLoginSuccess(demoUser);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = (roleKey) => {
    if (roleKey === 'vet') {
      setUsername('admin');
      setPassword('password');
    } else {
      setUsername('manager');
      setPassword('password');
    }
    setTimeout(() => {
      handleSubmit();
    }, 100);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md space-y-6 z-10">
        
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 shadow-xl shadow-emerald-500/20 mb-2">
            <span className="text-2xl font-black text-slate-950">BM</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <h1 className="text-2xl font-bold text-white tracking-tight">BovineGuard AI</h1>
          </div>
          <p className="text-xs text-slate-400 max-w-xs mx-auto">
            AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis
          </p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl shadow-slate-950">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Username / Personnel ID
              </label>
              <div className="relative">
                <User className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. admin or vet01"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-emerald-600/20 disabled:opacity-50 mt-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
              ) : (
                <LogIn className="w-4 h-4" />
              )}
              <span>Access Surveillance Dashboard</span>
            </button>
          </form>

          <div className="mt-6 pt-5 border-t border-slate-800">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block text-center mb-3">
              One-Click Presentation Logins
            </span>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleQuickDemo('vet')}
                className="p-2.5 rounded-xl bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/40 text-left transition flex items-center gap-2"
              >
                <div className="w-2 h-2 rounded-full bg-emerald-400" />
                <div>
                  <span className="text-xs font-semibold text-white block">Dr. Sharma</span>
                  <span className="text-[10px] text-slate-400 block">Veterinarian</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo('manager')}
                className="p-2.5 rounded-xl bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/40 text-left transition flex items-center gap-2"
              >
                <div className="w-2 h-2 rounded-full bg-sky-400" />
                <div>
                  <span className="text-xs font-semibold text-white block">S. Patel</span>
                  <span className="text-[10px] text-slate-400 block">Farm Manager</span>
                </div>
              </button>
            </div>
          </div>

        </div>

        <div className="flex items-center justify-center gap-1.5 text-center text-xs text-slate-500">
          <ShieldCheck className="w-4 h-4 text-emerald-500" />
          <span>Offline & Cloud Compatible &bull; Direct Pandas Engine</span>
        </div>

      </div>
    </div>
  );
};
""")

# 4. Update frontend/src/App.jsx
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

export function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('bovine_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [activeTab, setActiveTab] = useState('dashboard');
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
  };

  const handleSimulateWithCow = (cow) => {
    setSimulatedCowData(cow);
    setActiveTab('live-monitoring');
  };

  const handleRegistrationSuccess = (newCow) => {
    initData();
  };

  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-white">
      
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

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
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

      <footer className="border-t border-slate-800/80 bg-slate-950 py-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis</span>
          <span>Logged in as <strong>{user.name}</strong> ({user.role})</span>
        </div>
      </footer>

    </div>
  );
}

export default App;
""")

# 5. Update backend/app/config.py
with open("backend/app/config.py", "w", encoding="utf-8") as f:
    f.write("""import os

class Settings:
    PROJECT_NAME: str = "BovineGuard AI - Bovine Mastitis Predictive Modelling"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Based Early Forecasting of Bovine Mastitis in Indian Dairy Farms"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    DATA_FILE_PATH: str = os.getenv(
        "DATA_FILE_PATH",
        os.path.join(os.path.dirname(__file__), "../../data/mastitis_dataset.xlsx")
    )
    
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
""")

print("Cleaned up branding and simplified navigation.")
