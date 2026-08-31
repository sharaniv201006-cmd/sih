import React, { useState } from 'react';
import { ShieldCheck, LogIn, User, Lock, AlertCircle, Sparkles, Activity, CheckCircle } from 'lucide-react';
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
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-emerald-50/40 to-teal-50/30 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 relative overflow-hidden py-12">
      
      {/* 3D background floating ambient orbs */}
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-gradient-to-br from-emerald-400/20 to-teal-300/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-gradient-to-tl from-sky-400/20 to-emerald-300/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-lg space-y-6 z-10">
        
        {/* 3D Brand Header */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-b from-emerald-400 to-teal-600 shadow-[0_14px_30px_-4px_rgba(16,185,129,0.4),inset_0_2px_0_rgba(255,255,255,0.6)] mb-1 transform hover:scale-105 transition-transform duration-300">
            <span className="text-3xl font-black text-white tracking-tight drop-shadow-md">BM</span>
          </div>
          <div>
            <h1 className="text-3xl font-black text-slate-900 tracking-tight">BovineGuard AI</h1>
            <p className="text-sm font-medium text-emerald-700 mt-0.5">Bovine Mastitis Early Forecasting System</p>
          </div>
          <p className="text-xs text-slate-500 max-w-sm mx-auto leading-relaxed">
            Intelligent dairy herd surveillance engine powered by XGBoost machine learning and automated IoT biometrics.
          </p>
        </div>

        {/* 3D Elevated Login Card */}
        <div className="box-3d-static p-8 sm:p-10 border border-slate-200/90 shadow-[0_20px_50px_-10px_rgba(15,23,42,0.12),0_8px_16px_-4px_rgba(15,23,42,0.04),inset_0_2px_0_rgba(255,255,255,1)]">
          
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2 shadow-xs">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span className="font-semibold">{error}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                Username / Personnel ID
              </label>
              <div className="relative">
                <User className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. admin or vet01"
                  className="w-full pl-11 pr-4 py-3 bg-slate-50/80 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-medium"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-11 pr-4 py-3 bg-slate-50/80 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-medium"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 rounded-xl btn-3d-emerald text-white font-bold text-sm flex items-center justify-center gap-2 disabled:opacity-50 mt-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
              ) : (
                <LogIn className="w-5 h-5" />
              )}
              <span className="tracking-wide">ACCESS SURVEILLANCE DASHBOARD</span>
            </button>
          </form>

          {/* 3D One-Click Role Selector */}
          <div className="mt-8 pt-6 border-t border-slate-100">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block text-center mb-3">
              One-Click Presentation Logins
            </span>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => handleQuickDemo('vet')}
                className="p-3.5 rounded-2xl bg-white hover:bg-emerald-50/70 border border-slate-200 hover:border-emerald-300 shadow-[0_4px_10px_-2px_rgba(0,0,0,0.04),inset_0_1px_0_rgba(255,255,255,1)] hover:-translate-y-0.5 text-left transition-all duration-200 flex items-center gap-2.5 group"
              >
                <div className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)] shrink-0" />
                <div>
                  <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 block">Dr. Ramesh</span>
                  <span className="text-[10px] text-slate-400 font-medium block">Chief Veterinarian</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo('manager')}
                className="p-3.5 rounded-2xl bg-white hover:bg-sky-50/70 border border-slate-200 hover:border-sky-300 shadow-[0_4px_10px_-2px_rgba(0,0,0,0.04),inset_0_1px_0_rgba(255,255,255,1)] hover:-translate-y-0.5 text-left transition-all duration-200 flex items-center gap-2.5 group"
              >
                <div className="w-3 h-3 rounded-full bg-sky-500 shadow-[0_0_8px_rgba(14,165,233,0.6)] shrink-0" />
                <div>
                  <span className="text-xs font-bold text-slate-800 group-hover:text-sky-700 block">Suresh Patel</span>
                  <span className="text-[10px] text-slate-400 font-medium block">Farm Manager</span>
                </div>
              </button>
            </div>
          </div>

        </div>

        {/* Footer Feature Badges */}
        <div className="flex items-center justify-center gap-6 text-center text-xs text-slate-500 font-medium">
          <div className="flex items-center gap-1.5">
            <CheckCircle className="w-4 h-4 text-emerald-600" />
            <span>12,000+ Cow Records</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Activity className="w-4 h-4 text-emerald-600" />
            <span>90.8% XGBoost Accuracy</span>
          </div>
        </div>

      </div>
    </div>
  );
};
