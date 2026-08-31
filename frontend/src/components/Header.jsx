import React from 'react';
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
