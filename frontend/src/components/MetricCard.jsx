import React from 'react';

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
