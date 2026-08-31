# -*- coding: utf-8 -*-
import os

os.makedirs("frontend/src/components", exist_ok=True)
os.makedirs("frontend/src/pages", exist_ok=True)
os.makedirs("frontend/src/services", exist_ok=True)
os.makedirs("frontend/src/charts", exist_ok=True)

# 1. index.css
with open("frontend/src/index.css", "w", encoding="utf-8") as f:
    f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  background-color: #030712;
  color: #f3f4f6;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #0b0f19;
}
::-webkit-scrollbar-thumb {
  background: #1f293d;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #374151;
}
""")

# 2. services/api.js
with open("frontend/src/services/api.js", "w", encoding="utf-8") as f:
    f.write("""import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchHealth = async () => {
  const res = await apiClient.get('/health');
  return res.data;
};

export const fetchDashboard = async () => {
  const res = await apiClient.get('/dashboard');
  return res.data;
};

export const fetchAnimals = async (params = {}) => {
  const res = await apiClient.get('/animals', { params });
  return res.data;
};

export const fetchAnimalDetail = async (animalId) => {
  const res = await apiClient.get(`/animals/${animalId}`);
  return res.data;
};

export const fetchSensorData = async (animalId) => {
  const res = await apiClient.get(`/sensor-data/${animalId}`);
  return res.data;
};

export const fetchAnimalPrediction = async (animalId) => {
  const res = await apiClient.get(`/predictions/${animalId}`);
  return res.data;
};

export const predictRisk = async (payload) => {
  const res = await apiClient.post('/predict', payload);
  return res.data;
};

export const fetchModelPerformance = async () => {
  const res = await apiClient.get('/model-performance');
  return res.data;
};
""")

# 3. components/RiskBadge.jsx
with open("frontend/src/components/RiskBadge.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { ShieldCheck, AlertTriangle, AlertCircle, Flame } from 'lucide-react';

export const RiskBadge = ({ category, score = null, size = 'md' }) => {
  const cat = (category || 'No_Risk').replace(/_/g, ' ');
  
  let colorStyle = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
  let Icon = ShieldCheck;

  if (cat.toLowerCase().includes('high')) {
    colorStyle = 'bg-rose-500/15 text-rose-400 border-rose-500/40 shadow-sm shadow-rose-500/10';
    Icon = Flame;
  } else if (cat.toLowerCase().includes('moderate')) {
    colorStyle = 'bg-amber-500/15 text-amber-400 border-amber-500/40';
    Icon = AlertTriangle;
  } else if (cat.toLowerCase().includes('low')) {
    colorStyle = 'bg-sky-500/15 text-sky-400 border-sky-500/30';
    Icon = AlertCircle;
  }

  const sizeStyle = size === 'sm' 
    ? 'px-2 py-0.5 text-[11px] font-medium' 
    : size === 'lg' 
    ? 'px-3.5 py-1.5 text-sm font-semibold' 
    : 'px-2.5 py-1 text-xs font-semibold';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${colorStyle} ${sizeStyle}`}>
      <Icon className={size === 'lg' ? 'w-4 h-4' : 'w-3.5 h-3.5'} />
      <span>{cat.toUpperCase()}</span>
      {score !== null && (
        <span className="opacity-80 font-mono text-[11px]">
          ({score}%)
        </span>
      )}
    </span>
  );
};
""")

# 4. components/MetricCard.jsx
with open("frontend/src/components/MetricCard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';

export const MetricCard = ({ title, value, subtext, icon: Icon, color = 'emerald', trend = null }) => {
  const colorMap = {
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    rose: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    sky: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md hover:border-slate-700 transition duration-200">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2.5 rounded-xl border ${colorMap[color] || colorMap.emerald}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-3xl font-bold tracking-tight text-white font-mono">{value}</span>
        {trend && (
          <span className="text-xs text-emerald-400 font-medium">{trend}</span>
        )}
      </div>
      {subtext && <p className="mt-1 text-xs text-slate-400">{subtext}</p>}
    </div>
  );
};
""")

# 5. components/Navbar.jsx
with open("frontend/src/components/Navbar.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  LayoutDashboard, 
  Activity, 
  Sliders, 
  Binary, 
  BellRing, 
  Cpu 
} from 'lucide-react';

export const Navbar = ({ activeTab, setActiveTab, isBackendOnline }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'animals', label: 'Herd Animals', icon: Activity },
    { id: 'live-monitoring', label: 'Live IoT Simulator', icon: Sliders, highlight: true },
    { id: 'predictions', label: 'Predictions Log', icon: Binary },
    { id: 'alerts', label: 'Decision Alerts', icon: BellRing },
    { id: 'model-performance', label: 'ML Performance', icon: Cpu },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <span className="text-xl font-black text-slate-950">BM</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-base tracking-tight text-white">BovineGuard AI</span>
                <span className="px-1.5 py-0.5 text-[10px] font-bold uppercase rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  SIH 2026
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Early Forecasting of Bovine Mastitis
              </p>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800/60">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  } ${item.highlight && !isActive ? 'text-emerald-400' : ''}`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
              <div className={`w-2 h-2 rounded-full ${isBackendOnline ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-[11px] text-slate-300 hidden sm:inline">
                {isBackendOnline ? 'FastAPI + XGBoost Online' : 'Connecting Backend...'}
              </span>
            </div>
          </div>

        </div>
      </div>

      <div className="md:hidden flex overflow-x-auto px-4 py-2 gap-1 border-t border-slate-800/60 bg-slate-900/40">
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

# 6. components/EnvironmentalCard.jsx
with open("frontend/src/components/EnvironmentalCard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Thermometer, Droplets, Gauge, AlertTriangle, ShieldCheck } from 'lucide-react';

export const EnvironmentalCard = ({ envData }) => {
  if (!envData) return null;

  const temp = envData.ambient_temperature_c || 28.0;
  const hum = envData.relative_humidity_pct || 72.0;
  const thi = envData.average_thi || (0.8 * temp + (hum / 100) * (temp - 14.4) + 46.4).toFixed(1);
  const isElevated = envData.conditions_favorable_for_pathogens || thi >= 72;

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-white">Barn Environmental Risk Monitor</h3>
          <p className="text-xs text-slate-400">Microclimate Temperature-Humidity Index (THI)</p>
        </div>
        <div className={`px-2.5 py-1 rounded-full text-xs font-medium border flex items-center gap-1.5 ${
          isElevated
            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
            : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
        }`}>
          {isElevated ? <AlertTriangle className="w-3.5 h-3.5" /> : <ShieldCheck className="w-3.5 h-3.5" />}
          <span>{isElevated ? 'Pathogen-Favorable Microclimate' : 'Optimum Barn Climate'}</span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <Thermometer className="w-3.5 h-3.5 text-amber-400" />
            <span>Ambient Temp</span>
          </div>
          <span className="text-lg font-bold font-mono text-white">{temp}°C</span>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <Droplets className="w-3.5 h-3.5 text-sky-400" />
            <span>Rel. Humidity</span>
          </div>
          <span className="text-lg font-bold font-mono text-white">{hum}%</span>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <Gauge className="w-3.5 h-3.5 text-purple-400" />
            <span>THI Index</span>
          </div>
          <span className="text-lg font-bold font-mono text-white">{thi}</span>
        </div>
      </div>

      <p className="mt-3 text-[11px] text-slate-400 leading-relaxed border-t border-slate-800/60 pt-2">
        <strong className="text-slate-300">Scientific Context: </strong>
        Elevated THI (≥72) and humid bedding conditions foster opportunistic environmental pathogen propagation. Actual bacterial strain identification requires microbiological culture testing.
      </p>
    </div>
  );
};
""")

# 7. components/AlertBanner.jsx
with open("frontend/src/components/AlertBanner.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { ArrowRight, ShieldAlert } from 'lucide-react';
import { RiskBadge } from './RiskBadge';

export const AlertBanner = ({ alerts = [], onSelectAnimal }) => {
  if (!alerts || alerts.length === 0) return null;
  const topAlert = alerts[0];

  return (
    <div className="bg-gradient-to-r from-rose-950/80 via-slate-900/90 to-rose-950/60 border border-rose-500/40 rounded-2xl p-4 sm:p-5 backdrop-blur-md shadow-lg shadow-rose-950/30">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <div className="p-2.5 rounded-xl bg-rose-500/20 text-rose-400 border border-rose-500/30 mt-0.5">
            <ShieldAlert className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-bold uppercase tracking-wider text-rose-400">
                CRITICAL RISK NOTIFICATION
              </span>
              <RiskBadge category={topAlert.risk_category} score={topAlert.risk_score} size="sm" />
            </div>
            <h4 className="text-base font-bold text-white mt-0.5">
              Animal #{topAlert.animal_id} ({topAlert.breed}) &mdash; {topAlert.risk_score}% Mastitis Risk Score
            </h4>
            <div className="flex items-center gap-2 mt-1.5 flex-wrap">
              {topAlert.top_factors && topAlert.top_factors.map((f, idx) => (
                <span key={idx} className="text-[11px] px-2 py-0.5 rounded bg-slate-800/80 text-rose-300 border border-rose-500/20">
                  {f}
                </span>
              ))}
            </div>
          </div>
        </div>

        <button
          onClick={() => onSelectAnimal(topAlert.animal_id)}
          className="self-start sm:self-center px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold flex items-center gap-2 transition shadow-md shadow-rose-600/30 shrink-0"
        >
          <span>Inspect Animal #{topAlert.animal_id}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
""")

# 8. pages/Dashboard.jsx
with open("frontend/src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  Users, 
  ShieldCheck, 
  AlertCircle, 
  AlertTriangle, 
  Flame, 
  Activity, 
  ArrowRight,
  TrendingUp
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { EnvironmentalCard } from '../components/EnvironmentalCard';
import { AlertBanner } from '../components/AlertBanner';
import { RiskBadge } from '../components/RiskBadge';
import { 
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend 
} from 'recharts';

export const Dashboard = ({ data, onSelectAnimal, onNavigate }) => {
  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  const pieData = [
    { name: 'No Risk', value: data.no_risk_count, color: '#10b981' },
    { name: 'Low Risk', value: data.low_risk_count, color: '#0ea5e9' },
    { name: 'Moderate Risk', value: data.moderate_risk_count, color: '#f59e0b' },
    { name: 'High Risk', value: data.high_risk_count, color: '#f43f5e' },
  ];

  const herdComparison = [
    { metric: 'Body Temp (°C)', value: data.herd_averages.avg_body_temp, normal: 38.6 },
    { metric: 'Udder Temp (°C)', value: data.herd_averages.avg_udder_temp, normal: 33.8 },
    { metric: 'Conductivity (mS/cm)', value: data.herd_averages.avg_milk_conductivity, normal: 4.2 },
    { metric: 'Milk Yield (kg/d)', value: data.herd_averages.avg_milk_yield, normal: 15.0 },
    { metric: 'Hygiene Score', value: data.herd_averages.avg_hygiene_score, normal: 65.0 },
  ];

  return (
    <div className="space-y-6">
      
      {/* Top Notification Banner */}
      <AlertBanner alerts={data.recent_high_risk_alerts} onSelectAnimal={onSelectAnimal} />

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard 
          title="Total Herd" 
          value={data.total_animals.toLocaleString()} 
          subtext="Direct Excel Source" 
          icon={Users} 
          color="sky" 
        />
        <MetricCard 
          title="No Risk" 
          value={data.no_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.No_Risk}% healthy`} 
          icon={ShieldCheck} 
          color="emerald" 
        />
        <MetricCard 
          title="Low Risk" 
          value={data.low_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.Low}% monitored`} 
          icon={AlertCircle} 
          color="sky" 
        />
        <MetricCard 
          title="Moderate Risk" 
          value={data.moderate_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.Moderate}% subclinical`} 
          icon={AlertTriangle} 
          color="amber" 
        />
        <MetricCard 
          title="High Risk Alert" 
          value={data.high_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.High}% critical`} 
          icon={Flame} 
          color="rose" 
        />
      </div>

      {/* Main Charts & Environmental Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Risk Distribution Donut Chart */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Herd Risk Distribution</h3>
              <p className="text-xs text-slate-400">XGBoost Class Segmentation</p>
            </div>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} 
                  itemStyle={{ color: '#fff' }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-2 mt-2">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center gap-2 text-xs text-slate-300">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span>{item.name}: <strong>{item.value}</strong></span>
              </div>
            ))}
          </div>
        </div>

        {/* Herd Mean Biometric Telemetry */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-semibold text-white">Herd Sensor Means</h3>
              <p className="text-xs text-slate-400">Observed Mean vs Reference Baselines</p>
            </div>
            <TrendingUp className="w-4 h-4 text-sky-400" />
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={herdComparison} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="metric" stroke="#64748b" tick={{ fontSize: 10 }} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="value" name="Herd Average" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="normal" name="Normal Ref" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Barn Environmental Monitor */}
        <EnvironmentalCard envData={data.environmental_status} />

      </div>

      {/* Recent Predictions & Recent Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Recent High Risk Alerts */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Critical Decision-Support Alerts</h3>
              <p className="text-xs text-slate-400">Animals requiring immediate screening</p>
            </div>
            <button 
              onClick={() => onNavigate('alerts')}
              className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              <span>View All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {data.recent_high_risk_alerts.slice(0, 4).map((alert) => (
              <div 
                key={alert.animal_id}
                onClick={() => onSelectAnimal(alert.animal_id)}
                className="p-3.5 rounded-xl bg-slate-950/60 border border-rose-500/20 hover:border-rose-500/40 cursor-pointer transition flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 font-bold text-xs">
                    #{alert.animal_id}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-white">{alert.breed}</span>
                      <span className="text-[10px] text-slate-400">Farm: {alert.farm_id}</span>
                    </div>
                    <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                      {alert.top_factors.map((f, i) => (
                        <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-rose-300">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-sm font-bold font-mono text-rose-400">{alert.risk_score}%</span>
                  <p className="text-[10px] text-rose-400/80 uppercase font-semibold">HIGH RISK</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Dataset Predictions */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 backdrop-blur-md">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Recent Herd Telemetry</h3>
              <p className="text-xs text-slate-400">Live records from Excel data stream</p>
            </div>
            <button 
              onClick={() => onNavigate('animals')}
              className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              <span>Explore Herd</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="pb-2">Animal</th>
                  <th className="pb-2">Breed</th>
                  <th className="pb-2">Conductivity</th>
                  <th className="pb-2">Body Temp</th>
                  <th className="pb-2">Risk</th>
                  <th className="pb-2 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {data.recent_predictions.slice(0, 6).map((cow) => (
                  <tr key={cow.animal_id} className="hover:bg-slate-800/30 transition">
                    <td className="py-2.5 font-bold text-white font-mono">#{cow.animal_id}</td>
                    <td className="py-2.5 text-slate-300">{cow.breed}</td>
                    <td className="py-2.5 font-mono text-slate-300">{cow.milk_conductivity_mS_cm} mS/cm</td>
                    <td className="py-2.5 font-mono text-slate-300">{cow.body_temperature_c} °C</td>
                    <td className="py-2.5">
                      <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                    </td>
                    <td className="py-2.5 text-right">
                      <button
                        onClick={() => onSelectAnimal(cow.animal_id)}
                        className="px-2 py-1 rounded bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white transition text-[11px]"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </div>
  );
};
""")

print("Dashboard created.")
""")
