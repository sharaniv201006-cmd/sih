# 1. Update pages/AnimalDetail.jsx
with open("frontend/src/pages/AnimalDetail.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { ArrowLeft, Activity, Sparkles, CheckCircle2 } from 'lucide-react';
import { fetchAnimalDetail, fetchSensorData } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export const AnimalDetail = ({ animalId, onBack, onSimulateWithCow }) => {
  const [detail, setDetail] = useState(null);
  const [sensorTrend, setSensorTrend] = useState([]);
  const [loading, setLoading] = useState(true);

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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button onClick={onBack} className="flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-slate-900 px-3.5 py-2 rounded-xl bg-white border border-slate-200 shadow-2xs transition w-fit">
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Herd Surveillance</span>
        </button>

        <button onClick={() => onSimulateWithCow(animal)} className="flex items-center gap-2 text-xs font-bold text-emerald-700 hover:text-white px-4 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-600 border border-emerald-200 transition shadow-2xs">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Load into Live IoT Simulator</span>
        </button>
      </div>

      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200 flex flex-col items-center justify-center shadow-xs">
              <span className="text-[10px] text-emerald-600 font-bold uppercase">ANIMAL</span>
              <span className="text-xl font-black text-slate-900 font-mono">#{animal.animal_id}</span>
            </div>

            <div>
              <div className="flex items-center gap-2.5 flex-wrap">
                <h2 className="text-xl font-black text-slate-900">{animal.breed}</h2>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">Farm: {animal.farm_id}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">Date: {animal.record_date}</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-3 text-xs text-slate-500">
                <div>Age: <strong className="text-slate-800">{animal.age_years} yrs</strong></div>
                <div>Lactation: <strong className="text-slate-800">#{animal.lactation_number}</strong></div>
                <div>Days in Milk: <strong className="text-slate-800">{animal.days_in_milk} d</strong></div>
                <div>Vaccinated: <strong className="text-slate-800">{animal.vaccinated ? 'Yes' : 'No'}</strong></div>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 lg:w-72 flex flex-col items-center justify-center text-center">
            <span className="text-xs text-slate-500 uppercase font-bold tracking-wider">AI Mastitis Risk Score</span>
            <div className="my-1.5 flex items-baseline gap-1">
              <span className={`text-4xl font-black font-mono ${isHighRisk ? 'text-rose-600' : prediction.risk_category === 'Moderate' ? 'text-amber-600' : 'text-emerald-600'}`}>
                {prediction.risk_score}%
              </span>
            </div>
            <div className="mt-1">
              <RiskBadge category={prediction.risk_category} size="lg" />
            </div>
            <div className="grid grid-cols-2 gap-2 mt-3 w-full border-t border-slate-200 pt-2 text-[11px] text-slate-500">
              <div>7-Day Risk: <strong className="text-slate-800">{prediction.forecast_7d_risk_pct}%</strong></div>
              <div>14-Day Risk: <strong className="text-slate-800">{prediction.forecast_14d_risk_pct}%</strong></div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-4 h-4 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">Important Model Risk Factors (Feature Deviations)</h3>
          </div>
          <p className="text-xs text-slate-500 mb-4">
            Identified feature deviations relative to physiological baselines contributing to the prediction.
          </p>

          {prediction.top_risk_factors.length === 0 ? (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>All biometric and milking telemetry values are within normal physiological baselines.</span>
            </div>
          ) : (
            <div className="space-y-2.5">
              {prediction.top_risk_factors.map((factor, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-rose-50/50 border border-rose-100 flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-rose-800">{factor.factor}</span>
                    <p className="text-[11px] text-slate-500 font-mono mt-0.5">Observed: {factor.details}</p>
                  </div>
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-700 border border-rose-200">
                    Impact: +{factor.impact_score}
                  </span>
                </div>
              ))}
            </div>
          )}

          <div className="mt-5 border-t border-slate-100 pt-4">
            <h4 className="text-xs font-bold text-slate-800 mb-2">Veterinary Decision-Support Suggestions:</h4>
            <ul className="space-y-1.5 text-xs text-slate-600">
              {prediction.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 mb-3">Milking & Wearable Telemetry</h3>
          <div className="space-y-2.5">
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Milk Conductivity</span>
              <span className={`font-mono font-bold ${animal.milk_conductivity_mS_cm > 4.5 ? 'text-rose-600' : 'text-slate-800'}`}>
                {animal.milk_conductivity_mS_cm} mS/cm
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Core Body Temperature</span>
              <span className={`font-mono font-bold ${animal.body_temperature_c > 39.0 ? 'text-amber-600' : 'text-slate-800'}`}>
                {animal.body_temperature_c} °C
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Udder Surface Temperature</span>
              <span className="font-mono font-bold text-slate-800">{animal.udder_surface_temperature_c} °C</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Daily Milk Yield</span>
              <span className="font-mono font-bold text-slate-800">{animal.milk_yield_kg_day} kg/day</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Barn Hygiene Score</span>
              <span className="font-mono font-bold text-slate-800">{animal.hygiene_score_0_100} / 100</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Dominant Pathogen Proxy</span>
              <span className="font-mono text-emerald-700 font-bold">{animal.dominant_environment_pathogen}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">7-Day Sensor Telemetry Progression</h3>
            <p className="text-xs text-slate-500">Tracking Conductivity, Body Temp, and Milk Yield</p>
          </div>
        </div>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sensorTrend} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Line type="monotone" dataKey="milk_conductivity_mS_cm" name="Conductivity (mS/cm)" stroke="#f43f5e" strokeWidth={2.5} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="body_temperature_c" name="Body Temp (°C)" stroke="#f59e0b" strokeWidth={2.5} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="milk_yield_kg_day" name="Yield (kg/d)" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
""")

# 2. Update pages/LiveSensorMonitoring.jsx
with open("frontend/src/pages/LiveSensorMonitoring.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import { Sliders, Sparkles, Send, RotateCcw, Cpu } from 'lucide-react';
import { predictRisk } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const LiveSensorMonitoring = ({ initialCowData = null }) => {
  const defaultForm = {
    animal_id: initialCowData?.animal_id || 'COW_IOT_SIM',
    breed: initialCowData?.breed || 'Jersey_cross',
    age_years: initialCowData?.age_years || 4.5,
    lactation_number: initialCowData?.lactation_number || 3,
    days_in_milk: initialCowData?.days_in_milk || 75,
    previous_mastitis_history: initialCowData?.previous_mastitis_history || 0,
    vaccinated: initialCowData?.vaccinated ?? 1,
    chronic_disease_flag: initialCowData?.chronic_disease_flag || 0,
    ambient_temperature_c: initialCowData?.ambient_temperature_c || 28.5,
    relative_humidity_pct: initialCowData?.relative_humidity_pct || 72.0,
    hygiene_score_0_100: initialCowData?.hygiene_score_0_100 || 60.0,
    environment_total_mastitis_pathogen_load_log10: initialCowData?.environment_total_mastitis_pathogen_load_log10 || 4.6,
    S_aureus_load_log10_cfu_equiv: initialCowData?.S_aureus_load_log10_cfu_equiv || 4.1,
    S_uberis_load_log10_cfu_equiv: initialCowData?.S_uberis_load_log10_cfu_equiv || 4.2,
    E_coli_load_log10_cfu_equiv: initialCowData?.E_coli_load_log10_cfu_equiv || 3.9,
    K_pneumoniae_load_log10_cfu_equiv: initialCowData?.K_pneumoniae_load_log10_cfu_equiv || 3.7,
    S_agalactiae_load_log10_cfu_equiv: initialCowData?.S_agalactiae_load_log10_cfu_equiv || 3.4,
    dominant_environment_pathogen: initialCowData?.dominant_environment_pathogen || 'S_uberis',
    milk_yield_kg_day: initialCowData?.milk_yield_kg_day || 14.5,
    milk_conductivity_mS_cm: initialCowData?.milk_conductivity_mS_cm || 4.2,
    body_temperature_c: initialCowData?.body_temperature_c || 38.6,
    udder_surface_temperature_c: initialCowData?.udder_surface_temperature_c || 33.9,
  };

  const [formData, setFormData] = useState(defaultForm);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const setPreset = (presetType) => {
    if (presetType === 'healthy') {
      setFormData({
        ...formData,
        body_temperature_c: 38.5,
        udder_surface_temperature_c: 33.8,
        milk_conductivity_mS_cm: 3.9,
        milk_yield_kg_day: 16.5,
        hygiene_score_0_100: 75.0,
        ambient_temperature_c: 26.0,
        relative_humidity_pct: 65.0,
        environment_total_mastitis_pathogen_load_log10: 3.8,
        previous_mastitis_history: 0
      });
    } else if (presetType === 'early_warning') {
      setFormData({
        ...formData,
        body_temperature_c: 39.1,
        udder_surface_temperature_c: 34.6,
        milk_conductivity_mS_cm: 4.8,
        milk_yield_kg_day: 12.0,
        hygiene_score_0_100: 50.0,
        ambient_temperature_c: 31.0,
        relative_humidity_pct: 80.0,
        environment_total_mastitis_pathogen_load_log10: 4.9,
        previous_mastitis_history: 1
      });
    } else if (presetType === 'acute_high') {
      setFormData({
        ...formData,
        body_temperature_c: 39.8,
        udder_surface_temperature_c: 36.2,
        milk_conductivity_mS_cm: 5.8,
        milk_yield_kg_day: 8.0,
        hygiene_score_0_100: 35.0,
        ambient_temperature_c: 34.0,
        relative_humidity_pct: 88.0,
        environment_total_mastitis_pathogen_load_log10: 5.8,
        previous_mastitis_history: 1
      });
    }
  };

  const handleChange = (field, val) => {
    setFormData((prev) => ({ ...prev, [field]: val }));
  };

  const handleRunInference = async () => {
    setLoading(true);
    try {
      const res = await predictRisk(formData);
      setPrediction(res);
    } catch (err) {
      console.error('Inference error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-center justify-between flex-wrap gap-3 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500 text-white shadow-xs">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-amber-800">
              DEMO / SIMULATED SENSOR DATA
            </span>
            <p className="text-xs text-slate-600">
              Interactive IoT sensor stream simulator feeding directly into the trained XGBoost ML inference pipeline.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500 mr-1">Presets:</span>
          <button onClick={() => setPreset('healthy')} className="px-2.5 py-1 rounded-lg bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-xs font-bold border border-emerald-200 transition">
            Healthy Normal
          </button>
          <button onClick={() => setPreset('early_warning')} className="px-2.5 py-1 rounded-lg bg-amber-100 hover:bg-amber-200 text-amber-800 text-xs font-bold border border-amber-200 transition">
            Early Subclinical
          </button>
          <button onClick={() => setPreset('acute_high')} className="px-2.5 py-1 rounded-lg bg-rose-100 hover:bg-rose-200 text-rose-800 text-xs font-bold border border-rose-200 transition">
            Acute High Risk
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm space-y-5">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-sm font-bold text-slate-900">IoT Sensor & Animal Controls</h3>
              <p className="text-xs text-slate-500">Adjust parameters to simulate live hardware stream</p>
            </div>
            <button onClick={() => setFormData(defaultForm)} className="text-xs font-bold text-slate-500 hover:text-slate-800 flex items-center gap-1">
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2">1. Milking Sensors</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <div className="flex justify-between text-xs text-slate-700 font-semibold mb-1">
                    <span>Milk Conductivity</span>
                    <strong className="font-mono text-slate-900">{formData.milk_conductivity_mS_cm} mS/cm</strong>
                  </div>
                  <input
                    type="range"
                    min="3.0"
                    max="7.0"
                    step="0.1"
                    value={formData.milk_conductivity_mS_cm}
                    onChange={(e) => handleChange('milk_conductivity_mS_cm', parseFloat(e.target.value))}
                    className="w-full accent-emerald-600"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                    <span>3.0 (Healthy)</span>
                    <span>5.0+ (Ion Leakage)</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs text-slate-700 font-semibold mb-1">
                    <span>Daily Milk Yield</span>
                    <strong className="font-mono text-slate-900">{formData.milk_yield_kg_day} kg/day</strong>
                  </div>
                  <input
                    type="range"
                    min="4.0"
                    max="28.0"
                    step="0.5"
                    value={formData.milk_yield_kg_day}
                    onChange={(e) => handleChange('milk_yield_kg_day', parseFloat(e.target.value))}
                    className="w-full accent-emerald-600"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                    <span>4.0 (Drop)</span>
                    <span>28.0 (Peak)</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-xs font-bold text-sky-700 uppercase tracking-wider mb-2">2. Wearable Biometric Collar / Tag Sensors</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <div className="flex justify-between text-xs text-slate-700 font-semibold mb-1">
                    <span>Body Temperature</span>
                    <strong className="font-mono text-slate-900">{formData.body_temperature_c} °C</strong>
                  </div>
                  <input
                    type="range"
                    min="37.5"
                    max="41.0"
                    step="0.1"
                    value={formData.body_temperature_c}
                    onChange={(e) => handleChange('body_temperature_c', parseFloat(e.target.value))}
                    className="w-full accent-sky-600"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                    <span>37.5°C</span>
                    <span>38.6°C (Normal)</span>
                    <span>40.5°C (Fever)</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs text-slate-700 font-semibold mb-1">
                    <span>Udder Surface Temperature</span>
                    <strong className="font-mono text-slate-900">{formData.udder_surface_temperature_c} °C</strong>
                  </div>
                  <input
                    type="range"
                    min="32.0"
                    max="37.5"
                    step="0.1"
                    value={formData.udder_surface_temperature_c}
                    onChange={(e) => handleChange('udder_surface_temperature_c', parseFloat(e.target.value))}
                    className="w-full accent-sky-600"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 font-medium">
                    <span>33.8°C (Normal)</span>
                    <span>36.0°C+ (Inflamed)</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-xs font-bold text-purple-700 uppercase tracking-wider mb-2">3. Barn Environmental & Pathogen Proxies</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="text-[11px] font-bold text-slate-600 block mb-1">Ambient Temp (°C)</label>
                  <input
                    type="number"
                    value={formData.ambient_temperature_c}
                    onChange={(e) => handleChange('ambient_temperature_c', parseFloat(e.target.value))}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-bold"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-slate-600 block mb-1">Humidity (%)</label>
                  <input
                    type="number"
                    value={formData.relative_humidity_pct}
                    onChange={(e) => handleChange('relative_humidity_pct', parseFloat(e.target.value))}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-bold"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-slate-600 block mb-1">Hygiene Score (0-100)</label>
                  <input
                    type="number"
                    value={formData.hygiene_score_0_100}
                    onChange={(e) => handleChange('hygiene_score_0_100', parseFloat(e.target.value))}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-bold"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
              <div>
                <label className="text-[11px] font-bold text-slate-600 block mb-1">Breed</label>
                <select
                  value={formData.breed}
                  onChange={(e) => handleChange('breed', e.target.value)}
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-medium"
                >
                  <option value="Jersey_cross">Jersey Cross</option>
                  <option value="HF_cross">HF Cross</option>
                  <option value="Gir">Gir</option>
                  <option value="Sahiwal">Sahiwal</option>
                  <option value="Murrah">Murrah</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-bold text-slate-600 block mb-1">Lactation #</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.lactation_number}
                  onChange={(e) => handleChange('lactation_number', parseInt(e.target.value))}
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-bold"
                />
              </div>

              <div>
                <label className="text-[11px] font-bold text-slate-600 block mb-1">Days in Milk</label>
                <input
                  type="number"
                  min="1"
                  max="350"
                  value={formData.days_in_milk}
                  onChange={(e) => handleChange('days_in_milk', parseInt(e.target.value))}
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-bold"
                />
              </div>

              <div>
                <label className="text-[11px] font-bold text-slate-600 block mb-1">Mastitis History</label>
                <select
                  value={formData.previous_mastitis_history}
                  onChange={(e) => handleChange('previous_mastitis_history', parseInt(e.target.value))}
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 font-medium"
                >
                  <option value={0}>No History (0)</option>
                  <option value={1}>Prior Case (1)</option>
                </select>
              </div>
            </div>
          </div>

          <button
            onClick={handleRunInference}
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-emerald-600/20 disabled:opacity-50"
          >
            {loading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span>Execute XGBoost Inference Engine (POST /api/predict)</span>
          </button>
        </div>

        <div className="lg:col-span-5 bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="border-b border-slate-100 pb-3 mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Live Prediction Diagnostics</h3>
                <p className="text-xs text-slate-500">FastAPI Model Evaluation Response</p>
              </div>
              {prediction && (
                <RiskBadge category={prediction.risk_category} score={prediction.risk_score} size="md" />
              )}
            </div>

            {!prediction ? (
              <div className="py-16 text-center text-slate-400 space-y-3">
                <Sliders className="w-10 h-10 mx-auto text-slate-300" />
                <p className="text-xs max-w-xs mx-auto text-slate-500">
                  Adjust simulated sensor parameters on the left and click "Execute XGBoost Inference Engine" to generate real-time risk predictions.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[11px] font-bold text-slate-500 uppercase">Calibrated Mastitis Risk Score</span>
                  <div className="text-4xl font-black font-mono my-1 text-slate-900">
                    {prediction.risk_score}%
                  </div>
                  <p className="text-xs text-slate-600">
                    Category: <strong className="text-emerald-700">{prediction.risk_category}</strong>
                  </p>
                </div>

                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-slate-700">Model Probability Breakdown:</span>
                  <div className="grid grid-cols-4 gap-1.5 text-center text-xs">
                    {Object.entries(prediction.class_probabilities).map(([cat, prob]) => (
                      <div key={cat} className="bg-slate-50 p-2 rounded-xl border border-slate-200">
                        <span className="text-[10px] text-slate-500 font-medium block">{cat.replace(/_/g, ' ')}</span>
                        <strong className="font-mono text-slate-900 text-xs">{prob}%</strong>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <span className="text-xs font-bold text-slate-700 block mb-2">
                    Primary Model Risk Factors:
                  </span>
                  {prediction.top_risk_factors.length === 0 ? (
                    <p className="text-xs text-emerald-800 bg-emerald-50 p-2.5 rounded-xl border border-emerald-200 font-medium">
                      No significant physiological anomalies detected.
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {prediction.top_risk_factors.map((f, i) => (
                        <div key={i} className="p-2.5 rounded-xl bg-rose-50/60 border border-rose-200 flex justify-between items-center text-xs">
                          <span className="text-rose-800 font-semibold">{f.factor}</span>
                          <span className="font-mono font-bold text-rose-700">+{f.impact_score}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="border-t border-slate-100 pt-3">
                  <span className="text-xs font-bold text-slate-700 block mb-1">Decision Support Suggestions:</span>
                  <ul className="text-[11px] text-slate-600 space-y-1">
                    {prediction.recommendations.slice(0, 3).map((r, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-emerald-600 font-bold">•</span>
                        <span>{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-[10px] text-slate-400">
            Powered by Scikit-learn Pipeline + XGBoost Multi-Class Softmax Classifier.
          </div>
        </div>
      </div>
    </div>
  );
};
""")

print("AnimalDetail.jsx & LiveSensorMonitoring.jsx updated.")
