import React, { useState, useEffect } from 'react';
import { 
  Search, 
  ChevronLeft, 
  ChevronRight, 
  ArrowRight, 
  RefreshCw, 
  Filter, 
  Activity,
  Flame,
  ShieldCheck,
  AlertTriangle,
  AlertCircle
} from 'lucide-react';
import { fetchAnimals } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const Animals = ({ onSelectAnimal }) => {
  const [animals, setAnimals] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(12);
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

  const filterPills = [
    { id: 'All', label: 'All Animals', count: `${totalCount}`, color: 'slate' },
    { id: 'High', label: 'High Risk Alert', count: '76', color: 'rose', icon: Flame },
    { id: 'Moderate', label: 'Moderate Watch', count: '67', color: 'amber', icon: AlertTriangle },
    { id: 'Low', label: 'Low Risk', count: '94', color: 'sky', icon: AlertCircle },
    { id: 'No_Risk', label: 'Healthy / No Risk', count: '263', color: 'emerald', icon: ShieldCheck },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fadeIn">
      
      {/* Top Header & Overview */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-1">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Herd Master Inventory
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Herd Surveillance
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Search, filter, and inspect health status across {totalCount.toLocaleString()} cattle records
          </p>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="relative self-start sm:self-auto">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search Tag ID (e.g. #3991) or Breed..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 shadow-xs w-64 sm:w-72 font-medium"
          />
        </form>
      </div>

      {/* 1-Click Quick Filter Bar */}
      <div className="box-3d-static p-3 sm:p-4 flex flex-wrap items-center justify-between gap-3">
        
        {/* Risk Filter Buttons */}
        <div className="flex items-center gap-2 flex-wrap">
          {filterPills.map((pill) => {
            const isSelected = riskFilter === pill.id;
            return (
              <button
                key={pill.id}
                onClick={() => { setRiskFilter(pill.id); setPage(1); }}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
                  isSelected
                    ? pill.color === 'rose' 
                      ? 'bg-rose-600 text-white shadow-sm'
                      : pill.color === 'amber'
                      ? 'bg-amber-500 text-white shadow-sm'
                      : pill.color === 'sky'
                      ? 'bg-sky-600 text-white shadow-sm'
                      : pill.color === 'emerald'
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : 'bg-slate-900 text-white shadow-sm'
                    : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200/80'
                }`}
              >
                <span>{pill.label}</span>
              </button>
            );
          })}
        </div>

        {/* Breed Selector */}
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider hidden md:inline">
            Breed:
          </span>
          <select
            value={breedFilter}
            onChange={(e) => { setBreedFilter(e.target.value); setPage(1); }}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:bg-white focus:border-emerald-500 font-bold"
          >
            <option value="All">All Indian Breeds</option>
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

      </div>

      {/* Clean, Highly Understandable Table */}
      <div className="box-3d-static overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                <th className="py-3.5 px-5">Animal ID</th>
                <th className="py-3.5 px-5">Breed</th>
                <th className="py-3.5 px-5">Body Temperature</th>
                <th className="py-3.5 px-5">Udder Temperature</th>
                <th className="py-3.5 px-5">Health & Mastitis Risk</th>
                <th className="py-3.5 px-5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs font-medium">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-16 text-center text-slate-500">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mb-2"></div>
                    <p className="font-medium text-xs">Loading cattle records...</p>
                  </td>
                </tr>
              ) : animals.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-16 text-center text-slate-500">
                    <p className="font-bold text-sm text-slate-700">No animals found</p>
                    <p className="text-xs text-slate-400 mt-1">Try selecting a different filter or search query.</p>
                  </td>
                </tr>
              ) : (
                animals.map((cow) => {
                  const bTemp = parseFloat(cow.body_temperature_c || 38.6);
                  const uTemp = parseFloat(cow.udder_surface_temperature_c || 33.9);
                  const isHighRisk = cow.mastitis_risk_category === 'High';
                  const isFever = bTemp > 38.9;
                  const isWarmUdder = uTemp > 34.5;

                  return (
                    <tr 
                      key={cow.animal_id} 
                      className={`hover:bg-slate-50/80 transition-colors ${isHighRisk ? 'bg-rose-50/30' : ''}`}
                    >
                      {/* Animal ID */}
                      <td className="py-4 px-5">
                        <span className="font-black font-mono text-slate-900 text-sm">
                          #{cow.animal_id}
                        </span>
                      </td>

                      {/* Breed & Location */}
                      <td className="py-4 px-5">
                        <span className="font-bold text-slate-900 block">{cow.breed.replace('_', ' ')}</span>
                        {cow.state && (
                          <span className="text-[11px] text-slate-400 font-medium block">
                            {cow.district ? `${cow.district}, ` : ''}{cow.state}
                          </span>
                        )}
                      </td>

                      {/* Body Temp */}
                      <td className="py-4 px-5">
                        <div className="flex items-center gap-1.5 font-mono">
                          <span className={`w-2 h-2 rounded-full shrink-0 ${isFever ? 'bg-rose-500' : 'bg-emerald-500'}`} />
                          <span className={`font-bold ${isFever ? 'text-rose-600 font-black' : 'text-slate-700'}`}>
                            {bTemp.toFixed(2)} °C
                          </span>
                        </div>
                      </td>

                      {/* Udder Temp */}
                      <td className="py-4 px-5">
                        <div className="flex items-center gap-1.5 font-mono">
                          <span className={`w-2 h-2 rounded-full shrink-0 ${isWarmUdder ? 'bg-rose-500' : 'bg-emerald-500'}`} />
                          <span className={`font-bold ${isWarmUdder ? 'text-rose-600 font-black' : 'text-slate-700'}`}>
                            {uTemp.toFixed(2)} °C
                          </span>
                        </div>
                      </td>

                      {/* Risk Category */}
                      <td className="py-4 px-5">
                        <RiskBadge 
                          category={cow.mastitis_risk_category} 
                          score={cow.synthetic_risk_score_pct} 
                          size="sm" 
                        />
                      </td>

                      {/* Inspect Action */}
                      <td className="py-4 px-5 text-right">
                        <button
                          onClick={() => onSelectAnimal(cow.animal_id)}
                          className="px-3.5 py-1.5 rounded-xl btn-3d-slate hover:bg-emerald-600 hover:text-white hover:border-emerald-600 text-slate-700 font-bold text-xs transition shadow-2xs inline-flex items-center gap-1.5"
                        >
                          <span>Inspect</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Clean Pagination Bar */}
        <div className="flex items-center justify-between px-5 py-3.5 border-t border-slate-100 bg-slate-50/70 text-xs text-slate-500 font-medium">
          <span>
            Page <strong>{page}</strong> of <strong>{totalPages}</strong> ({totalCount.toLocaleString()} cattle)
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3.5 py-1.5 rounded-xl btn-3d-slate disabled:opacity-40 disabled:cursor-not-allowed text-slate-700 transition flex items-center gap-1 font-bold text-xs"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Previous</span>
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-3.5 py-1.5 rounded-xl btn-3d-slate disabled:opacity-40 disabled:cursor-not-allowed text-slate-700 transition flex items-center gap-1 font-bold text-xs"
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
