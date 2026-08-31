# -*- coding: utf-8 -*-
# 1. Update index.html
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
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-50 text-slate-900 antialiased selection:bg-emerald-500 selection:text-white font-sans">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

# 2. Update components/RiskBadge.jsx
with open("frontend/src/components/RiskBadge.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, Flame } from 'lucide-react';

export const RiskBadge = ({ category, score, size = 'md' }) => {
  const getBadgeConfig = () => {
    switch (category) {
      case 'No_Risk':
        return {
          label: 'No Risk',
          bg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          dot: 'bg-emerald-500',
          icon: ShieldCheck,
        };
      case 'Low':
        return {
          label: 'Low Risk',
          bg: 'bg-sky-50 text-sky-700 border-sky-200',
          dot: 'bg-sky-500',
          icon: AlertCircle,
        };
      case 'Moderate':
        return {
          label: 'Moderate Risk',
          bg: 'bg-amber-50 text-amber-700 border-amber-200',
          dot: 'bg-amber-500',
          icon: AlertTriangle,
        };
      case 'High':
        return {
          label: 'High Risk',
          bg: 'bg-rose-50 text-rose-700 border-rose-200',
          dot: 'bg-rose-500',
          icon: Flame,
        };
      default:
        return {
          label: category || 'Unknown',
          bg: 'bg-slate-100 text-slate-700 border-slate-200',
          dot: 'bg-slate-400',
          icon: AlertCircle,
        };
    }
  };

  const { label, bg, dot, icon: Icon } = getBadgeConfig();
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : size === 'lg' ? 'px-3 py-1.5 text-sm font-semibold' : 'px-2.5 py-1 text-xs font-medium';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${bg} ${sizeClasses} shadow-sm transition`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dot} animate-pulse`} />
      <Icon className="w-3.5 h-3.5" />
      <span>{label}</span>
      {score !== undefined && score !== null && (
        <span className="font-mono font-bold ml-1 opacity-90">
          ({typeof score === 'number' ? score.toFixed(1) : score}%)
        </span>
      )}
    </span>
  );
};
""")

# 3. Update components/MetricCard.jsx
with open("frontend/src/components/MetricCard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';

export const MetricCard = ({ title, value, subtext, icon: Icon, color = 'emerald' }) => {
  const colorMap = {
    emerald: { bg: 'bg-emerald-50 text-emerald-600 border-emerald-100', text: 'text-emerald-700', val: 'text-slate-900' },
    sky: { bg: 'bg-sky-50 text-sky-600 border-sky-100', text: 'text-sky-700', val: 'text-slate-900' },
    amber: { bg: 'bg-amber-50 text-amber-600 border-amber-100', text: 'text-amber-700', val: 'text-slate-900' },
    rose: { bg: 'bg-rose-50 text-rose-600 border-rose-100', text: 'text-rose-700', val: 'text-rose-600' },
    purple: { bg: 'bg-purple-50 text-purple-600 border-purple-100', text: 'text-purple-700', val: 'text-slate-900' },
  };

  const scheme = colorMap[color] || colorMap.emerald;

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</span>
        <div className={`p-2.5 rounded-xl border ${scheme.bg} shadow-sm`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="mt-3">
        <div className={`text-2xl font-black font-mono tracking-tight ${scheme.val}`}>
          {value}
        </div>
        {subtext && (
          <p className="text-xs text-slate-500 mt-1 flex items-center gap-1 font-medium">
            <span>{subtext}</span>
          </p>
        )}
      </div>
    </div>
  );
};
""")

# 4. Update components/AlertBanner.jsx
with open("frontend/src/components/AlertBanner.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { AlertOctagon, ArrowRight } from 'lucide-react';

export const AlertBanner = ({ alerts = [], onSelectAnimal }) => {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="bg-gradient-to-r from-rose-50 to-amber-50 border border-rose-200 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-rose-500 text-white shadow-sm shadow-rose-500/20 shrink-0">
          <AlertOctagon className="w-5 h-5 animate-pulse" />
        </div>
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-rose-800">
            {alerts.length} High-Risk Alert{alerts.length > 1 ? 's' : ''} Detected
          </h4>
          <p className="text-xs text-slate-600 mt-0.5">
            Animals showing acute physiological deviation (elevated milk conductivity or body temperature) requiring California Mastitis Test (CMT) verification.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 overflow-x-auto pb-1 md:pb-0">
        {alerts.slice(0, 3).map((item) => (
          <button
            key={item.animal_id}
            onClick={() => onSelectAnimal(item.animal_id)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-rose-200 hover:border-rose-400 text-xs font-semibold text-rose-700 shadow-xs hover:shadow transition shrink-0"
          >
            <span>Cow #{item.animal_id} ({item.risk_score}%)</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        ))}
      </div>
    </div>
  );
};
""")

# 5. Update components/EnvironmentalCard.jsx
with open("frontend/src/components/EnvironmentalCard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Thermometer, Droplets, Wind, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const EnvironmentalCard = ({ envData }) => {
  if (!envData) return null;

  const isFavorable = envData.conditions_favorable_for_pathogens;

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-900">Barn Microclimate & THI</h3>
          <p className="text-xs text-slate-500">Pathogen proliferation risk conditions</p>
        </div>
        <div className={`p-2 rounded-xl border ${isFavorable ? 'bg-amber-50 text-amber-600 border-amber-200' : 'bg-emerald-50 text-emerald-600 border-emerald-200'}`}>
          <Wind className="w-4 h-4" />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center mb-4">
        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <div className="flex items-center justify-center gap-1 text-slate-500 mb-1">
            <Thermometer className="w-3.5 h-3.5" />
            <span className="text-[10px] font-semibold uppercase">Ambient</span>
          </div>
          <span className="text-sm font-bold font-mono text-slate-800">{envData.ambient_temperature_c} °C</span>
        </div>

        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <div className="flex items-center justify-center gap-1 text-slate-500 mb-1">
            <Droplets className="w-3.5 h-3.5" />
            <span className="text-[10px] font-semibold uppercase">Humidity</span>
          </div>
          <span className="text-sm font-bold font-mono text-slate-800">{envData.relative_humidity_pct} %</span>
        </div>

        <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <div className="flex items-center justify-center gap-1 text-slate-500 mb-1">
            <Wind className="w-3.5 h-3.5" />
            <span className="text-[10px] font-semibold uppercase">THI Index</span>
          </div>
          <span className={`text-sm font-bold font-mono ${envData.average_thi >= 72 ? 'text-amber-600' : 'text-emerald-600'}`}>
            {envData.average_thi}
          </span>
        </div>
      </div>

      <div className={`p-3 rounded-xl border flex items-start gap-2.5 ${isFavorable ? 'bg-amber-50/70 border-amber-200 text-amber-800' : 'bg-emerald-50/70 border-emerald-200 text-emerald-800'}`}>
        {isFavorable ? (
          <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        ) : (
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
        )}
        <div className="text-xs">
          <span className="font-bold block">
            {isFavorable ? 'Pathogen Proliferation Warning' : 'Optimal Barn Microclimate'}
          </span>
          <p className="text-[11px] opacity-90 mt-0.5 leading-snug">
            {isFavorable
              ? 'Elevated Heat-Humidity Index (THI >= 72). Increase stall ventilation and replace bedding to limit bacterial exposure.'
              : 'Ambient temperature and humidity are within ideal bounds for herd thermal comfort.'}
          </p>
        </div>
      </div>
    </div>
  );
};
""")

# 6. Update components/Navbar.jsx
with open("frontend/src/components/Navbar.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  LayoutDashboard, 
  Activity, 
  Sliders, 
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
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur-md shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-md shadow-emerald-500/20">
              <span className="text-xl font-black text-white">BM</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-base tracking-tight text-slate-900">BovineGuard AI</span>
                <span className="px-1.5 py-0.5 text-[10px] font-bold uppercase rounded bg-emerald-100 text-emerald-800 border border-emerald-200">
                  Surveillance
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">
                Bovine Mastitis Early Forecasting System
              </p>
            </div>
          </div>

          {/* Desktop Nav Items */}
          <nav className="hidden lg:flex items-center gap-1 bg-slate-100/80 p-1 rounded-xl border border-slate-200/80">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-white text-emerald-700 shadow-sm border border-slate-200/60'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="px-1.5 py-0.2 text-[9px] font-bold rounded bg-emerald-100 text-emerald-700 uppercase">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right Header */}
          <div className="flex items-center gap-3">
            
            {/* Backend status indicator */}
            <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs">
              <div className={`w-2 h-2 rounded-full ${isBackendOnline ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-[11px] font-medium text-slate-600">
                {isBackendOnline ? 'AI Model Online' : 'Connecting'}
              </span>
            </div>

            {/* User Profile & Logout */}
            {user && (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
                <div className="text-right hidden sm:block">
                  <span className="text-xs font-bold text-slate-800 block">{user.name || user.username}</span>
                  <span className="text-[10px] font-medium text-emerald-600 block">{user.role || 'Veterinarian'}</span>
                </div>
                <button
                  onClick={onLogout}
                  title="Log out"
                  className="p-2 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-600 border border-slate-200 hover:border-rose-200 text-slate-500 transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            )}

          </div>

        </div>
      </div>

      {/* Mobile Nav Bar */}
      <div className="lg:hidden flex overflow-x-auto px-4 py-2 gap-1 border-t border-slate-200 bg-slate-50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex shrink-0 items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${
                isActive ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-600 bg-white border border-slate-200'
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

print("Clean White Theme: Core components updated.")
