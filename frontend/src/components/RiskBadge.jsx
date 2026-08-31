import React from 'react';
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
