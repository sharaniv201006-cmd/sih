# -*- coding: utf-8 -*-
with open("frontend/src/components/Header.jsx", "r", encoding="utf-8") as f:
    hdr = f.read()
hdr = hdr.replace("12,000+ cattle records", "500 Indian cattle records")
with open("frontend/src/components/Header.jsx", "w", encoding="utf-8") as f:
    f.write(hdr)

with open("frontend/src/pages/ModelPerformance.jsx", "r", encoding="utf-8") as f:
    mp = f.read()
mp = mp.replace("12,000+ dataset records", "500 Indian breed dataset records")
with open("frontend/src/pages/ModelPerformance.jsx", "w", encoding="utf-8") as f:
    f.write(mp)

print("Updated Header.jsx and ModelPerformance.jsx.")
