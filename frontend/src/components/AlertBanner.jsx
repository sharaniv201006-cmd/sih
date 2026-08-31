import React from 'react';
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
