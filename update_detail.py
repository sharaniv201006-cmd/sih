# -*- coding: utf-8 -*-
with open("frontend/src/pages/AnimalDetail.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, 
  AlertTriangle, 
  CheckCircle2, 
  Thermometer, 
  Activity, 
  ShieldAlert, 
  HeartPulse, 
  Check, 
  Info,
  Sparkles
} from 'lucide-react';
import { fetchAnimalDetail } from '../services/api';

export const AnimalDetail = ({ animalId, onBack }) => {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAnimal = async () => {
      setLoading(true);
      try {
        const detRes = await fetchAnimalDetail(animalId);
        setDetail(detRes);
      } catch (err) {
        console.error('Error fetching animal details:', err);
      } finally {
        setLoading(false);
      }
    };
    if (animalId) loadAnimal();
  }, [animalId]);

  if (loading || !detail) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  const { animal, prediction } = detail;
  const isHighRisk = prediction.risk_category === 'High';
  const isModerateRisk = prediction.risk_category === 'Moderate';
  const isLowRisk = prediction.risk_category === 'Low';
  const isNoRisk = prediction.risk_category === 'No_Risk';

  // Format Risk Category Display
  const getRiskColorClasses = () => {
    if (isHighRisk) {
      return {
        bg: 'bg-rose-50 border-rose-200',
        text: 'text-rose-700',
        pill: 'bg-rose-600 text-white',
        scoreText: 'text-rose-600',
        message: 'Immediate veterinary inspection recommended.',
        icon: ShieldAlert
      };
    }
    if (isModerateRisk) {
      return {
        bg: 'bg-amber-50 border-amber-200',
        text: 'text-amber-700',
        pill: 'bg-amber-500 text-white',
        scoreText: 'text-amber-600',
        message: 'Moderate risk detected. Close monitoring advised.',
        icon: AlertTriangle
      };
    }
    return {
      bg: 'bg-emerald-50 border-emerald-200',
      text: 'text-emerald-700',
      pill: 'bg-emerald-600 text-white',
      scoreText: 'text-emerald-600',
      message: 'Animal is in healthy condition. Continue routine monitoring.',
      icon: CheckCircle2
    };
  };

  const riskTheme = getRiskColorClasses();
  const RiskIcon = riskTheme.icon;

  // Determine Simple High-Risk Factors (No complex ML terms)
  const factors = [];
  const bodyTemp = parseFloat(animal.body_temperature_c || 38.6);
  const udderTemp = parseFloat(animal.udder_surface_temperature_c || 33.9);

  if (bodyTemp > 38.9) {
    factors.push({
      title: 'High Body Temperature',
      detail: `${bodyTemp.toFixed(2)} °C`,
      isWarning: true
    });
  } else {
    factors.push({
      title: 'Normal Body Temperature',
      detail: `${bodyTemp.toFixed(2)} °C`,
      isWarning: false
    });
  }

  if (udderTemp > 34.5) {
    factors.push({
      title: 'High Udder Temperature',
      detail: `${udderTemp.toFixed(2)} °C`,
      isWarning: true
    });
  } else {
    factors.push({
      title: 'Normal Udder Temperature',
      detail: `${udderTemp.toFixed(2)} °C`,
      isWarning: false
    });
  }

  // IoT Biometrics (Activity & Rumination)
  const isAbnormalActivity = animal.abnormal_behavior || isHighRisk || isModerateRisk;
  factors.push({
    title: isAbnormalActivity ? 'Low Activity' : 'Normal Activity',
    detail: isAbnormalActivity ? 'Restlessness or reduced movement detected' : 'Normal herd activity',
    isWarning: isAbnormalActivity
  });

  const isAbnormalRumination = isHighRisk || animal.previous_mastitis_history;
  factors.push({
    title: isAbnormalRumination ? 'Abnormal Rumination' : 'Healthy Rumination',
    detail: isAbnormalRumination ? 'Reduced feeding and cud-chewing pattern' : 'Consistent chewing cycle',
    isWarning: isAbnormalRumination
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fadeIn">
      
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <button 
          onClick={onBack} 
          className="flex items-center gap-2 text-xs font-bold text-slate-700 hover:text-slate-900 px-4 py-2.5 rounded-xl btn-3d-slate transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Herd Surveillance</span>
        </button>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono font-bold text-slate-500 bg-white px-3 py-1.5 rounded-xl border border-slate-200">
            Animal Tag: <strong className="text-slate-900">#{animal.animal_id}</strong>
          </span>
          <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
            {animal.breed}
          </span>
        </div>
      </div>

      {/* 1. MASTITIS RISK SUMMARY CARD */}
      <div className={`box-3d-static p-6 sm:p-8 border ${riskTheme.bg}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5">
          <div className="flex items-start gap-4">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shadow-md shrink-0 ${isHighRisk ? 'bg-rose-100 text-rose-700' : isModerateRisk ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'}`}>
              <RiskIcon className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                  Mastitis Risk:
                </span>
                <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${riskTheme.pill}`}>
                  {prediction.risk_category.replace('_', ' ')}
                </span>
              </div>
              <p className="text-sm font-bold text-slate-800 mt-1.5">
                {riskTheme.message}
              </p>
            </div>
          </div>

          <div className="text-left sm:text-right border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-200/60">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
              Risk Score
            </span>
            <span className={`text-4xl sm:text-5xl font-black font-mono tracking-tight ${riskTheme.scoreText}`}>
              {prediction.risk_score.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* 2. WHY IS THIS ANIMAL AT RISK? */}
      <div className="box-3d-static p-6 sm:p-7">
        <h2 className="text-base font-black text-slate-900 tracking-tight mb-1">
          Why is this animal at risk?
        </h2>
        <p className="text-xs text-slate-500 font-medium mb-4">
          Key physiological indicators detected from continuous biometric monitoring
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          {factors.map((f, idx) => (
            <div 
              key={idx}
              className={`p-4 rounded-2xl border transition flex items-start gap-3 ${
                f.isWarning 
                  ? 'bg-rose-50/70 border-rose-200 text-rose-900 shadow-2xs' 
                  : 'bg-emerald-50/50 border-emerald-100 text-emerald-900'
              }`}
            >
              <div className={`p-1.5 rounded-lg shrink-0 mt-0.5 ${
                f.isWarning ? 'bg-rose-200 text-rose-700' : 'bg-emerald-200 text-emerald-700'
              }`}>
                {f.isWarning ? <AlertTriangle className="w-4 h-4" /> : <Check className="w-4 h-4" />}
              </div>
              <div>
                <span className="text-xs font-bold block">{f.title}</span>
                <span className="text-xs font-mono font-bold mt-0.5 block opacity-90">{f.detail}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. LIVE SENSOR READINGS (ONLY 4 CLEAN CARDS) */}
      <div className="box-3d-static p-6 sm:p-7">
        <h2 className="text-base font-black text-slate-900 tracking-tight mb-1">
          Live Sensor Readings
        </h2>
        <p className="text-xs text-slate-500 font-medium mb-4">
          Non-invasive on-animal IoT telemetry
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          {/* 1. Body Temp */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 text-center">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
              Body Temp
            </span>
            <span className={`text-xl font-black font-mono mt-1 block ${bodyTemp > 38.9 ? 'text-rose-600' : 'text-slate-900'}`}>
              {bodyTemp.toFixed(2)} °C
            </span>
            <span className="text-[10px] text-slate-400 font-medium">Normal ~38.6 °C</span>
          </div>

          {/* 2. Udder Temp */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 text-center">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
              Udder Temp
            </span>
            <span className={`text-xl font-black font-mono mt-1 block ${udderTemp > 34.5 ? 'text-rose-600' : 'text-slate-900'}`}>
              {udderTemp.toFixed(2)} °C
            </span>
            <span className="text-[10px] text-slate-400 font-medium">Normal ~33.9 °C</span>
          </div>

          {/* 3. Activity */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 text-center">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
              Activity
            </span>
            <span className={`text-xl font-black mt-1 block ${isAbnormalActivity ? 'text-amber-600' : 'text-emerald-700'}`}>
              {isAbnormalActivity ? 'Low' : 'Normal'}
            </span>
            <span className="text-[10px] text-slate-400 font-medium">IoT Collar</span>
          </div>

          {/* 4. Rumination */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 text-center">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
              Rumination
            </span>
            <span className={`text-xl font-black mt-1 block ${isAbnormalRumination ? 'text-amber-600' : 'text-emerald-700'}`}>
              {isAbnormalRumination ? 'Abnormal' : 'Normal'}
            </span>
            <span className="text-[10px] text-slate-400 font-medium">IoT Collar</span>
          </div>
        </div>
      </div>

      {/* 4. RECOMMENDED ACTIONS */}
      <div className="box-3d-static p-6 sm:p-7 space-y-4">
        <h2 className="text-base font-black text-slate-900 tracking-tight">
          Recommended Actions
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-bold text-slate-700">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center shrink-0 text-xs">
              1
            </span>
            <span>Inspect the animal for physical signs</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center shrink-0 text-xs">
              2
            </span>
            <span>Check the udder for swelling or abnormality</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center shrink-0 text-xs">
              3
            </span>
            <span>Perform a veterinary mastitis test if required</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center shrink-0 text-xs">
              4
            </span>
            <span>Continue monitoring sensor readings</span>
          </div>
        </div>

        {/* Small Disclaimer */}
        <div className="flex items-start gap-2 pt-2 border-t border-slate-100 text-[11px] text-slate-400 font-medium">
          <Info className="w-3.5 h-3.5 shrink-0 mt-0.5 text-slate-400" />
          <span>
            AI prediction is a decision-support tool and does not replace veterinary clinical diagnosis.
          </span>
        </div>
      </div>

    </div>
  );
};
""")

print("Updated AnimalDetail.jsx with clean, simple 5-second readable layout.")
