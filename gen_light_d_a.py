# 1. Update pages/Dashboard.jsx
with open("frontend/src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Users, ShieldCheck, AlertCircle, AlertTriangle, Flame, Activity, ArrowRight, TrendingUp } from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { EnvironmentalCard } from '../components/EnvironmentalCard';
import { AlertBanner } from '../components/AlertBanner';
import { RiskBadge } from '../components/RiskBadge';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';

export const Dashboard = ({ data, onSelectAnimal, onNavigate }) => {
  if (!data) return <div className="flex items-center justify-center min-h-[400px]"><div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div></div>;

  const pieData = [
    { name: 'No Risk', value: data.no_risk_count, color: '#10b981' },
    { name: 'Low Risk', value: data.low_risk_count, color: '#0ea5e9' },
    { name: 'Moderate Risk', value: data.moderate_risk_count, color: '#f59e0b' },
    { name: 'High Risk', value: data.high_risk_count, color: '#f43f5e' },
  ];

  const herdComparison = [
    { metric: 'Body Temp (°C)', value: data.herd_averages.avg_body_temp, normal: 38.6 },
    { metric: 'Udder Temp (°C)', value: data.herd_averages.avg_udder_temp, normal: 33.8 },
    { metric: 'Conductivity', value: data.herd_averages.avg_milk_conductivity, normal: 4.2 },
    { metric: 'Milk Yield (kg)', value: data.herd_averages.avg_milk_yield, normal: 15.0 },
    { metric: 'Hygiene Score', value: data.herd_averages.avg_hygiene_score, normal: 65.0 },
  ];

  return (
    <div className="space-y-6">
      <AlertBanner alerts={data.recent_high_risk_alerts} onSelectAnimal={onSelectAnimal} />

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard title="Total Herd" value={data.total_animals.toLocaleString()} subtext="Direct Excel Source" icon={Users} color="sky" />
        <MetricCard title="No Risk" value={data.no_risk_count.toLocaleString()} subtext={`${data.risk_distribution_pct.No_Risk}% healthy`} icon={ShieldCheck} color="emerald" />
        <MetricCard title="Low Risk" value={data.low_risk_count.toLocaleString()} subtext={`${data.risk_distribution_pct.Low}% monitored`} icon={AlertCircle} color="sky" />
        <MetricCard title="Moderate Risk" value={data.moderate_risk_count.toLocaleString()} subtext={`${data.risk_distribution_pct.Moderate}% subclinical`} icon={AlertTriangle} color="amber" />
        <MetricCard title="High Risk Alert" value={data.high_risk_count.toLocaleString()} subtext={`${data.risk_distribution_pct.High}% critical`} icon={Flame} color="rose" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Herd Risk Distribution</h3>
              <p className="text-xs text-slate-500">XGBoost Multi-Class Segmentation</p>
            </div>
            <Activity className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={85} paddingAngle={4} dataKey="value">
                  {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} itemStyle={{ color: '#0f172a', fontWeight: 'bold' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center gap-2 text-xs text-slate-600 font-medium">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span>{item.name}: <strong>{item.value}</strong></span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Herd Sensor Means</h3>
              <p className="text-xs text-slate-500">Observed Mean vs Reference Baselines</p>
            </div>
            <TrendingUp className="w-4 h-4 text-sky-600" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={herdComparison} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="metric" stroke="#64748b" tick={{ fontSize: 10 }} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="value" name="Herd Average" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="normal" name="Normal Ref" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <EnvironmentalCard envData={data.environmental_status} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Critical Decision-Support Alerts</h3>
              <p className="text-xs text-slate-500">Animals requiring immediate screening</p>
            </div>
            <button onClick={() => onNavigate('alerts')} className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
              <span>View All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="space-y-3">
            {data.recent_high_risk_alerts.slice(0, 4).map((alert) => (
              <div key={alert.animal_id} onClick={() => onSelectAnimal(alert.animal_id)} className="p-3.5 rounded-xl bg-rose-50/50 border border-rose-100 hover:border-rose-300 cursor-pointer transition flex items-center justify-between shadow-2xs">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-rose-100 border border-rose-200 flex items-center justify-center text-rose-700 font-bold text-xs font-mono">
                    #{alert.animal_id}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-900">{alert.breed}</span>
                      <span className="text-[10px] text-slate-500">Farm: {alert.farm_id}</span>
                    </div>
                    <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                      {alert.top_factors.map((f, i) => (
                        <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white text-rose-700 font-medium border border-rose-200">{f}</span>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-sm font-black font-mono text-rose-600">{alert.risk_score}%</span>
                  <p className="text-[10px] text-rose-600 uppercase font-bold">HIGH RISK</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Recent Herd Telemetry</h3>
              <p className="text-xs text-slate-500">Live records from Excel data stream</p>
            </div>
            <button onClick={() => onNavigate('animals')} className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
              <span>Explore Herd</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-500 border-b border-slate-200 font-semibold">
                <tr>
                  <th className="pb-2">Animal</th>
                  <th className="pb-2">Breed</th>
                  <th className="pb-2">Conductivity</th>
                  <th className="pb-2">Body Temp</th>
                  <th className="pb-2">Risk</th>
                  <th className="pb-2 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.recent_predictions.slice(0, 6).map((cow) => (
                  <tr key={cow.animal_id} className="hover:bg-slate-50 transition">
                    <td className="py-2.5 font-bold text-slate-900 font-mono">#{cow.animal_id}</td>
                    <td className="py-2.5 text-slate-600 font-medium">{cow.breed}</td>
                    <td className="py-2.5 font-mono text-slate-700">{cow.milk_conductivity_mS_cm} mS/cm</td>
                    <td className="py-2.5 font-mono text-slate-700">{cow.body_temperature_c} °C</td>
                    <td className="py-2.5">
                      <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                    </td>
                    <td className="py-2.5 text-right">
                      <button onClick={() => onSelectAnimal(cow.animal_id)} className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-emerald-600 hover:text-white text-slate-700 transition text-[11px] font-bold">
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

# 2. Update pages/Animals.jsx
with open("frontend/src/pages/Animals.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Search, ChevronLeft, ChevronRight, Eye, RefreshCw } from 'lucide-react';
import { fetchAnimals } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const Animals = ({ onSelectAnimal }) => {
  const [animals, setAnimals] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(15);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('All');
  const [breedFilter, setBreedFilter] = useState('All');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchAnimals({
        page,
        page_size: pageSize,
        search: search.trim() || undefined,
        risk: riskFilter !== 'All' ? riskFilter : undefined,
        breed: breedFilter !== 'All' ? breedFilter : undefined,
      });
      setAnimals(data.animals);
      setTotalCount(data.total_count);
      setTotalPages(data.total_pages);
    } catch (err) {
      console.error('Failed to fetch animals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, riskFilter, breedFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadData();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200/90 p-5 rounded-2xl shadow-sm">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Herd Inventory & Surveillance</h2>
          <p className="text-xs text-slate-500">
            Surveillance over {totalCount.toLocaleString()} animal records loaded directly from Excel
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <form onSubmit={handleSearchSubmit} className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search ID, Farm, Breed..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 w-48 sm:w-56 font-medium"
            />
          </form>

          <select
            value={riskFilter}
            onChange={(e) => { setRiskFilter(e.target.value); setPage(1); }}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:bg-white focus:border-emerald-500 font-medium"
          >
            <option value="All">All Risk Levels</option>
            <option value="No_Risk">No Risk</option>
            <option value="Low">Low Risk</option>
            <option value="Moderate">Moderate Risk</option>
            <option value="High">High Risk</option>
          </select>

          <select
            value={breedFilter}
            onChange={(e) => { setBreedFilter(e.target.value); setPage(1); }}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:bg-white focus:border-emerald-500 font-medium"
          >
            <option value="All">All Breeds</option>
            <option value="Jersey_cross">Jersey Cross</option>
            <option value="HF_cross">HF Cross</option>
            <option value="Gir">Gir</option>
            <option value="Sahiwal">Sahiwal</option>
            <option value="Murrah">Murrah</option>
          </select>

          <button onClick={loadData} className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl transition border border-slate-200" title="Refresh Data">
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-200/90 rounded-2xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 border-b border-slate-200 uppercase tracking-wider font-bold">
              <tr>
                <th className="py-3.5 px-4">Animal ID</th>
                <th className="py-3.5 px-4">Farm</th>
                <th className="py-3.5 px-4">Breed</th>
                <th className="py-3.5 px-4">Age / Lact.</th>
                <th className="py-3.5 px-4">Milk Yield</th>
                <th className="py-3.5 px-4">Conductivity</th>
                <th className="py-3.5 px-4">Body Temp</th>
                <th className="py-3.5 px-4">Udder Temp</th>
                <th className="py-3.5 px-4">Risk Category</th>
                <th className="py-3.5 px-4 text-right">Inspect</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="10" className="py-12 text-center text-slate-500">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
                    <p>Loading animal telemetry records...</p>
                  </td>
                </tr>
              ) : animals.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-12 text-center text-slate-500">
                    No animals found matching current filters.
                  </td>
                </tr>
              ) : (
                animals.map((cow) => (
                  <tr key={cow.animal_id} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-4 font-bold text-slate-900 font-mono">#{cow.animal_id}</td>
                    <td className="py-3 px-4 text-slate-600 font-mono">{cow.farm_id}</td>
                    <td className="py-3 px-4 text-slate-700 font-medium">{cow.breed}</td>
                    <td className="py-3 px-4 text-slate-600">{cow.age_years} yrs / L{cow.lactation_number}</td>
                    <td className="py-3 px-4 font-mono text-slate-700 font-medium">{cow.milk_yield_kg_day} kg</td>
                    <td className="py-3 px-4 font-mono">
                      <span className={cow.milk_conductivity_mS_cm > 4.5 ? 'text-rose-600 font-bold' : 'text-slate-700'}>
                        {cow.milk_conductivity_mS_cm} mS/cm
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <span className={cow.body_temperature_c > 39.0 ? 'text-amber-600 font-bold' : 'text-slate-700'}>
                        {cow.body_temperature_c} °C
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-700">{cow.udder_surface_temperature_c} °C</td>
                    <td className="py-3 px-4">
                      <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => onSelectAnimal(cow.animal_id)}
                        className="p-1.5 rounded-lg bg-slate-100 hover:bg-emerald-600 text-slate-700 hover:text-white transition inline-flex items-center gap-1 text-[11px] font-bold"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Details</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-slate-50 text-xs text-slate-500 font-medium">
          <span>Page <strong>{page}</strong> of <strong>{totalPages}</strong> ({totalCount.toLocaleString()} cows)</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3 py-1.5 rounded-lg bg-white border border-slate-200 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed text-slate-700 transition flex items-center gap-1 font-semibold"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Prev</span>
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-3 py-1.5 rounded-lg bg-white border border-slate-200 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed text-slate-700 transition flex items-center gap-1 font-semibold"
            >
              <span>Next</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

print("Dashboard.jsx & Animals.jsx updated.")
