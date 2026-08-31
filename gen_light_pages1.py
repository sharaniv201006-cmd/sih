# -*- coding: utf-8 -*-
# 1. Update pages/Login.jsx
with open("frontend/src/pages/Login.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import { ShieldCheck, LogIn, User, Lock, AlertCircle, Sparkles } from 'lucide-react';
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-emerald-50/30 to-teal-50/20 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      
      {/* Decorative gradient blur */}
      <div className="absolute top-10 left-10 w-80 h-80 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-teal-400/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md space-y-6 z-10">
        
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-xl shadow-emerald-500/20 mb-2">
            <span className="text-2xl font-black text-white">BM</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">BovineGuard AI</h1>
          <p className="text-xs text-slate-500 max-w-xs mx-auto">
            AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-xl shadow-slate-200/50">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5">
                Username / Personnel ID
              </label>
              <div className="relative">
                <User className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. admin or vet01"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-emerald-600/20 disabled:opacity-50 mt-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
              ) : (
                <LogIn className="w-4 h-4" />
              )}
              <span>Access Surveillance Dashboard</span>
            </button>
          </form>

          {/* Quick Logins */}
          <div className="mt-6 pt-5 border-t border-slate-100">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block text-center mb-3">
              One-Click Presentation Logins
            </span>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleQuickDemo('vet')}
                className="p-2.5 rounded-xl bg-slate-50 hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 text-left transition flex items-center gap-2"
              >
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0" />
                <div>
                  <span className="text-xs font-bold text-slate-800 block">Dr. Sharma</span>
                  <span className="text-[10px] text-slate-500 block">Veterinarian</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo('manager')}
                className="p-2.5 rounded-xl bg-slate-50 hover:bg-sky-50 border border-slate-200 hover:border-sky-300 text-left transition flex items-center gap-2"
              >
                <div className="w-2.5 h-2.5 rounded-full bg-sky-500 shrink-0" />
                <div>
                  <span className="text-xs font-bold text-slate-800 block">S. Patel</span>
                  <span className="text-[10px] text-slate-500 block">Farm Manager</span>
                </div>
              </button>
            </div>
          </div>

        </div>

        <div className="flex items-center justify-center gap-1.5 text-center text-xs text-slate-500">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Offline & Cloud Compatible &bull; Direct Pandas Engine</span>
        </div>

      </div>
    </div>
  );
};
""")

# 2. Update pages/AnimalRegistration.jsx
with open("frontend/src/pages/AnimalRegistration.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import { 
  PlusCircle, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  Info,
  Check,
  X,
  RotateCcw
} from 'lucide-react';
import { registerAnimal } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const AnimalRegistration = ({ onRegistrationSuccess, onInspectAnimal }) => {
  // STRICTLY MINIMAL FORM STATE: ONLY the 6 requested fields
  const [animalId, setAnimalId] = useState('');
  const [breed, setBreed] = useState('Jersey_cross');
  const [age, setAge] = useState('');
  const [lactation, setLactation] = useState('');
  const [hadMastitisBefore, setHadMastitisBefore] = useState(false);
  const [abnormalBehavior, setAbnormalBehavior] = useState(false);

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [registeredResult, setRegisteredResult] = useState(null);

  const resetForm = () => {
    setAnimalId('');
    setBreed('Jersey_cross');
    setAge('');
    setLactation('');
    setHadMastitisBefore(false);
    setAbnormalBehavior(false);
    setErrorMessage('');
    setRegisteredResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    // Validation
    const parsedId = parseInt(animalId);
    if (!animalId || isNaN(parsedId) || parsedId <= 0) {
      setErrorMessage('Please enter a valid positive Animal ID (e.g. 12005).');
      return;
    }

    const parsedAge = parseFloat(age);
    if (!age || isNaN(parsedAge) || parsedAge <= 0 || parsedAge > 20) {
      setErrorMessage('Please enter a valid age in years (e.g. 3.5).');
      return;
    }

    const parsedLact = parseInt(lactation);
    if (!lactation || isNaN(parsedLact) || parsedLact <= 0 || parsedLact > 15) {
      setErrorMessage('Please enter a valid lactation number (e.g. 2).');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        animal_id: parsedId,
        breed: breed,
        age_years: parsedAge,
        lactation_number: parsedLact,
        previous_mastitis_history: hadMastitisBefore,
        abnormal_behavior: abnormalBehavior
      };

      const res = await registerAnimal(payload);
      if (res.success) {
        setRegisteredResult(res);
        if (onRegistrationSuccess) onRegistrationSuccess(res.animal);
      } else {
        setErrorMessage(res.message || 'Registration failed.');
      }
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || 'Error connecting to backend server.';
      setErrorMessage(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-600 mb-1 shadow-xs">
          <PlusCircle className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">Animal Registration</h2>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Enroll a new bovine to active AI surveillance. Milking, biometric, and environmental sensors will be paired automatically by the IoT network.
        </p>
      </div>

      {/* Success Notification View */}
      {registeredResult ? (
        <div className="bg-white border border-emerald-200 rounded-3xl p-6 sm:p-8 shadow-xl shadow-emerald-900/5 space-y-6 text-center">
          
          <div className="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center mx-auto shadow-md shadow-emerald-500/10">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h3 className="text-xl font-bold text-slate-900">
              Animal #{registeredResult.animal.animal_id} Registered Successfully!
            </h3>
            <p className="text-xs text-slate-500">
              Integrated into the dataset and evaluated through the XGBoost ML pipeline.
            </p>
          </div>

          {/* Initial AI Evaluation Summary */}
          {registeredResult.initial_prediction && (
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-left">
              <div>
                <span className="text-[11px] text-slate-500 uppercase font-bold">Initial AI Baseline Risk</span>
                <div className="flex items-center gap-2 mt-1">
                  <RiskBadge 
                    category={registeredResult.initial_prediction.risk_category} 
                    score={registeredResult.initial_prediction.risk_score} 
                    size="md" 
                  />
                  <span className="text-xs text-slate-600 font-medium">
                    Breed: {registeredResult.animal.breed}
                  </span>
                </div>
              </div>

              <div className="text-right sm:text-right text-xs text-slate-500">
                <span>7-Day Risk: <strong className="text-slate-800">{registeredResult.initial_prediction.forecast_7d_risk_pct}%</strong></span>
                <p className="text-[10px] text-slate-400">Continuous IoT Telemetry Ready</p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <button
              onClick={() => onInspectAnimal(registeredResult.animal.animal_id)}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition shadow-md shadow-emerald-600/20"
            >
              <span>Inspect Animal in Surveillance</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={resetForm}
              className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center gap-2 transition border border-slate-200"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Register Another Animal</span>
            </button>
          </div>

        </div>
      ) : (
        /* Minimal Registration Form */
        <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-xl shadow-slate-200/40">
          
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {errorMessage && (
              <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Input 1: Animal ID */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5">
                1. Animal ID <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                min="1"
                step="1"
                placeholder="Enter unique ear tag / collar ID (e.g. 12005)"
                value={animalId}
                onChange={(e) => setAnimalId(e.target.value)}
                className="w-full px-4 py-3 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition font-mono font-bold"
                required
              />
              <span className="text-[11px] text-slate-400 mt-1 block">
                System automatically verifies ID to prevent duplicates.
              </span>
            </div>

            {/* Input 2: Breed */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5">
                2. Breed <span className="text-rose-500">*</span>
              </label>
              <select
                value={breed}
                onChange={(e) => setBreed(e.target.value)}
                className="w-full px-4 py-3 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition font-medium"
              >
                <option value="Jersey_cross">Jersey Cross</option>
                <option value="HF_cross">Holstein Friesian (HF) Cross</option>
                <option value="Gir">Gir (Indigenous)</option>
                <option value="Sahiwal">Sahiwal (Indigenous)</option>
                <option value="Murrah">Murrah Buffalo</option>
              </select>
            </div>

            {/* Input 3 & 4: Age & Lactation Number */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  3. Age (Years) <span className="text-rose-500">*</span>
                </label>
                <input
                  type="number"
                  min="0.5"
                  max="20"
                  step="0.1"
                  placeholder="e.g. 3.5"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition font-mono font-bold"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  4. Lactation Number <span className="text-rose-500">*</span>
                </label>
                <input
                  type="number"
                  min="1"
                  max="15"
                  step="1"
                  placeholder="e.g. 2"
                  value={lactation}
                  onChange={(e) => setLactation(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50/70 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition font-mono font-bold"
                  required
                />
              </div>
            </div>

            {/* Question 5: Has the animal had mastitis before? */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2.5">
              <label className="block text-xs font-bold text-slate-700">
                5. Has the animal had mastitis before?
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setHadMastitisBefore(true)}
                  className={`py-2.5 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    hadMastitisBefore
                      ? 'bg-rose-100 text-rose-800 border-rose-300 shadow-sm'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <Check className="w-4 h-4" />
                  <span>Yes (Prior History)</span>
                </button>

                <button
                  type="button"
                  onClick={() => setHadMastitisBefore(false)}
                  className={`py-2.5 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    !hadMastitisBefore
                      ? 'bg-emerald-100 text-emerald-800 border-emerald-300 shadow-sm'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <X className="w-4 h-4" />
                  <span>No (First-time / Clean)</span>
                </button>
              </div>
            </div>

            {/* Question 6: Is the animal currently showing abnormal behavior? */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2.5">
              <label className="block text-xs font-bold text-slate-700">
                6. Is the animal currently showing abnormal behavior?
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setAbnormalBehavior(true)}
                  className={`py-2.5 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    abnormalBehavior
                      ? 'bg-amber-100 text-amber-800 border-amber-300 shadow-sm'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <Check className="w-4 h-4" />
                  <span>Yes (Restless / Low intake)</span>
                </button>

                <button
                  type="button"
                  onClick={() => setAbnormalBehavior(false)}
                  className={`py-2.5 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    !abnormalBehavior
                      ? 'bg-emerald-100 text-emerald-800 border-emerald-300 shadow-sm'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <X className="w-4 h-4" />
                  <span>No (Normal Activity)</span>
                </button>
              </div>
            </div>

            {/* Info Box */}
            <div className="flex items-start gap-2 p-3 rounded-xl bg-emerald-50/60 border border-emerald-100 text-[11px] text-emerald-800">
              <Info className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>
                IoT physical sensors (collar temperature, milking conductivity, barn sensors) will pair automatically to this ID for continuous telemetry.
              </span>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-emerald-600/25 disabled:opacity-50"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
              ) : (
                <PlusCircle className="w-5 h-5" />
              )}
              <span>Register Animal & Initialize AI Monitoring</span>
            </button>

          </form>

        </div>
      )}

    </div>
  );
};
""")

print("Login and Registration pages updated to attractive white theme.")
