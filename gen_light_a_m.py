# 1. Update pages/Alerts.jsx
with open("frontend/src/pages/Alerts.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Sliders, ArrowRight, CheckCircle2 } from 'lucide-react';
import { fetchAnimals } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const Alerts = ({ onSelectAnimal }) => {
  const [alertThreshold, setAlertThreshold] = useState(60);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const res = await fetchAnimals({
        page: 1,
        page_size: 50,
        sort_by: 'synthetic_risk_score_pct',
        sort_order: 'desc'
      });
      const filtered = res.animals.filter(
        (a) => (a.synthetic_risk_score_pct || 0) >= alertThreshold
      );
      setAlerts(filtered);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [alertThreshold]);

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200/90 p-5 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">Configurable Alert Center</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-700 border border-rose-200">
              {alerts.length} Active Alerts
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Real-time threshold surveillance and veterinary screening recommendations
          </p>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 px-4 py-2.5 rounded-xl border border-slate-200">
          <Sliders className="w-4 h-4 text-emerald-600" />
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-500 uppercase font-bold">High-Risk Alert Threshold</span>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min="30"
                max="85"
                step="5"
                value={alertThreshold}
                onChange={(e) => setAlertThreshold(parseInt(e.target.value))}
                className="w-32 accent-emerald-600"
              />
              <span className="text-xs font-mono font-bold text-slate-900">{alertThreshold}%</span>
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-500">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
          <p>Scanning herd against {alertThreshold}% threshold...</p>
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500 shadow-sm">
          <CheckCircle2 className="w-12 h-12 mx-auto text-emerald-600 mb-3" />
          <h3 className="text-base font-bold text-slate-900">No Animals Above Current Threshold</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            All animals in the current herd dataset have risk scores below {alertThreshold}%.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {alerts.map((cow) => (
            <div
              key={cow.animal_id}
              className="bg-white border border-rose-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-rose-300 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-700 border border-rose-200 flex items-center justify-center font-mono font-bold text-sm">
                      #{cow.animal_id}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{cow.breed}</h4>
                      <p className="text-[11px] text-slate-500">Farm: {cow.farm_id} &bull; Lactation #{cow.lactation_number}</p>
                    </div>
                  </div>
                  <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                </div>

                <div className="grid grid-cols-2 gap-2 my-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                  <div>
                    <span className="text-slate-500 text-[10px] font-medium block">Conductivity</span>
                    <strong className="font-mono text-rose-600 font-bold">{cow.milk_conductivity_mS_cm} mS/cm</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] font-medium block">Body Temp</span>
                    <strong className="font-mono text-amber-600 font-bold">{cow.body_temperature_c} °C</strong>
                  </div>
                </div>

                <div className="text-[11px] text-slate-600 leading-relaxed">
                  <strong className="text-slate-800">Decision-Support Suggestion: </strong>
                  Perform California Mastitis Test (CMT) at next milking. Quarantine milk until subclinical clearance.
                </div>
              </div>

              <button
                onClick={() => onSelectAnimal(cow.animal_id)}
                className="mt-4 w-full py-2.5 rounded-xl bg-slate-100 hover:bg-emerald-600 text-slate-700 hover:text-white text-xs font-bold flex items-center justify-center gap-2 transition"
              >
                <span>Inspect Full Biometric Profile</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
""")

# 2. Update pages/ModelPerformance.jsx
with open("frontend/src/pages/ModelPerformance.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Award, CheckCircle, BarChart2, Layers } from 'lucide-react';
import { fetchModelPerformance } from '../services/api';
import { MetricCard } from '../components/MetricCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const ModelPerformance = () => {
  const [modelData, setModelData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const res = await fetchModelPerformance();
        setModelData(res);
      } catch (err) {
        console.error('Error fetching model performance:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading || !modelData) return <div className="flex items-center justify-center min-h-[400px]"><div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div></div>;

  const { metrics, feature_importance } = modelData;
  const topFeatures = (feature_importance || []).slice(0, 10);
  const classes = metrics.classes || ['No_Risk', 'Low', 'Moderate', 'High'];
  const cm = metrics.confusion_matrix || [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]];

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200/90 p-5 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">{metrics.model_name || 'XGBoost Multi-Class Model'}</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
              Evaluated on 2,400 Test Samples
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Algorithm: {metrics.algorithm} &bull; Pipeline: Standard Scaler + One-Hot Encoding + Multi:Softprob
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Accuracy" value={`${((metrics.accuracy || 0) * 100).toFixed(1)}%`} subtext="Stratified 80/20 split" icon={Award} color="emerald" />
        <MetricCard title="Weighted Precision" value={`${((metrics.precision || 0) * 100).toFixed(1)}%`} subtext="Multi-class precision" icon={CheckCircle} color="sky" />
        <MetricCard title="Weighted Recall" value={`${((metrics.recall || 0) * 100).toFixed(1)}%`} subtext="True positive detection" icon={BarChart2} color="purple" />
        <MetricCard title="F1-Score" value={`${((metrics.f1_score || 0) * 100).toFixed(1)}%`} subtext="Harmonic mean" icon={Layers} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">XGBoost Feature Importance Ranking</h3>
              <p className="text-xs text-slate-500">Relative gain percentage per model feature</p>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topFeatures} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis dataKey="feature" type="category" stroke="#64748b" tick={{ fontSize: 10 }} width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} formatter={(val) => [`${val}%`, 'Importance']} />
                <Bar dataKey="importance" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Confusion Matrix (Test Evaluation)</h3>
            <p className="text-xs text-slate-500 mb-4">Predicted vs Actual category assignments</p>
            <div className="overflow-x-auto">
              <table className="w-full text-center text-xs">
                <thead>
                  <tr className="text-slate-500 border-b border-slate-200">
                    <th className="py-2 text-left font-bold">Actual \\ Pred</th>
                    {classes.map((c) => (
                      <th key={c} className="py-2 px-2 text-slate-800 font-bold">{c.replace(/_/g, ' ')}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {cm.map((row, i) => (
                    <tr key={i}>
                      <td className="py-3 px-2 text-left font-bold text-slate-700">{classes[i]?.replace(/_/g, ' ')}</td>
                      {row.map((val, j) => (
                        <td key={j} className={`py-3 px-2 font-mono font-bold ${i === j ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg' : 'text-slate-400'}`}>
                          {val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <p className="mt-4 text-[11px] text-slate-500 border-t border-slate-100 pt-3">
            <strong>Training Details: </strong>
            150 estimators, max depth = 6, learning rate = 0.08, stratified 80/20 train-test split over 12,000+ dataset records.
          </p>
        </div>
      </div>
    </div>
  );
};
""")

# 3. Update App.jsx
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
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col selection:bg-emerald-500 selection:text-white">
      
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

      <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis</span>
          <span>Logged in as <strong className="text-slate-700">{user.name}</strong> ({user.role})</span>
        </div>
      </footer>

    </div>
  );
}

export default App;
""")

print("Alerts, ModelPerformance, and App.jsx updated.")
