# -*- coding: utf-8 -*-
with open("frontend/src/pages/Alerts.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Thermometer, 
  AlertTriangle, 
  ArrowRight, 
  CheckCircle2, 
  Flame,
  ShieldCheck,
  AlertCircle,
  Activity,
  HeartPulse
} from 'lucide-react';
import { fetchAnimals } from '../services/api';

export const Alerts = ({ onSelectAnimal }) => {
  const [riskFilter, setRiskFilter] = useState('All'); // 'All', 'High', 'Moderate'
  const [search, setSearch] = useState('');
  const [animals, setAnimals] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      // Fetch high and moderate risk animals
      const res = await fetchAnimals({
        page: 1,
        page_size: 40,
        risk: riskFilter === 'All' ? undefined : riskFilter,
        search: search.trim() || undefined,
        sort_by: 'synthetic_risk_score_pct',
        sort_order: 'desc'
      });
      
      // If 'All', show High and Moderate risk animals by default
      let list = res.animals || [];
      if (riskFilter === 'All' && !search.trim()) {
        list = list.filter(a => a.mastitis_risk_category === 'High' || a.mastitis_risk_category === 'Moderate');
      }
      setAnimals(list);
    } catch (err) {
      console.error('Error fetching decision alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [riskFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadAlerts();
  };

  // Helper for clean Risk details
  const getRiskDetails = (category) => {
    switch (category) {
      case 'High':
        return {
          label: 'HIGH RISK',
          pillBg: 'bg-rose-100 text-rose-700 border-rose-200',
          indicatorColor: 'bg-rose-600',
          cardBorder: 'border-rose-200/90 hover:border-rose-400',
          message: 'Veterinary inspection recommended.',
          attentionTitle: 'Attention Required',
          iconColor: 'text-rose-600'
        };
      case 'Moderate':
        return {
          label: 'MODERATE RISK',
          pillBg: 'bg-amber-100 text-amber-800 border-amber-200',
          indicatorColor: 'bg-amber-500',
          cardBorder: 'border-amber-200/90 hover:border-amber-400',
          message: 'Monitor the animal closely.',
          attentionTitle: 'Monitoring Recommended',
          iconColor: 'text-amber-600'
        };
      case 'Low':
        return {
          label: 'LOW RISK',
          pillBg: 'bg-sky-100 text-sky-800 border-sky-200',
          indicatorColor: 'bg-sky-500',
          cardBorder: 'border-slate-200 hover:border-sky-300',
          message: 'Continue regular monitoring.',
          attentionTitle: 'Routine Surveillance',
          iconColor: 'text-sky-600'
        };
      default:
        return {
          label: 'NO RISK',
          pillBg: 'bg-emerald-100 text-emerald-800 border-emerald-200',
          indicatorColor: 'bg-emerald-600',
          cardBorder: 'border-slate-200 hover:border-emerald-300',
          message: 'No abnormality detected.',
          attentionTitle: 'Normal Condition',
          iconColor: 'text-emerald-600'
        };
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fadeIn">
      
      {/* PAGE HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-1">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Veterinary Surveillance
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Decision Alerts
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Animals requiring attention
          </p>
        </div>

        {/* Search Box */}
        <form onSubmit={handleSearchSubmit} className="relative self-start sm:self-auto">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search Animal ID (e.g. #3991)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-xs w-64 sm:w-72 font-medium"
          />
        </form>
      </div>

      {/* FILTER BUTTONS: [All] [🔴 High Risk] [🟠 Moderate Risk] */}
      <div className="box-3d-static p-3 sm:p-4 flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setRiskFilter('All')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition ${
              riskFilter === 'All'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200'
            }`}
          >
            All Alerts
          </button>

          <button
            onClick={() => setRiskFilter('High')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
              riskFilter === 'High'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'bg-slate-50 hover:bg-rose-50 hover:text-rose-700 text-slate-600 border border-slate-200'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-rose-500 shrink-0" />
            <span>High Risk</span>
          </button>

          <button
            onClick={() => setRiskFilter('Moderate')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
              riskFilter === 'Moderate'
                ? 'bg-amber-500 text-white shadow-sm'
                : 'bg-slate-50 hover:bg-amber-50 hover:text-amber-700 text-slate-600 border border-slate-200'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0" />
            <span>Moderate Risk</span>
          </button>
        </div>

        <span className="text-xs font-bold text-slate-500 font-mono">
          Showing {animals.length} alerts
        </span>
      </div>

      {/* 3-COLUMN RESPONSIVE ANIMAL ALERT CARDS GRID */}
      {loading ? (
        <div className="py-20 text-center text-slate-500">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
          <p className="font-medium text-xs">Scanning herd telemetry alerts...</p>
        </div>
      ) : animals.length === 0 ? (
        <div className="box-3d-static p-12 text-center text-slate-500">
          <CheckCircle2 className="w-12 h-12 mx-auto text-emerald-600 mb-3" />
          <h3 className="text-base font-bold text-slate-900">No Alerts Found</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            All animals matching the selected filter are in normal condition.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {animals.map((cow) => {
            const riskInfo = getRiskDetails(cow.mastitis_risk_category);
            const bTemp = parseFloat(cow.body_temperature_c || 38.6);
            const uTemp = parseFloat(cow.udder_surface_temperature_c || 33.9);
            const isFever = bTemp > 38.9;
            const isWarmUdder = uTemp > 34.5;

            return (
              <div
                key={cow.animal_id}
                className={`box-3d p-5 sm:p-6 border ${riskInfo.cardBorder} flex flex-col justify-between transition-all duration-200 group`}
              >
                <div className="space-y-4">
                  
                  {/* Card Header: Animal ID & Breed & Risk Pill */}
                  <div className="flex items-start justify-between gap-2 border-b border-slate-100 pb-3">
                    <div className="flex items-start gap-2.5">
                      <span className="text-2xl mt-0.5 shrink-0" role="img" aria-label="cow">🐄</span>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-base font-black font-mono text-slate-900">
                            #{cow.animal_id}
                          </span>
                          <span className="text-xs font-bold text-slate-700">
                            {cow.breed.replace('_', ' ')}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400 font-medium mt-0.5">
                          Farm {cow.farm_id} &bull; Lactation #{cow.lactation_number}
                        </p>
                      </div>
                    </div>

                    {/* Simple Risk Label (No repeated large % percentages) */}
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider border shadow-2xs shrink-0 ${riskInfo.pillBg}`}>
                      {riskInfo.label}
                    </span>
                  </div>

                  {/* Sensor Readings (Only 2 Key Measurements) */}
                  <div className="space-y-2.5 pt-1">
                    
                    {/* 1. Body Temperature */}
                    <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
                        <Thermometer className="w-4 h-4 text-amber-500" />
                        <span>Body Temperature</span>
                      </div>
                      <span className={`text-xs font-black font-mono ${isFever ? 'text-rose-600' : 'text-slate-900'}`}>
                        {bTemp.toFixed(2)} °C
                      </span>
                    </div>

                    {/* 2. Udder Temperature */}
                    <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
                        <Thermometer className="w-4 h-4 text-rose-500" />
                        <span>Udder Temperature</span>
                      </div>
                      <span className={`text-xs font-black font-mono ${isWarmUdder ? 'text-rose-600' : 'text-slate-900'}`}>
                        {uTemp.toFixed(2)} °C
                      </span>
                    </div>

                  </div>

                  {/* Attention / Recommended Message Block */}
                  <div className="p-3 rounded-xl bg-slate-50/70 border border-slate-200/80 space-y-1">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
                      <AlertTriangle className={`w-3.5 h-3.5 ${riskInfo.iconColor}`} />
                      <span>{riskInfo.attentionTitle}</span>
                    </div>
                    <p className="text-[11px] text-slate-500 font-medium leading-relaxed">
                      {riskInfo.message}
                    </p>
                  </div>

                </div>

                {/* Card Action Button */}
                <button
                  onClick={() => onSelectAnimal(cow.animal_id)}
                  className="mt-5 w-full py-2.5 rounded-xl btn-3d-slate hover:bg-emerald-600 hover:text-white hover:border-emerald-600 text-slate-700 text-xs font-bold flex items-center justify-center gap-2 transition shadow-xs group-hover:border-emerald-400"
                >
                  <span>View Animal</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>

              </div>
            );
          })}
        </div>
      )}

    </div>
  );
};
""")

print("Updated Alerts.jsx with clean 3-column veterinary cards.")
