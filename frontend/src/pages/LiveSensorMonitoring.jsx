import React, { useState } from 'react';
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
