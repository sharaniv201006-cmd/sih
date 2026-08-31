import React from 'react';
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
