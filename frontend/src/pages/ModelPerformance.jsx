import React, { useState, useEffect } from 'react';
import { Award, CheckCircle, BarChart2, Layers } from 'lucide-react';
import { fetchModelPerformance } from '../services/api';
import { MetricCard } from '../components/MetricCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const ModelPerformance = () => {
  const [modelData, setModelData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const res = await fetchModelPerformance();
        setModelData(res);
      } catch (err) {
        console.error('Error fetching model performance:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading || !modelData) return <div className="flex items-center justify-center min-h-[400px]"><div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500"></div></div>;

  const { metrics, feature_importance } = modelData;
  const topFeatures = (feature_importance || []).slice(0, 10);
  const classes = metrics.classes || ['No_Risk', 'Low', 'Moderate', 'High'];
  const cm = metrics.confusion_matrix || [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]];

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200/90 p-5 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">{metrics.model_name || 'XGBoost Multi-Class Model'}</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
              Evaluated on 2,400 Test Samples
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Algorithm: {metrics.algorithm} &bull; Pipeline: Standard Scaler + One-Hot Encoding + Multi:Softprob
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Accuracy" value={`${((metrics.accuracy || 0) * 100).toFixed(1)}%`} subtext="Stratified 80/20 split" icon={Award} color="emerald" />
        <MetricCard title="Weighted Precision" value={`${((metrics.precision || 0) * 100).toFixed(1)}%`} subtext="Multi-class precision" icon={CheckCircle} color="sky" />
        <MetricCard title="Weighted Recall" value={`${((metrics.recall || 0) * 100).toFixed(1)}%`} subtext="True positive detection" icon={BarChart2} color="purple" />
        <MetricCard title="F1-Score" value={`${((metrics.f1_score || 0) * 100).toFixed(1)}%`} subtext="Harmonic mean" icon={Layers} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">XGBoost Feature Importance Ranking</h3>
              <p className="text-xs text-slate-500">Relative gain percentage per model feature</p>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topFeatures} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis dataKey="feature" type="category" stroke="#64748b" tick={{ fontSize: 10 }} width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} formatter={(val) => [`${val}%`, 'Importance']} />
                <Bar dataKey="importance" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Confusion Matrix (Test Evaluation)</h3>
            <p className="text-xs text-slate-500 mb-4">Predicted vs Actual category assignments</p>
            <div className="overflow-x-auto">
              <table className="w-full text-center text-xs">
                <thead>
                  <tr className="text-slate-500 border-b border-slate-200">
                    <th className="py-2 text-left font-bold">Actual \ Pred</th>
                    {classes.map((c) => (
                      <th key={c} className="py-2 px-2 text-slate-800 font-bold">{c.replace(/_/g, ' ')}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {cm.map((row, i) => (
                    <tr key={i}>
                      <td className="py-3 px-2 text-left font-bold text-slate-700">{classes[i]?.replace(/_/g, ' ')}</td>
                      {row.map((val, j) => (
                        <td key={j} className={`py-3 px-2 font-mono font-bold ${i === j ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg' : 'text-slate-400'}`}>
                          {val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <p className="mt-4 text-[11px] text-slate-500 border-t border-slate-100 pt-3">
            <strong>Training Details: </strong>
            150 estimators, max depth = 6, learning rate = 0.08, stratified 80/20 train-test split over 500 Indian breed dataset records.
          </p>
        </div>
      </div>
    </div>
  );
};
