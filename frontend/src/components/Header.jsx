import React from 'react';
import { PlusCircle, Search } from 'lucide-react';

export const Header = ({ activeTab, setActiveTab }) => {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'dashboard': return { title: 'Executive Herd Dashboard', sub: 'Real-time herd risk segmentation & analytics' };
      case 'register-animal': return { title: 'Animal Registration', sub: 'Enroll new bovine into active AI surveillance' };
      case 'animals': return { title: 'Herd Surveillance Master Inventory', sub: 'Surveillance across 500 Indian cattle records' };
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
