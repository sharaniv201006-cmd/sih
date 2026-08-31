import React, { useState, useEffect } from 'react';
import { RefreshCw, Eye } from 'lucide-react';
import { fetchAnimals } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const PredictionsHistory = ({ onSelectAnimal }) => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState('All');

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetchAnimals({
        page: 1,
        page_size: 40,
        risk: riskFilter !== 'All' ? riskFilter : undefined,
        sort_by: 'synthetic_risk_score_pct',
        sort_order: 'desc'
      });
      setRecords(res.animals);
    } catch (err) {
      console.error('Error fetching prediction logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [riskFilter]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/70 border border-slate-800 p-5 rounded-2xl backdrop-blur-md">
        <div>
          <h2 className="text-lg font-bold text-white">Model Predictions & Forecast Logs</h2>
          <p className="text-xs text-slate-400">
            Chronological and calibrated risk forecasts derived from the trained XGBoost model
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="px-3 py-1.5 bg-slate-950/80 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
          >
            <option value="All">All Categories</option>
            <option value="High">High Risk Only</option>
            <option value="Moderate">Moderate Risk</option>
            <option value="Low">Low Risk</option>
            <option value="No_Risk">No Risk</option>
          </select>

          <button onClick={loadData} className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition">
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-md">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 uppercase tracking-wider font-semibold">
              <tr>
                <th className="py-3 px-4">Animal ID</th>
                <th className="py-3 px-4">Farm</th>
                <th className="py-3 px-4">Date</th>
                <th className="py-3 px-4">Breed</th>
                <th className="py-3 px-4">Conductivity</th>
                <th className="py-3 px-4">Body Temp</th>
                <th className="py-3 px-4">7d Forecast</th>
                <th className="py-3 px-4">14d Forecast</th>
                <th className="py-3 px-4">Predicted Risk</th>
                <th className="py-3 px-4 text-right">Inspect</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr>
                  <td colSpan="10" className="py-12 text-center text-slate-400">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
                    <p>Fetching prediction records...</p>
                  </td>
                </tr>
              ) : records.map((cow) => (
                <tr key={cow.animal_id} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4 font-bold text-white font-mono">#{cow.animal_id}</td>
                  <td className="py-3 px-4 font-mono text-slate-300">{cow.farm_id}</td>
                  <td className="py-3 px-4 text-slate-400">{cow.record_date}</td>
                  <td className="py-3 px-4 text-slate-200">{cow.breed}</td>
                  <td className="py-3 px-4 font-mono text-slate-200">{cow.milk_conductivity_mS_cm} mS/cm</td>
                  <td className="py-3 px-4 font-mono text-slate-200">{cow.body_temperature_c} °C</td>
                  <td className="py-3 px-4 font-mono text-slate-300">
                    {cow.mastitis_in_next_7d ? <span className="text-rose-400 font-bold">Positive (1)</span> : 'Negative (0)'}
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-300">
                    {cow.mastitis_in_next_14d ? <span className="text-rose-400 font-bold">Positive (1)</span> : 'Negative (0)'}
                  </td>
                  <td className="py-3 px-4">
                    <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => onSelectAnimal(cow.animal_id)}
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white transition inline-flex items-center gap-1 text-[11px]"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Inspect</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
