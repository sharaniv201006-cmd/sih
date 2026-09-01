# -*- coding: utf-8 -*-
# 1. Update Animals.jsx to show state/district subtitle
with open("frontend/src/pages/Animals.jsx", "r", encoding="utf-8") as f:
    anim_code = f.read()

old_cell = """                      {/* Breed */}
                      <td className="py-4 px-5 font-bold text-slate-700">
                        {cow.breed.replace('_', ' ')}
                      </td>"""

new_cell = """                      {/* Breed & Location */}
                      <td className="py-4 px-5">
                        <span className="font-bold text-slate-900 block">{cow.breed.replace('_', ' ')}</span>
                        {cow.state && (
                          <span className="text-[11px] text-slate-400 font-medium block">
                            {cow.district ? `${cow.district}, ` : ''}{cow.state}
                          </span>
                        )}
                      </td>"""

if old_cell in anim_code:
    anim_code = anim_code.replace(old_cell, new_cell)
    with open("frontend/src/pages/Animals.jsx", "w", encoding="utf-8") as f:
        f.write(anim_code)
    print("Updated Animals.jsx with State/District display.")

# 2. Update AnimalDetail.jsx to show state & district badge
with open("frontend/src/pages/AnimalDetail.jsx", "r", encoding="utf-8") as f:
    detail_code = f.read()

old_detail_hdr = """          <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
            {animal.breed}
          </span>"""

new_detail_hdr = """          <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
            {animal.breed}
          </span>
          {animal.state && (
            <span className="text-xs font-bold text-sky-800 bg-sky-50 px-3 py-1.5 rounded-xl border border-sky-200 hidden sm:inline-block">
              📍 {animal.district ? `${animal.district}, ` : ''}{animal.state}
            </span>
          )}"""

if old_detail_hdr in detail_code:
    detail_code = detail_code.replace(old_detail_hdr, new_detail_hdr)
    with open("frontend/src/pages/AnimalDetail.jsx", "w", encoding="utf-8") as f:
        f.write(detail_code)
    print("Updated AnimalDetail.jsx with State/District location badge.")
