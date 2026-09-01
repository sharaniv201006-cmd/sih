# -*- coding: utf-8 -*-
# Update breed options in Animals.jsx and AnimalRegistration.jsx

with open("frontend/src/pages/Animals.jsx", "r", encoding="utf-8") as f:
    animals_code = f.read()

indian_breeds_options = """<option value="All">All Indian Breeds</option>
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
            <option value="Krishna Valley">Krishna Valley</option>"""

# Replace in Animals.jsx
old_anim_options = """<option value="All">All Breeds</option>
            <option value="Jersey_cross">Jersey Cross</option>
            <option value="HF_cross">Holstein Friesian (HF)</option>
            <option value="Gir">Gir</option>
            <option value="Sahiwal">Sahiwal</option>
            <option value="Murrah">Murrah Buffalo</option>"""

if old_anim_options in animals_code:
    animals_code = animals_code.replace(old_anim_options, indian_breeds_options)
    with open("frontend/src/pages/Animals.jsx", "w", encoding="utf-8") as f:
        f.write(animals_code)
    print("Updated Animals.jsx with Indian breed options.")

# Replace in AnimalRegistration.jsx
with open("frontend/src/pages/AnimalRegistration.jsx", "r", encoding="utf-8") as f:
    reg_code = f.read()

old_reg_options = """<option value="Jersey_cross">Jersey Cross</option>
                <option value="HF_cross">Holstein Friesian (HF) Cross</option>
                <option value="Gir">Gir (Indigenous)</option>
                <option value="Sahiwal">Sahiwal (Indigenous)</option>
                <option value="Murrah">Murrah Buffalo</option>"""

new_reg_options = """<option value="Gir">Gir</option>
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
                <option value="Krishna Valley">Krishna Valley</option>"""

if old_reg_options in reg_code:
    reg_code = reg_code.replace(old_reg_options, new_reg_options)
    with open("frontend/src/pages/AnimalRegistration.jsx", "w", encoding="utf-8") as f:
        f.write(reg_code)
    print("Updated AnimalRegistration.jsx with Indian breed options.")
