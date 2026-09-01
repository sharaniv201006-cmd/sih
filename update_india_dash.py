# -*- coding: utf-8 -*-
with open("frontend/src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { 
  Users, 
  ShieldCheck, 
  AlertTriangle, 
  Flame, 
  MapPin, 
  Calendar, 
  ArrowRight, 
  ChevronRight, 
  Activity, 
  RefreshCw,
  Layers,
  Sparkles
} from 'lucide-react';
import { fetchIndiaRisk, fetchStateRisk } from '../services/api';
import { IndiaMap } from '../components/IndiaMap';

export const Dashboard = ({ onSelectAnimal, onNavigate }) => {
  const [indiaData, setIndiaData] = useState(null);
  const [selectedState, setSelectedState] = useState('Karnataka'); // Default selected active state
  const [stateDetail, setStateDetail] = useState(null);
  const [loadingMap, setLoadingMap] = useState(true);
  const [loadingState, setLoadingState] = useState(false);

  // 1. Fetch national India risk aggregated data
  const loadIndiaSummary = async () => {
    setLoadingMap(true);
    try {
      const data = await fetchIndiaRisk();
      setIndiaData(data);
    } catch (err) {
      console.error('Error fetching India risk:', err);
    } finally {
      setLoadingMap(false);
    }
  };

  // 2. Fetch district-wise data for clicked state
  const loadStateDistricts = async (stateName) => {
    setSelectedState(stateName);
    setLoadingState(true);
    try {
      const sData = await fetchStateRisk(stateName);
      setStateDetail(sData);
    } catch (err) {
      console.error('Error fetching state details:', err);
    } finally {
      setLoadingState(false);
    }
  };

  useEffect(() => {
    loadIndiaSummary();
  }, []);

  useEffect(() => {
    if (selectedState) {
      loadStateDistricts(selectedState);
    }
  }, [selectedState]);

  if (loadingMap || !indiaData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[450px] space-y-3">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div>
        <p className="text-xs font-bold text-slate-500">Loading India Herd Surveillance Map...</p>
      </div>
    );
  }

  const {
    total_animals,
    no_risk_count,
    low_moderate_count,
    high_risk_count,
    overall_herd_risk_pct,
    last_updated,
    state_risks
  } = indiaData;

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fadeIn">
      
      {/* 1. TOP HEADER & METADATA */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-1">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              National AI Surveillance
            </span>
            <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>Last Updated: {last_updated}</span>
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Bovine Mastitis India Risk Heatmap
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Interactive national geospatial epidemiology and district-level predictive surveillance
          </p>
        </div>

        {/* Overall Herd Risk Badge */}
        <div className="p-3.5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 text-amber-700 flex items-center justify-center font-bold">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Overall Herd Risk
            </span>
            <span className="text-lg font-black font-mono text-slate-900">
              {overall_herd_risk_pct}% Average
            </span>
          </div>
        </div>
      </div>

      {/* 2. FOUR SUMMARY CARDS */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: Total Animals */}
        <div className="box-3d-static p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
              Total Animals
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-slate-900 mt-1 block">
              {total_animals.toLocaleString()}
            </span>
            <span className="text-[11px] text-slate-400 font-medium">Verified Indian Cattle</span>
          </div>
          <div className="p-3 rounded-2xl icon-3d-sky text-sky-700">
            <Users className="w-6 h-6" />
          </div>
        </div>

        {/* Card 2: No Risk */}
        <div className="box-3d-static p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
              No Risk
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-emerald-600 mt-1 block">
              {no_risk_count.toLocaleString()}
            </span>
            <span className="text-[11px] text-emerald-700 font-bold">
              {((no_risk_count / total_animals) * 100).toFixed(1)}% Healthy
            </span>
          </div>
          <div className="p-3 rounded-2xl icon-3d-emerald text-emerald-700">
            <ShieldCheck className="w-6 h-6" />
          </div>
        </div>

        {/* Card 3: Low / Moderate Risk */}
        <div className="box-3d-static p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
              Low / Moderate Risk
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-amber-600 mt-1 block">
              {low_moderate_count.toLocaleString()}
            </span>
            <span className="text-[11px] text-amber-700 font-bold">
              {((low_moderate_count / total_animals) * 100).toFixed(1)}% Monitored
            </span>
          </div>
          <div className="p-3 rounded-2xl icon-3d-amber text-amber-700">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>

        {/* Card 4: High Risk Alert */}
        <div className="box-3d-static p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
              High Risk
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-rose-600 mt-1 block">
              {high_risk_count.toLocaleString()}
            </span>
            <span className="text-[11px] text-rose-700 font-bold">
              {((high_risk_count / total_animals) * 100).toFixed(1)}% Urgent Inspection
            </span>
          </div>
          <div className="p-3 rounded-2xl icon-3d-rose text-rose-700">
            <Flame className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* 3. MAIN SECTION: INTERACTIVE INDIA MAP & STATE/DISTRICT DRILL-DOWN */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column: Interactive Map of India (7 Cols) */}
        <div className="lg:col-span-7 box-3d-static p-6 sm:p-7 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
                <MapPin className="w-4 h-4" />
              </div>
              <div>
                <h2 className="text-base font-black text-slate-900">National Mastitis Heatmap</h2>
                <p className="text-xs text-slate-500">Hover over any State/UT for risk summary &bull; Click to view districts</p>
              </div>
            </div>
            <button 
              onClick={loadIndiaSummary}
              className="p-1.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-500 transition"
              title="Refresh Heatmap"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Interactive Vector Map Component */}
          <IndiaMap 
            stateRisks={state_risks} 
            selectedState={selectedState}
            onSelectState={(st) => loadStateDistricts(st)}
          />
        </div>

        {/* Right Column: State & District-Wise Risk Breakdown (5 Cols) */}
        <div className="lg:col-span-5 box-3d-static p-6 sm:p-7 space-y-5">
          
          {/* Header of Selected State */}
          <div className="border-b border-slate-100 pb-3 flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-black uppercase text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-200">
                  State Focus
                </span>
              </div>
              <h3 className="text-xl font-black text-slate-900 mt-1">
                {selectedState}
              </h3>
            </div>

            {stateDetail && stateDetail.districts?.length > 0 && (
              <div className="text-right">
                <span className="text-xs font-bold text-slate-400 block">State Avg Risk</span>
                <span className="text-xl font-black font-mono text-emerald-700">
                  {stateDetail.state_risk_pct}%
                </span>
              </div>
            )}
          </div>

          {/* District Risk List */}
          {loadingState ? (
            <div className="py-12 text-center text-slate-500 space-y-2">
              <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-emerald-500 mx-auto"></div>
              <p className="text-xs font-medium">Fetching district biometrics for {selectedState}...</p>
            </div>
          ) : !stateDetail || !stateDetail.districts || stateDetail.districts.length === 0 ? (
            <div className="py-12 text-center text-slate-400 space-y-2">
              <Info className="w-8 h-8 mx-auto text-slate-300" />
              <p className="text-xs font-bold text-slate-700">No data available for {selectedState}</p>
              <p className="text-[11px] text-slate-400 max-w-xs mx-auto">
                Click on states with active surveillance data (e.g. Karnataka, Gujarat, Tamil Nadu, Maharashtra, Rajasthan).
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <span className="text-xs font-bold text-slate-600 block uppercase tracking-wider">
                District-Wise Risk Breakdown ({stateDetail.districts.length} Districts)
              </span>

              <div className="space-y-2.5">
                {stateDetail.districts.map((d, idx) => {
                  const getBadgeColor = (tier) => {
                    if (tier === 'Critical' || tier === 'High') return 'bg-rose-100 text-rose-700 border-rose-200';
                    if (tier === 'Moderate') return 'bg-amber-100 text-amber-700 border-amber-200';
                    return 'bg-emerald-100 text-emerald-700 border-emerald-200';
                  };

                  return (
                    <div 
                      key={idx}
                      className="p-3.5 rounded-2xl bg-slate-50/90 border border-slate-200/90 hover:bg-white hover:border-emerald-300 transition-all shadow-2xs flex items-center justify-between"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-black text-slate-900">{d.district}</span>
                          <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded-md border ${getBadgeColor(d.risk_tier)}`}>
                            {d.risk_tier}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 font-medium mt-0.5">
                          {d.total_animals} cattle &bull; <strong className="text-rose-600 font-bold">{d.high_risk_animals} high risk</strong>
                        </p>
                      </div>

                      <div className="text-right">
                        <span className="text-sm font-black font-mono text-slate-900 block">
                          {d.risk_percentage}%
                        </span>
                        <span className="text-[10px] text-slate-400 font-medium">Risk Score</span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Sample Cattle from this State */}
              {stateDetail.animals_sample && stateDetail.animals_sample.length > 0 && (
                <div className="pt-3 border-t border-slate-100">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-slate-700">Sample Cattle in {selectedState}</span>
                    <button 
                      onClick={() => onNavigate('animals')}
                      className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
                    >
                      <span>View in Herd</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>

                  <div className="space-y-1.5">
                    {stateDetail.animals_sample.slice(0, 4).map((cow) => (
                      <div 
                        key={cow.animal_id}
                        onClick={() => onSelectAnimal(cow.animal_id)}
                        className="p-2 rounded-xl bg-white border border-slate-200 hover:border-emerald-400 cursor-pointer transition flex items-center justify-between text-xs"
                      >
                        <div className="flex items-center gap-2 font-mono">
                          <span className="font-bold text-slate-900">#{cow.animal_id}</span>
                          <span className="text-slate-600 font-sans">{cow.breed}</span>
                        </div>
                        <span className="font-mono font-bold text-emerald-700">
                          {cow.synthetic_risk_score_pct}% &rarr;
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}

        </div>

      </div>

    </div>
  );
};
""")

print("Updated Dashboard.jsx with Interactive India Map and district-wise drilldown.")
