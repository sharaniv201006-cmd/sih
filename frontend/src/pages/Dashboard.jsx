import React from 'react';
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
