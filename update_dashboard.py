# -*- coding: utf-8 -*-
with open("frontend/src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  Users, 
  ShieldCheck, 
  AlertCircle, 
  AlertTriangle, 
  Flame, 
  PlusCircle, 
  PieChart as PieIcon,
  ArrowRight,
  Search
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

export const Dashboard = ({ data, onSelectAnimal, onNavigate }) => {
  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  // Risk Distribution Donut Chart Data
  const pieData = [
    { 
      name: 'No Risk', 
      value: data.no_risk_count, 
      pct: data.risk_distribution_pct.No_Risk,
      color: '#10b981' 
    },
    { 
      name: 'Low Risk', 
      value: data.low_risk_count, 
      pct: data.risk_distribution_pct.Low,
      color: '#0ea5e9' 
    },
    { 
      name: 'Moderate Risk', 
      value: data.moderate_risk_count, 
      pct: data.risk_distribution_pct.Moderate,
      color: '#f59e0b' 
    },
    { 
      name: 'High Risk', 
      value: data.high_risk_count, 
      pct: data.risk_distribution_pct.High,
      color: '#f43f5e' 
    },
  ];

  // High-Risk Alert Animals sorted descending by risk percentage
  const highRiskAnimals = [...(data.recent_high_risk_alerts || [])].sort(
    (a, b) => b.risk_score - a.risk_score
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      
      {/* 1. TOP HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-1">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              BovineGuard AI
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Executive Herd Dashboard
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Real-time herd risk segmentation & early bovine mastitis forecasting
          </p>
        </div>

        <button
          onClick={() => onNavigate('register-animal')}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl btn-3d-emerald text-white text-xs font-bold shadow-md self-start sm:self-auto"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Register Animal</span>
        </button>
      </div>

      {/* 2. RISK SUMMARY CARDS (EXACTLY 5 CARDS) */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3.5 sm:gap-4">
        <MetricCard 
          title="Total Herd" 
          value={data.total_animals.toLocaleString()} 
          subtext="Direct Excel Source" 
          icon={Users} 
          color="sky" 
        />
        <MetricCard 
          title="No Risk" 
          value={data.no_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.No_Risk}% healthy`} 
          icon={ShieldCheck} 
          color="emerald" 
        />
        <MetricCard 
          title="Low Risk" 
          value={data.low_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.Low}% monitored`} 
          icon={AlertCircle} 
          color="sky" 
        />
        <MetricCard 
          title="Moderate Risk" 
          value={data.moderate_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.Moderate}% subclinical`} 
          icon={AlertTriangle} 
          color="amber" 
        />
        <MetricCard 
          title="High Risk Alert" 
          value={data.high_risk_count.toLocaleString()} 
          subtext={`${data.risk_distribution_pct.High}% critical`} 
          icon={Flame} 
          color="rose" 
        />
      </div>

      {/* 3. HERD RISK DISTRIBUTION GRAPH (ONLY ONE GRAPH) */}
      <div className="box-3d-static p-6 sm:p-7">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl icon-3d-emerald text-emerald-700">
              <PieIcon className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-black text-slate-900 tracking-tight">
                Herd Risk Distribution
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Dynamic XGBoost multi-class segmentation results
              </p>
            </div>
          </div>
          <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-full border border-slate-200">
            {data.total_animals.toLocaleString()} Total Animals
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          {/* Donut Chart */}
          <div className="lg:col-span-6 h-64 sm:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie 
                  data={pieData} 
                  cx="50%" 
                  cy="50%" 
                  innerRadius={70} 
                  outerRadius={100} 
                  paddingAngle={5} 
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value, name, props) => [`${Number(value).toLocaleString()} cows (${props.payload.pct}%)`, name]}
                  contentStyle={{ 
                    backgroundColor: '#ffffff', 
                    borderColor: '#e2e8f0', 
                    borderRadius: '16px', 
                    boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)',
                    fontWeight: 'bold',
                    fontSize: '12px'
                  }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Counts & Percentages Breakdown */}
          <div className="lg:col-span-6 grid grid-cols-2 gap-3.5">
            {pieData.map((item) => (
              <div 
                key={item.name} 
                className="p-4 rounded-2xl bg-slate-50/90 border border-slate-200/90 shadow-2xs hover:bg-white hover:border-slate-300 transition"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="w-3 h-3 rounded-full shrink-0 shadow-xs" style={{ backgroundColor: item.color }} />
                  <span className="text-xs font-bold text-slate-700">{item.name}</span>
                </div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-2xl font-black font-mono text-slate-900">
                    {item.value.toLocaleString()}
                  </span>
                  <span className="text-xs font-black px-2 py-0.5 rounded-md font-mono" style={{ color: item.color, backgroundColor: `${item.color}15` }}>
                    {item.pct}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 4. HIGH-RISK ALERT ANIMALS TABLE */}
      <div className="box-3d-static p-6 sm:p-7">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl icon-3d-rose text-rose-700">
              <Flame className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-black text-slate-900 tracking-tight">
                High-Risk Alert Animals
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Animals showing critical risk probability &mdash; sorted from highest to lowest risk
              </p>
            </div>
          </div>
          <span className="text-xs font-bold text-rose-700 bg-rose-50 px-3 py-1 rounded-full border border-rose-200">
            {highRiskAnimals.length} Urgent Action Required
          </span>
        </div>

        {/* Clean, Minimal Animal Rows */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Animal ID</th>
                <th className="py-3 px-4">Breed</th>
                <th className="py-3 px-4">Mastitis Risk Percentage</th>
                <th className="py-3 px-4 text-center">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs font-medium">
              {highRiskAnimals.map((animal) => (
                <tr 
                  key={animal.animal_id}
                  className="hover:bg-rose-50/40 transition-colors group"
                >
                  {/* Animal ID */}
                  <td className="py-3.5 px-4 font-black font-mono text-slate-900 text-sm">
                    #{animal.animal_id}
                  </td>

                  {/* Breed */}
                  <td className="py-3.5 px-4 text-slate-700 font-bold">
                    {animal.breed}
                  </td>

                  {/* Mastitis Risk Percentage */}
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-black text-rose-600 text-sm">
                        {animal.risk_score.toFixed(1)}%
                      </span>
                      <div className="w-20 bg-slate-100 h-2 rounded-full overflow-hidden hidden sm:block">
                        <div 
                          className="bg-rose-500 h-full rounded-full" 
                          style={{ width: `${Math.min(100, animal.risk_score)}%` }} 
                        />
                      </div>
                    </div>
                  </td>

                  {/* HIGH RISK Label */}
                  <td className="py-3.5 px-4 text-center">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-rose-100 text-rose-700 border border-rose-200 shadow-2xs">
                      <span className="w-1.5 h-1.5 rounded-full bg-rose-600 animate-ping shrink-0" />
                      <span>HIGH RISK</span>
                    </span>
                  </td>

                  {/* Inspect Button */}
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => onSelectAnimal(animal.animal_id)}
                      className="px-3.5 py-1.5 rounded-xl btn-3d-slate hover:bg-emerald-600 hover:text-white hover:border-emerald-600 text-slate-700 font-bold text-xs transition shadow-2xs inline-flex items-center gap-1.5"
                    >
                      <span>Inspect</span>
                      <ArrowRight className="w-3.5 h-3.5" />
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
""")

print("Updated Dashboard.jsx to clean, minimal SIH presentation layout.")
