import React, { useState } from 'react';
import { 
  PlusCircle, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  Info,
  Check,
  X,
  RotateCcw,
  Sparkles,
  Zap
} from 'lucide-react';
import { registerAnimal } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const AnimalRegistration = ({ onRegistrationSuccess, onInspectAnimal }) => {
  // PRE-FILLED WITH REALISTIC SAMPLE DATA FOR 1-CLICK INSTANT USE
  const [animalId, setAnimalId] = useState('12005');
  const [breed, setBreed] = useState('Gir');
  const [age, setAge] = useState('3.5');
  const [lactation, setLactation] = useState('2');
  const [hadMastitisBefore, setHadMastitisBefore] = useState(false);
  const [abnormalBehavior, setAbnormalBehavior] = useState(false);

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [registeredResult, setRegisteredResult] = useState(null);

  const loadSample = (type) => {
    setErrorMessage('');
    if (type === 'healthy_gir') {
      setAnimalId(String(Math.floor(12000 + Math.random() * 8000)));
      setBreed('Gir');
      setAge('3.5');
      setLactation('2');
      setHadMastitisBefore(false);
      setAbnormalBehavior(false);
    } else if (type === 'risk_hf') {
      setAnimalId(String(Math.floor(12000 + Math.random() * 8000)));
      setBreed('HF_cross');
      setAge('4.5');
      setLactation('3');
      setHadMastitisBefore(true);
      setAbnormalBehavior(true);
    } else if (type === 'murrah') {
      setAnimalId(String(Math.floor(12000 + Math.random() * 8000)));
      setBreed('Murrah');
      setAge('5.0');
      setLactation('3');
      setHadMastitisBefore(false);
      setAbnormalBehavior(false);
    }
  };

  const resetForm = () => {
    setAnimalId('');
    setBreed('Jersey_cross');
    setAge('');
    setLactation('');
    setHadMastitisBefore(false);
    setAbnormalBehavior(false);
    setErrorMessage('');
    setRegisteredResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    const parsedId = parseInt(animalId);
    if (!animalId || isNaN(parsedId) || parsedId <= 0) {
      setErrorMessage('Please enter a valid positive Animal ID (e.g. 12005).');
      return;
    }

    const parsedAge = parseFloat(age);
    if (!age || isNaN(parsedAge) || parsedAge <= 0 || parsedAge > 20) {
      setErrorMessage('Please enter a valid age in years (e.g. 3.5).');
      return;
    }

    const parsedLact = parseInt(lactation);
    if (!lactation || isNaN(parsedLact) || parsedLact <= 0 || parsedLact > 15) {
      setErrorMessage('Please enter a valid lactation number (e.g. 2).');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        animal_id: parsedId,
        breed: breed,
        age_years: parsedAge,
        lactation_number: parsedLact,
        previous_mastitis_history: hadMastitisBefore,
        abnormal_behavior: abnormalBehavior
      };

      const res = await registerAnimal(payload);
      if (res.success) {
        setRegisteredResult(res);
        if (onRegistrationSuccess) onRegistrationSuccess(res.animal);
      } else {
        setErrorMessage(res.message || 'Registration failed.');
      }
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || 'Error connecting to backend server.';
      setErrorMessage(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* 3D Header */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center justify-center p-3 rounded-2xl icon-3d-emerald text-emerald-700 mb-1">
          <PlusCircle className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight">Animal Registration</h2>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Enroll a new bovine to active AI surveillance. Milking, biometric, and environmental sensors will be paired automatically by the IoT network.
        </p>

        {/* Quick 1-Click Sample Pre-Fill Buttons */}
        <div className="flex items-center justify-center gap-2 pt-2 flex-wrap">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Zap className="w-3 h-3 text-amber-500" />
            <span>Sample Presets:</span>
          </span>
          <button
            type="button"
            onClick={() => loadSample('healthy_gir')}
            className="px-3 py-1 rounded-xl btn-3d-slate text-emerald-800 text-xs font-bold hover:border-emerald-300 transition"
          >
            🟢 Gir (Healthy Sample)
          </button>
          <button
            type="button"
            onClick={() => loadSample('risk_hf')}
            className="px-3 py-1 rounded-xl btn-3d-slate text-amber-800 text-xs font-bold hover:border-amber-300 transition"
          >
            🟡 HF Cross (At-Risk Sample)
          </button>
          <button
            type="button"
            onClick={() => loadSample('murrah')}
            className="px-3 py-1 rounded-xl btn-3d-slate text-sky-800 text-xs font-bold hover:border-sky-300 transition"
          >
            🔵 Murrah (Buffalo Sample)
          </button>
        </div>
      </div>

      {/* Success Notification View */}
      {registeredResult ? (
        <div className="box-3d-static p-8 shadow-[0_20px_50px_-10px_rgba(16,185,129,0.15)] space-y-6 text-center border-emerald-200">
          
          <div className="w-16 h-16 rounded-full icon-3d-emerald text-emerald-700 flex items-center justify-center mx-auto shadow-md">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h3 className="text-xl font-bold text-slate-900">
              Animal #{registeredResult.animal.animal_id} Registered Successfully!
            </h3>
            <p className="text-xs text-slate-500">
              Integrated into the dataset and evaluated through the XGBoost ML pipeline.
            </p>
          </div>

          {/* Initial AI Evaluation Summary */}
          {registeredResult.initial_prediction && (
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-left shadow-inner">
              <div>
                <span className="text-[11px] text-slate-500 uppercase font-bold">Initial AI Baseline Risk</span>
                <div className="flex items-center gap-2 mt-1">
                  <RiskBadge 
                    category={registeredResult.initial_prediction.risk_category} 
                    score={registeredResult.initial_prediction.risk_score} 
                    size="md" 
                  />
                  <span className="text-xs text-slate-600 font-medium">
                    Breed: {registeredResult.animal.breed}
                  </span>
                </div>
              </div>

              <div className="text-right sm:text-right text-xs text-slate-500">
                <span>7-Day Risk: <strong className="text-slate-800">{registeredResult.initial_prediction.forecast_7d_risk_pct}%</strong></span>
                <p className="text-[10px] text-slate-400">Continuous IoT Telemetry Ready</p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <button
              onClick={() => onInspectAnimal(registeredResult.animal.animal_id)}
              className="px-6 py-3 rounded-xl btn-3d-emerald text-white font-bold text-xs flex items-center justify-center gap-2"
            >
              <span>Inspect Animal in Surveillance</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={resetForm}
              className="px-6 py-3 rounded-xl btn-3d-slate text-slate-700 font-bold text-xs flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Register Another Animal</span>
            </button>
          </div>

        </div>
      ) : (
        /* Minimal Registration Form with 3D Depth */
        <div className="box-3d-static p-8 shadow-[0_20px_40px_-10px_rgba(15,23,42,0.08)]">
          
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {errorMessage && (
              <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5 shadow-xs">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <span className="font-semibold">{errorMessage}</span>
              </div>
            )}

            {/* Input 1: Animal ID */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                1. Animal ID <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                min="1"
                step="1"
                placeholder="Enter unique ear tag / collar ID (e.g. 12005)"
                value={animalId}
                onChange={(e) => setAnimalId(e.target.value)}
                className="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl text-base text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-mono font-bold"
                required
              />
              <span className="text-[11px] text-slate-400 mt-1 block">
                System automatically verifies ID to prevent duplicates.
              </span>
            </div>

            {/* Input 2: Breed */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                2. Breed <span className="text-rose-500">*</span>
              </label>
              <select
                value={breed}
                onChange={(e) => setBreed(e.target.value)}
                className="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-900 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-bold"
              >
                <option value="Gir">Gir</option>
                <option value="Sahiwal">Sahiwal</option>
                <option value="Red Sindhi">Red Sindhi</option>
                <option value="Ongole">Ongole</option>
                <option value="Hariana">Hariana</option>
                <option value="Kankrej">Kankrej</option>
                <option value="Tharparkar">Tharparkar</option>
                <option value="Hallikar">Hallikar</option>
                <option value="Deoni">Deoni</option>
                <option value="Dangi">Dangi</option>
                <option value="Rathi">Rathi</option>
                <option value="Kangayam">Kangayam</option>
                <option value="Umblachery">Umblachery</option>
                <option value="Vechur">Vechur</option>
                <option value="Krishna Valley">Krishna Valley</option>
              </select>
            </div>

            {/* Input 3 & 4: Age & Lactation Number */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                  3. Age (Years) <span className="text-rose-500">*</span>
                </label>
                <input
                  type="number"
                  min="0.5"
                  max="20"
                  step="0.1"
                  placeholder="e.g. 3.5"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl text-base text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-mono font-bold"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                  4. Lactation Number <span className="text-rose-500">*</span>
                </label>
                <input
                  type="number"
                  min="1"
                  max="15"
                  step="1"
                  placeholder="e.g. 2"
                  value={lactation}
                  onChange={(e) => setLactation(e.target.value)}
                  className="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl text-base text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] transition font-mono font-bold"
                  required
                />
              </div>
            </div>

            {/* Question 5: Has the animal had mastitis before? */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] space-y-2.5">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                5. Has the animal had mastitis before?
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setHadMastitisBefore(true)}
                  className={`py-3 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    hadMastitisBefore
                      ? 'bg-rose-500 text-white border-rose-600 shadow-[0_4px_12px_rgba(244,63,94,0.35)]'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100 shadow-xs'
                  }`}
                >
                  <Check className="w-4 h-4" />
                  <span>Yes (Prior History)</span>
                </button>

                <button
                  type="button"
                  onClick={() => setHadMastitisBefore(false)}
                  className={`py-3 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    !hadMastitisBefore
                      ? 'bg-emerald-600 text-white border-emerald-700 shadow-[0_4px_12px_rgba(16,185,129,0.35)]'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100 shadow-xs'
                  }`}
                >
                  <X className="w-4 h-4" />
                  <span>No (Clean History)</span>
                </button>
              </div>
            </div>

            {/* Question 6: Is the animal currently showing abnormal behavior? */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 shadow-[inset_0_2px_4px_rgba(0,0,0,0.02)] space-y-2.5">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                6. Is the animal currently showing abnormal behavior?
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setAbnormalBehavior(true)}
                  className={`py-3 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    abnormalBehavior
                      ? 'bg-amber-500 text-white border-amber-600 shadow-[0_4px_12px_rgba(245,158,11,0.35)]'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100 shadow-xs'
                  }`}
                >
                  <Check className="w-4 h-4" />
                  <span>Yes (Restless / Low intake)</span>
                </button>

                <button
                  type="button"
                  onClick={() => setAbnormalBehavior(false)}
                  className={`py-3 px-4 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition ${
                    !abnormalBehavior
                      ? 'bg-emerald-600 text-white border-emerald-700 shadow-[0_4px_12px_rgba(16,185,129,0.35)]'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100 shadow-xs'
                  }`}
                >
                  <X className="w-4 h-4" />
                  <span>No (Normal Activity)</span>
                </button>
              </div>
            </div>

            {/* Info Box */}
            <div className="flex items-start gap-2.5 p-3.5 rounded-2xl bg-emerald-50 border border-emerald-100 text-xs text-emerald-800 shadow-xs">
              <Info className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>
                IoT physical sensors (collar temperature, milking conductivity, barn sensors) will pair automatically to this ID for continuous telemetry.
              </span>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 rounded-xl btn-3d-emerald text-white font-bold text-sm flex items-center justify-center gap-2 transition disabled:opacity-50"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
              ) : (
                <PlusCircle className="w-5 h-5" />
              )}
              <span className="tracking-wide">REGISTER ANIMAL & INITIALIZE AI MONITORING</span>
            </button>

          </form>

        </div>
      )}

    </div>
  );
};
