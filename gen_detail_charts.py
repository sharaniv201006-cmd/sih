# -*- coding: utf-8 -*-
with open("frontend/src/pages/AnimalDetail.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, 
  Activity, 
  Sparkles, 
  CheckCircle2, 
  TrendingUp, 
  Thermometer, 
  Droplets, 
  Milk,
  AlertTriangle
} from 'lucide-react';
import { fetchAnimalDetail, fetchSensorData } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine 
} from 'recharts';

export const AnimalDetail = ({ animalId, onBack, onSimulateWithCow }) => {
  const [detail, setDetail] = useState(null);
  const [sensorTrend, setSensorTrend] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeChartTab, setActiveChartTab] = useState('all');

  useEffect(() => {
    const loadAnimal = async () => {
      setLoading(true);
      try {
        const [detRes, senRes] = await Promise.all([
          fetchAnimalDetail(animalId),
          fetchSensorData(animalId),
        ]);
        setDetail(detRes);
        setSensorTrend(senRes.telemetry_trend || []);
      } catch (err) {
        console.error('Error fetching animal details:', err);
      } finally {
        setLoading(false);
      }
    };
    if (animalId) loadAnimal();
  }, [animalId]);

  if (loading || !detail) return <div className="flex items-center justify-center min-h-[400px]"><div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div></div>;

  const { animal, prediction } = detail;
  const isHighRisk = prediction.risk_category === 'High';

  return (
    <div className="space-y-6">
      
      {/* Navigation Top Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button 
          onClick={onBack} 
          className="flex items-center gap-2 text-xs font-bold text-slate-700 hover:text-slate-900 px-4 py-2.5 rounded-xl btn-3d-slate transition w-fit"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Herd Surveillance</span>
        </button>

        <button 
          onClick={() => onSimulateWithCow(animal)} 
          className="flex items-center gap-2 text-xs font-bold text-white px-4 py-2.5 rounded-xl btn-3d-emerald transition shadow-md"
        >
          <Sparkles className="w-4 h-4" />
          <span>Load into Live IoT Simulator</span>
        </button>
      </div>

      {/* Main Animal Profile Card with 3D Depth */}
      <div className="box-3d-static p-6 sm:p-8">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 rounded-2xl icon-3d-emerald text-emerald-800 flex flex-col items-center justify-center shadow-md shrink-0">
              <span className="text-[10px] font-bold uppercase">COW</span>
              <span className="text-xl font-black font-mono">#{animal.animal_id}</span>
            </div>

            <div>
              <div className="flex items-center gap-2.5 flex-wrap">
                <h2 className="text-2xl font-black text-slate-900">{animal.breed}</h2>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-bold border border-slate-200">
                  Farm: {animal.farm_id}
                </span>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-bold border border-slate-200">
                  Record Date: {animal.record_date}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-3 text-xs text-slate-500 font-medium">
                <div>Age: <strong className="text-slate-900">{animal.age_years} yrs</strong></div>
                <div>Lactation: <strong className="text-slate-900">#{animal.lactation_number}</strong></div>
                <div>Days in Milk: <strong className="text-slate-900">{animal.days_in_milk} d</strong></div>
                <div>Vaccinated: <strong className="text-slate-900">{animal.vaccinated ? 'Yes' : 'No'}</strong></div>
              </div>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 lg:w-80 flex flex-col items-center justify-center text-center shadow-inner">
            <span className="text-xs text-slate-500 uppercase font-bold tracking-wider">AI Mastitis Risk Score</span>
            <div className="my-1.5 flex items-baseline gap-1">
              <span className={`text-4xl font-black font-mono ${isHighRisk ? 'text-rose-600' : prediction.risk_category === 'Moderate' ? 'text-amber-600' : 'text-emerald-600'}`}>
                {prediction.risk_score}%
              </span>
            </div>
            <div className="mt-1">
              <RiskBadge category={prediction.risk_category} size="lg" />
            </div>
            <div className="grid grid-cols-2 gap-2 mt-3 w-full border-t border-slate-200 pt-2 text-[11px] text-slate-500 font-medium">
              <div>7-Day Risk: <strong className="text-slate-800">{prediction.forecast_7d_risk_pct}%</strong></div>
              <div>14-Day Risk: <strong className="text-slate-800">{prediction.forecast_14d_risk_pct}%</strong></div>
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Risk Factors and Telemetry Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Risk Factors */}
        <div className="lg:col-span-2 box-3d-static p-6">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-5 h-5 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">Primary Model Risk Factors (Feature Deviations)</h3>
          </div>
          <p className="text-xs text-slate-500 mb-4">
            Identified feature deviations relative to healthy physiological baselines contributing to this risk level.
          </p>

          {prediction.top_risk_factors.length === 0 ? (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2.5 font-medium shadow-xs">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
              <span>All biometric and milking telemetry values are within normal physiological baselines.</span>
            </div>
          ) : (
            <div className="space-y-2.5">
              {prediction.top_risk_factors.map((factor, idx) => (
                <div key={idx} className="p-3.5 rounded-2xl bg-rose-50/70 border border-rose-200 flex items-center justify-between shadow-2xs">
                  <div>
                    <span className="text-xs font-bold text-rose-900">{factor.factor}</span>
                    <p className="text-[11px] text-slate-600 font-mono mt-0.5">Observed: {factor.details}</p>
                  </div>
                  <span className="text-xs font-mono font-bold px-3 py-1 rounded-full bg-rose-100 text-rose-700 border border-rose-200">
                    Impact: +{factor.impact_score}
                  </span>
                </div>
              ))}
            </div>
          )}

          <div className="mt-6 border-t border-slate-100 pt-4">
            <h4 className="text-xs font-bold text-slate-800 mb-2 uppercase tracking-wider">Veterinary Decision-Support Suggestions:</h4>
            <ul className="space-y-2 text-xs text-slate-600">
              {prediction.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-xl border border-slate-200/80">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Current Milking & Telemetry Values */}
        <div className="box-3d-static p-6 space-y-3">
          <h3 className="text-sm font-bold text-slate-900 mb-3">Live Telemetry Readings</h3>
          
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Milk Conductivity</span>
            <span className={`font-mono font-bold text-sm ${animal.milk_conductivity_mS_cm > 4.5 ? 'text-rose-600' : 'text-slate-900'}`}>
              {animal.milk_conductivity_mS_cm} mS/cm
            </span>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Core Body Temp</span>
            <span className={`font-mono font-bold text-sm ${animal.body_temperature_c > 39.0 ? 'text-amber-600' : 'text-slate-900'}`}>
              {animal.body_temperature_c} °C
            </span>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Udder Surface Temp</span>
            <span className="font-mono font-bold text-sm text-slate-900">{animal.udder_surface_temperature_c} °C</span>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Daily Milk Yield</span>
            <span className="font-mono font-bold text-sm text-slate-900">{animal.milk_yield_kg_day} kg/day</span>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Barn Hygiene Score</span>
            <span className="font-mono font-bold text-sm text-slate-900">{animal.hygiene_score_0_100} / 100</span>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-semibold">Pathogen Exposure Proxy</span>
            <span className="font-mono font-bold text-xs text-emerald-700">{animal.dominant_environment_pathogen}</span>
          </div>
        </div>

      </div>

      {/* PROPERLY SCALED INDEPENDENT 7-DAY SENSOR TREND CHARTS */}
      <div className="box-3d-static p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-base font-black text-slate-900 tracking-tight">7-Day Sensor Telemetry Progression</h3>
            <p className="text-xs text-slate-500">Longitudinal monitoring with independent physiological scaling & alert thresholds</p>
          </div>

          {/* Chart Filter Buttons */}
          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setActiveChartTab('all')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${activeChartTab === 'all' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
            >
              All 3 Metrics
            </button>
            <button
              onClick={() => setActiveChartTab('cond')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${activeChartTab === 'cond' ? 'bg-rose-500 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
            >
              Conductivity
            </button>
            <button
              onClick={() => setActiveChartTab('temp')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${activeChartTab === 'temp' ? 'bg-amber-500 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
            >
              Body Temp
            </button>
            <button
              onClick={() => setActiveChartTab('yield')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${activeChartTab === 'yield' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
            >
              Milk Yield
            </button>
          </div>
        </div>

        {/* 3 Dedicated High-Contrast Scaled Charts */}
        <div className={`grid gap-6 ${activeChartTab === 'all' ? 'grid-cols-1 lg:grid-cols-3' : 'grid-cols-1'}`}>
          
          {/* Chart 1: Milk Conductivity */}
          {(activeChartTab === 'all' || activeChartTab === 'cond') && (
            <div className="bg-slate-50 border border-slate-200/90 rounded-2xl p-4 shadow-xs">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                  <span className="text-xs font-bold text-slate-800">Milk Conductivity (mS/cm)</span>
                </div>
                <span className="text-[10px] font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                  Threshold: 4.5 mS/cm
                </span>
              </div>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={sensorTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorCond" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 10 }} />
                    <YAxis domain={[3.0, 6.5]} stroke="#64748b" tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <ReferenceLine y={4.5} stroke="#f43f5e" strokeDasharray="4 4" label={{ value: 'Risk > 4.5', fill: '#f43f5e', fontSize: 10 }} />
                    <Area type="monotone" dataKey="milk_conductivity_mS_cm" name="Conductivity (mS/cm)" stroke="#f43f5e" strokeWidth={2.5} fillOpacity={1} fill="url(#colorCond)" dot={{ r: 3, fill: '#f43f5e' }} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Chart 2: Body Temperature */}
          {(activeChartTab === 'all' || activeChartTab === 'temp') && (
            <div className="bg-slate-50 border border-slate-200/90 rounded-2xl p-4 shadow-xs">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                  <span className="text-xs font-bold text-slate-800">Core Body Temp (°C)</span>
                </div>
                <span className="text-[10px] font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  Normal: 38.6 °C
                </span>
              </div>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={sensorTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 10 }} />
                    <YAxis domain={[37.5, 41.0]} stroke="#64748b" tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <ReferenceLine y={39.0} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'Fever > 39.0', fill: '#f59e0b', fontSize: 10 }} />
                    <Area type="monotone" dataKey="body_temperature_c" name="Body Temp (°C)" stroke="#f59e0b" strokeWidth={2.5} fillOpacity={1} fill="url(#colorTemp)" dot={{ r: 3, fill: '#f59e0b' }} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Chart 3: Daily Milk Yield */}
          {(activeChartTab === 'all' || activeChartTab === 'yield') && (
            <div className="bg-slate-50 border border-slate-200/90 rounded-2xl p-4 shadow-xs">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span className="text-xs font-bold text-slate-800">Daily Milk Yield (kg/day)</span>
                </div>
                <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Target: 15-20 kg
                </span>
              </div>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={sensorTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorYield" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 10 }} />
                    <YAxis domain={[0, 25]} stroke="#64748b" tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Area type="monotone" dataKey="milk_yield_kg_day" name="Yield (kg/day)" stroke="#10b981" strokeWidth={2.5} fillOpacity={1} fill="url(#colorYield)" dot={{ r: 3, fill: '#10b981' }} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

        </div>
      </div>

    </div>
  );
};
""")

print("AnimalDetail.jsx updated with properly scaled independent charts.")
