import React, { useState, useEffect } from 'react';
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
