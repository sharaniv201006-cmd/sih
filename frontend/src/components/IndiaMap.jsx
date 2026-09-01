import React, { useState } from 'react';
import { MapPin, ShieldAlert, CheckCircle2, AlertTriangle, Info, ArrowRight, Eye, Layers } from 'lucide-react';

// Comprehensive, accurate SVG boundary paths for Indian States and UTs
const INDIA_STATES_PATHS = [
  {
    id: 'Jammu & Kashmir',
    name: 'Jammu & Kashmir',
    d: 'M 195,35 L 215,25 L 240,30 L 255,50 L 240,75 L 210,80 L 195,65 Z',
    labelX: 215,
    labelY: 55
  },
  {
    id: 'Ladakh',
    name: 'Ladakh',
    d: 'M 240,30 L 285,35 L 305,65 L 290,95 L 255,80 L 240,75 L 255,50 Z',
    labelX: 270,
    labelY: 60
  },
  {
    id: 'Himachal Pradesh',
    name: 'Himachal Pradesh',
    d: 'M 215,80 L 245,78 L 260,105 L 235,115 L 215,95 Z',
    labelX: 235,
    labelY: 98
  },
  {
    id: 'Punjab',
    name: 'Punjab',
    d: 'M 180,95 L 215,90 L 215,125 L 185,130 L 175,110 Z',
    labelX: 195,
    labelY: 112
  },
  {
    id: 'Uttarakhand',
    name: 'Uttarakhand',
    d: 'M 240,110 L 275,115 L 285,140 L 250,145 L 235,120 Z',
    labelX: 260,
    labelY: 130
  },
  {
    id: 'Haryana',
    name: 'Haryana',
    d: 'M 205,125 L 235,120 L 235,155 L 210,165 L 195,140 Z',
    labelX: 215,
    labelY: 145
  },
  {
    id: 'Delhi',
    name: 'Delhi',
    d: 'M 225,142 L 232,142 L 232,149 L 225,149 Z',
    labelX: 228,
    labelY: 146
  },
  {
    id: 'Rajasthan',
    name: 'Rajasthan',
    d: 'M 125,140 L 195,135 L 215,165 L 205,230 L 140,240 L 115,190 Z',
    labelX: 160,
    labelY: 185
  },
  {
    id: 'Uttar Pradesh',
    name: 'Uttar Pradesh',
    d: 'M 235,145 L 315,155 L 350,210 L 280,240 L 235,195 L 230,160 Z',
    labelX: 290,
    labelY: 190
  },
  {
    id: 'Gujarat',
    name: 'Gujarat',
    d: 'M 85,220 L 140,230 L 165,275 L 135,310 L 80,270 L 60,240 Z',
    labelX: 110,
    labelY: 265
  },
  {
    id: 'Madhya Pradesh',
    name: 'Madhya Pradesh',
    d: 'M 165,235 L 270,230 L 305,290 L 220,320 L 160,285 Z',
    labelX: 230,
    labelY: 275
  },
  {
    id: 'Bihar',
    name: 'Bihar',
    d: 'M 350,195 L 415,200 L 410,245 L 345,240 Z',
    labelX: 380,
    labelY: 220
  },
  {
    id: 'West Bengal',
    name: 'West Bengal',
    d: 'M 410,225 L 435,230 L 425,310 L 395,300 L 405,250 Z',
    labelX: 415,
    labelY: 270
  },
  {
    id: 'Jharkhand',
    name: 'Jharkhand',
    d: 'M 345,240 L 405,245 L 395,295 L 340,285 Z',
    labelX: 370,
    labelY: 265
  },
  {
    id: 'Odisha',
    name: 'Odisha',
    d: 'M 330,290 L 395,295 L 380,365 L 315,350 L 320,310 Z',
    labelX: 350,
    labelY: 330
  },
  {
    id: 'Chhattisgarh',
    name: 'Chhattisgarh',
    d: 'M 285,255 L 335,260 L 320,360 L 280,350 L 280,285 Z',
    labelX: 300,
    labelY: 310
  },
  {
    id: 'Maharashtra',
    name: 'Maharashtra',
    d: 'M 140,305 L 235,300 L 275,355 L 205,405 L 145,370 Z',
    labelX: 200,
    labelY: 350
  },
  {
    id: 'Telangana',
    name: 'Telangana',
    d: 'M 225,365 L 285,360 L 280,425 L 220,420 Z',
    labelX: 250,
    labelY: 395
  },
  {
    id: 'Andhra Pradesh',
    name: 'Andhra Pradesh',
    d: 'M 235,420 L 305,375 L 325,430 L 255,490 L 225,450 Z',
    labelX: 275,
    labelY: 450
  },
  {
    id: 'Karnataka',
    name: 'Karnataka',
    d: 'M 175,395 L 225,390 L 235,480 L 180,495 L 165,420 Z',
    labelX: 195,
    labelY: 445
  },
  {
    id: 'Goa',
    name: 'Goa',
    d: 'M 160,420 L 170,420 L 168,435 L 158,435 Z',
    labelX: 164,
    labelY: 428
  },
  {
    id: 'Kerala',
    name: 'Kerala',
    d: 'M 180,495 L 205,490 L 215,570 L 195,575 Z',
    labelX: 195,
    labelY: 535
  },
  {
    id: 'Tamil Nadu',
    name: 'Tamil Nadu',
    d: 'M 215,485 L 260,485 L 250,575 L 205,570 Z',
    labelX: 235,
    labelY: 530
  },
  {
    id: 'Sikkim',
    name: 'Sikkim',
    d: 'M 410,175 L 430,175 L 428,195 L 408,195 Z',
    labelX: 420,
    labelY: 185
  },
  {
    id: 'Assam',
    name: 'Assam',
    d: 'M 450,195 L 520,190 L 510,235 L 445,230 Z',
    labelX: 480,
    labelY: 210
  },
  {
    id: 'Arunachal Pradesh',
    name: 'Arunachal Pradesh',
    d: 'M 480,150 L 565,165 L 545,200 L 475,190 Z',
    labelX: 520,
    labelY: 175
  },
  {
    id: 'Meghalaya',
    name: 'Meghalaya',
    d: 'M 445,215 L 485,215 L 480,235 L 440,235 Z',
    labelX: 460,
    labelY: 225
  },
  {
    id: 'Nagaland',
    name: 'Nagaland',
    d: 'M 530,200 L 555,205 L 545,235 L 525,230 Z',
    labelX: 540,
    labelY: 215
  },
  {
    id: 'Manipur',
    name: 'Manipur',
    d: 'M 525,235 L 550,235 L 545,265 L 520,265 Z',
    labelX: 535,
    labelY: 250
  },
  {
    id: 'Mizoram',
    name: 'Mizoram',
    d: 'M 505,265 L 530,265 L 525,305 L 500,300 Z',
    labelX: 515,
    labelY: 285
  },
  {
    id: 'Tripura',
    name: 'Tripura',
    d: 'M 475,255 L 495,255 L 490,285 L 470,280 Z',
    labelX: 485,
    labelY: 270
  }
];

export const IndiaMap = ({ stateRisks = {}, onSelectState, selectedState }) => {
  const [hoveredState, setHoveredState] = useState(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  const getStateRisk = (stateName) => {
    return stateRisks[stateName] || null;
  };

  const handleMouseMove = (e, state) => {
    setHoveredState(state);
    const rect = e.currentTarget.getBoundingClientRect();
    setTooltipPos({
      x: e.clientX - rect.left + 15,
      y: e.clientY - rect.top - 15
    });
  };

  const handleMouseLeave = () => {
    setHoveredState(null);
  };

  return (
    <div className="relative w-full flex flex-col items-center select-none">
      
      {/* SVG Vector Interactive India Map */}
      <div className="w-full max-w-xl aspect-[5/6] relative flex items-center justify-center">
        <svg
          viewBox="40 10 540 600"
          className="w-full h-full drop-shadow-md transition-all duration-300"
          onMouseLeave={handleMouseLeave}
        >
          <defs>
            {/* Filter for glowing active selected state */}
            <filter id="activeGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#047857" floodOpacity="0.4" />
            </filter>
          </defs>

          {/* Render all States */}
          {INDIA_STATES_PATHS.map((state) => {
            const riskData = getStateRisk(state.name);
            const isHovered = hoveredState?.name === state.name;
            const isSelected = selectedState === state.name;
            
            // Soft professional risk heatmap colors
            let fillColor = '#f1f5f9'; // Slate-100 (No data)
            let strokeColor = '#cbd5e1'; // Slate-300
            let strokeWidth = 1.2;

            if (riskData) {
              fillColor = riskData.color_hex;
              strokeColor = '#ffffff';
              strokeWidth = 1.8;
            }

            if (isSelected) {
              strokeColor = '#065f46';
              strokeWidth = 3;
            } else if (isHovered) {
              strokeColor = '#0f172a';
              strokeWidth = 2.5;
            }

            return (
              <g key={state.id} className="cursor-pointer transition-all duration-150">
                <path
                  d={state.d}
                  fill={fillColor}
                  stroke={strokeColor}
                  strokeWidth={strokeWidth}
                  strokeLinejoin="round"
                  className="transition-all duration-200"
                  style={{
                    filter: isSelected ? 'url(#activeGlow)' : undefined,
                    opacity: isHovered || isSelected ? 1 : 0.92
                  }}
                  onMouseMove={(e) => handleMouseMove(e, state)}
                  onClick={() => onSelectState(state.name)}
                />
                
                {/* State Label abbreviation if has data */}
                {riskData && (
                  <text
                    x={state.labelX}
                    y={state.labelY}
                    fontSize="10"
                    fontWeight="800"
                    fill="#0f172a"
                    textAnchor="middle"
                    pointerEvents="none"
                    className="drop-shadow-xs font-sans"
                  >
                    {riskData.overall_risk_pct}%
                  </text>
                )}
              </g>
            );
          })}
        </svg>

        {/* Dynamic State Hover Tooltip */}
        {hoveredState && (
          <div
            className="absolute z-50 pointer-events-none p-3.5 rounded-2xl bg-white/95 backdrop-blur-md border border-slate-200/90 shadow-xl w-60 animate-fadeIn"
            style={{
              left: `${Math.min(300, Math.max(10, tooltipPos.x))}px`,
              top: `${Math.min(420, Math.max(10, tooltipPos.y))}px`
            }}
          >
            {getStateRisk(hoveredState.name) ? (
              (() => {
                const r = getStateRisk(hoveredState.name);
                return (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-1.5">
                      <span className="text-xs font-black text-slate-900">{r.state}</span>
                      <span 
                        className="text-[10px] font-black uppercase px-2 py-0.5 rounded-md"
                        style={{ backgroundColor: `${r.color_hex}20`, color: r.color_hex }}
                      >
                        {r.risk_tier} Risk
                      </span>
                    </div>

                    <div className="flex items-baseline justify-between">
                      <span className="text-xs text-slate-500 font-medium">Total Cattle:</span>
                      <span className="text-xs font-black text-slate-900 font-mono">{r.total_animals} cows</span>
                    </div>

                    <div className="grid grid-cols-2 gap-1 text-[11px] font-medium pt-1 border-t border-slate-100">
                      <div className="text-emerald-700">🟢 No Risk: <strong>{r.no_risk}</strong></div>
                      <div className="text-sky-700">🔵 Low: <strong>{r.low_risk}</strong></div>
                      <div className="text-amber-700">🟡 Moderate: <strong>{r.moderate_risk}</strong></div>
                      <div className="text-rose-700">🔴 High: <strong>{r.high_risk}</strong></div>
                    </div>

                    <div className="pt-1.5 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-[11px] text-slate-500 font-bold uppercase">Overall Risk:</span>
                      <span className="text-sm font-black font-mono" style={{ color: r.color_hex }}>
                        {r.overall_risk_pct}%
                      </span>
                    </div>

                    <span className="text-[10px] text-slate-400 block text-center italic mt-1">
                      Click state to view district breakdown →
                    </span>
                  </div>
                );
              })()
            ) : (
              <div className="text-center py-2 space-y-1">
                <span className="text-xs font-bold text-slate-800 block">{hoveredState.name}</span>
                <span className="text-[11px] text-slate-400 font-medium block">No surveillance data recorded</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Map Risk Color Legend */}
      <div className="mt-4 p-3 bg-white border border-slate-200/90 rounded-2xl shadow-xs flex items-center justify-center gap-4 sm:gap-6 flex-wrap text-xs font-bold text-slate-700">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-xs" />
          <span>Low Risk (&lt;25%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-amber-500 shadow-xs" />
          <span>Moderate (25-40%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-orange-500 shadow-xs" />
          <span>High (40-60%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-rose-500 shadow-xs" />
          <span>Critical (&gt;60%)</span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-400">
          <span className="w-3 h-3 rounded-full bg-slate-200" />
          <span>No Data</span>
        </div>
      </div>

    </div>
  );
};
