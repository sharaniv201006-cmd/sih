# -*- coding: utf-8 -*-
# Create components/Sidebar.jsx
with open("frontend/src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { 
  LayoutDashboard, 
  PlusCircle, 
  Activity, 
  Sliders, 
  BellRing, 
  Cpu, 
  Layers, 
  LogOut, 
  ChevronLeft, 
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

export const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  isCollapsed, 
  setIsCollapsed, 
  user, 
  onLogout,
  isBackendOnline 
}) => {
  const menuItems = [
    { id: 'all-in-one', label: 'All-In-One View', icon: Layers, highlight: true },
    { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
    { id: 'register-animal', label: 'Register Animal', icon: PlusCircle, badge: 'New' },
    { id: 'animals', label: 'Herd Surveillance', icon: Activity },
    { id: 'live-monitoring', label: 'Live IoT Simulator', icon: Sliders },
    { id: 'alerts', label: 'Decision Alerts', icon: BellRing },
    { id: 'model-performance', label: 'ML Performance', icon: Cpu },
  ];

  return (
    <aside
      className={`sticky top-0 h-screen bg-white border-r border-slate-200 shadow-[4px_0_24px_rgba(0,0,0,0.03)] flex flex-col justify-between transition-all duration-300 z-40 ${
        isCollapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Top Header & Brand */}
      <div>
        <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100">
          <div 
            className="flex items-center gap-3 cursor-pointer overflow-hidden"
            onClick={() => setActiveTab('dashboard')}
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-md shadow-emerald-500/25 shrink-0">
              <span className="text-xl font-black text-white">BM</span>
            </div>
            {!isCollapsed && (
              <div className="animate-fadeIn">
                <span className="font-extrabold text-base tracking-tight text-slate-900 block leading-tight">
                  BovineGuard
                </span>
                <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-wider block">
                  AI Surveillance
                </span>
              </div>
            )}
          </div>

          {/* Collapse/Expand Toggle Button */}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-500 hover:text-slate-800 transition"
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Menu Items */}
        <nav className="p-3 space-y-1.5 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                title={isCollapsed ? item.label : undefined}
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-2xl text-xs font-bold transition-all duration-200 group ${
                  isActive
                    ? 'btn-3d-emerald text-white shadow-md shadow-emerald-600/30'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                } ${item.highlight && !isActive ? 'text-emerald-700 bg-emerald-50/60 border border-emerald-100' : ''}`}
              >
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-white' : 'text-slate-500 group-hover:text-slate-800'}`} />
                
                {!isCollapsed && (
                  <div className="flex-1 flex items-center justify-between overflow-hidden animate-fadeIn">
                    <span className="truncate">{item.label}</span>
                    {item.badge && (
                      <span className={`px-1.5 py-0.5 text-[9px] font-bold rounded uppercase ${
                        isActive ? 'bg-white/20 text-white' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom User Profile & Status */}
      <div className="p-3 border-t border-slate-100 space-y-2">
        {/* Model Online Status */}
        <div className={`p-2.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center gap-2">
            <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${isBackendOnline ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            {!isCollapsed && (
              <span className="text-[11px] font-bold text-slate-700">
                {isBackendOnline ? 'AI Model Online' : 'Connecting API'}
              </span>
            )}
          </div>
          {!isCollapsed && (
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          )}
        </div>

        {/* User Card & Logout */}
        {user && (
          <div className={`p-2 rounded-2xl bg-white border border-slate-200/90 shadow-2xs flex items-center ${isCollapsed ? 'justify-center' : 'justify-between gap-2'}`}>
            <div className="flex items-center gap-2 overflow-hidden">
              <div className="w-8 h-8 rounded-xl bg-emerald-100 border border-emerald-200 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0">
                {user.name ? user.name.charAt(0) : 'U'}
              </div>
              {!isCollapsed && (
                <div className="overflow-hidden">
                  <span className="text-xs font-bold text-slate-900 block truncate">{user.name || user.username}</span>
                  <span className="text-[10px] text-slate-500 font-medium block truncate">{user.role || 'Veterinarian'}</span>
                </div>
              )}
            </div>
            {!isCollapsed && (
              <button
                onClick={onLogout}
                title="Log out"
                className="p-1.5 rounded-xl hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition shrink-0"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        )}
      </div>
    </aside>
  );
};
""")
print("Sidebar.jsx created.")
