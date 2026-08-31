import React, { useState, useEffect } from 'react';
import { Sliders, ArrowRight, CheckCircle2 } from 'lucide-react';
import { fetchAnimals } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const Alerts = ({ onSelectAnimal }) => {
  const [alertThreshold, setAlertThreshold] = useState(60);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const res = await fetchAnimals({
        page: 1,
        page_size: 50,
        sort_by: 'synthetic_risk_score_pct',
        sort_order: 'desc'
      });
      const filtered = res.animals.filter(
        (a) => (a.synthetic_risk_score_pct || 0) >= alertThreshold
      );
      setAlerts(filtered);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [alertThreshold]);

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200/90 p-5 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">Configurable Alert Center</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-700 border border-rose-200">
              {alerts.length} Active Alerts
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Real-time threshold surveillance and veterinary screening recommendations
          </p>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 px-4 py-2.5 rounded-xl border border-slate-200">
          <Sliders className="w-4 h-4 text-emerald-600" />
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-500 uppercase font-bold">High-Risk Alert Threshold</span>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min="30"
                max="85"
                step="5"
                value={alertThreshold}
                onChange={(e) => setAlertThreshold(parseInt(e.target.value))}
                className="w-32 accent-emerald-600"
              />
              <span className="text-xs font-mono font-bold text-slate-900">{alertThreshold}%</span>
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-500">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
          <p>Scanning herd against {alertThreshold}% threshold...</p>
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500 shadow-sm">
          <CheckCircle2 className="w-12 h-12 mx-auto text-emerald-600 mb-3" />
          <h3 className="text-base font-bold text-slate-900">No Animals Above Current Threshold</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            All animals in the current herd dataset have risk scores below {alertThreshold}%.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {alerts.map((cow) => (
            <div
              key={cow.animal_id}
              className="bg-white border border-rose-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-rose-300 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-700 border border-rose-200 flex items-center justify-center font-mono font-bold text-sm">
                      #{cow.animal_id}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{cow.breed}</h4>
                      <p className="text-[11px] text-slate-500">Farm: {cow.farm_id} &bull; Lactation #{cow.lactation_number}</p>
                    </div>
                  </div>
                  <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                </div>

                <div className="grid grid-cols-2 gap-2 my-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                  <div>
                    <span className="text-slate-500 text-[10px] font-medium block">Conductivity</span>
                    <strong className="font-mono text-rose-600 font-bold">{cow.milk_conductivity_mS_cm} mS/cm</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] font-medium block">Body Temp</span>
                    <strong className="font-mono text-amber-600 font-bold">{cow.body_temperature_c} °C</strong>
                  </div>
                </div>

                <div className="text-[11px] text-slate-600 leading-relaxed">
                  <strong className="text-slate-800">Decision-Support Suggestion: </strong>
                  Perform California Mastitis Test (CMT) at next milking. Quarantine milk until subclinical clearance.
                </div>
              </div>

              <button
                onClick={() => onSelectAnimal(cow.animal_id)}
                className="mt-4 w-full py-2.5 rounded-xl bg-slate-100 hover:bg-emerald-600 text-slate-700 hover:text-white text-xs font-bold flex items-center justify-center gap-2 transition"
              >
                <span>Inspect Full Biometric Profile</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
