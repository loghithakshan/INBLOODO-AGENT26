from src.llm.llm_service import LLMService

def generate_recommendations(interpretation: list, risks: list, parameters: dict = None):
    """
    Generate lifestyle recommendations and medical advice based on findings and risks using LLM.
    """
    llm_service = LLMService()
    parameters = parameters or {}
    patient_context = None

    # Try to get recommendations from LLM
    llm_recommendations = llm_service.generate_medical_recommendations(
        interpretations=interpretation,
        risks=risks,
        parameters=parameters,
        patient_context=patient_context
    )

    if llm_recommendations:
        return llm_recommendations

    # Fallback to hardcoded recommendations if LLM fails
    recommendations = []

    # Convert to lowercase for easier matching
    all_findings = [f.lower() for f in interpretation + risks]

    # Anemia recommendations
    if any("anemia" in finding or "low hemoglobin" in finding for finding in all_findings):
        recommendations.extend([
            "Increase iron-rich foods: spinach, lentils, red meat",
            "Consider vitamin C rich foods to enhance iron absorption",
            "Consult doctor for iron supplements if needed",
            "Regular blood tests to monitor hemoglobin levels"
        ])

    # Diabetes recommendations
    if any("diabetes" in finding or "glucose" in finding or "hba1c" in finding for finding in all_findings):
        recommendations.extend([
            "Follow low glycemic index diet",
            "Regular physical exercise (30 minutes daily)",
            "Monitor blood sugar levels regularly",
            "Consult endocrinologist for diabetes management",
            "Weight management if BMI > 25"
        ])

    # Liver issues
    if any("liver" in finding or "alt" in finding or "ast" in finding or "bilirubin" in finding for finding in all_findings):
        recommendations.extend([
            "Avoid alcohol consumption",
            "Follow liver-friendly diet: avoid fried foods, processed meats",
            "Stay hydrated and maintain healthy weight",
            "Consult hepatologist for liver function evaluation"
        ])

    # Kidney issues
    if any("kidney" in finding or "creatinine" in finding or "urea" in finding for finding in all_findings):
        recommendations.extend([
            "Reduce salt intake (<2g sodium daily)",
            "Stay well hydrated (2-3 liters water daily)",
            "Limit protein intake if advised by doctor",
            "Regular monitoring of kidney function",
            "Consult nephrologist for kidney health"
        ])

    # Cardiovascular risk
    if any("cholesterol" in finding or "cardiovascular" in finding or "ldl" in finding for finding in all_findings):
        recommendations.extend([
            "Heart-healthy diet: Mediterranean diet recommended",
            "Reduce saturated fats and trans fats",
            "Increase omega-3 rich foods: fish, nuts, seeds",
            "Regular cardiovascular exercise",
            "Quit smoking if applicable",
            "Consult cardiologist for heart health assessment"
        ])

    # Thyroid issues
    if any("thyroid" in finding or "tsh" in finding for finding in all_findings):
        recommendations.extend([
            "Iodine-rich diet for thyroid health",
            "Regular thyroid function monitoring",
            "Consult endocrinologist for thyroid management",
            "Medication adherence if prescribed"
        ])

    # Electrolyte imbalances
    if any("sodium" in finding or "potassium" in finding or "electrolyte" in finding for finding in all_findings):
        recommendations.extend([
            "Balanced diet with adequate fruits and vegetables",
            "Monitor salt intake carefully",
            "Stay hydrated appropriately",
            "Consult doctor before making dietary changes"
        ])

    # Vitamin deficiencies
    if any("vitamin" in finding or "iron" in finding for finding in all_findings):
        recommendations.extend([
            "Include variety of colorful vegetables and fruits",
            "Consider multivitamin supplements after medical consultation",
            "Regular nutrient level monitoring"
        ])

    # Infection/Inflammation
    if any("infection" in finding or "wbc" in finding for finding in all_findings):
        recommendations.extend([
            "Maintain good hygiene practices",
            "Adequate rest and sleep",
            "Balanced nutrition to support immune system",
            "Seek medical attention if symptoms worsen"
        ])

    # General recommendations
    recommendations.extend([
        "Schedule regular health check-ups",
        "Maintain healthy lifestyle: balanced diet, exercise, stress management",
        "Keep medical records organized",
        "Inform healthcare providers about all medications and supplements"
    ])

    return list(set(recommendations))  # Remove duplicates

def generate_prescriptions(interpretation: list, risks: list, parameters: dict):
    """
    Generate natural remedy suggestions based on findings.
    IMPORTANT: These are natural remedy suggestions only - always consult healthcare professionals.
    """
    prescriptions = []

    all_findings = [f.lower() for f in interpretation + risks]

    # Anemia natural remedies
    if any("anemia" in finding or "low hemoglobin" in finding for finding in all_findings):
        prescriptions.extend([
            "🍎 Iron-rich foods: Spinach, lentils, red meat, pumpkin seeds",
            "🍊 Vitamin C foods: Citrus fruits, bell peppers to enhance iron absorption",
            "🥬 Leafy greens: Kale, Swiss chard, beet greens for natural iron",
            "🌰 Nuts and seeds: Almonds, sesame seeds, sunflower seeds",
            "🍇 Dried fruits: Raisins, apricots, prunes for natural iron boost"
        ])

    # Diabetes natural remedies (Based on recent clinical studies)
    if any("diabetes" in finding or "glucose" in finding or "hba1c" in finding for finding in all_findings):
        prescriptions.extend([
            "🌿 Ceylon cinnamon: 1/2 teaspoon daily (2023 studies show 10-15% glucose reduction)",
            "🥬 Bitter melon: 50-100g daily (clinical trials show HbA1c reduction)",
            "🫘 Fenugreek seeds: 5-10g soaked overnight (meta-analysis shows blood sugar benefits)",
            "🍃 Gymnema sylvestre: 300-400mg daily (traditional + modern research validated)",
            "🫚 Ginger tea: 2g daily (recent studies show improved insulin sensitivity)",
            "🧄 Garlic: 600-1200mg daily (research shows blood sugar regulation benefits)"
        ])

    # Liver issues natural remedies
    if any("liver" in finding or "alt" in finding or "ast" in finding or "bilirubin" in finding for finding in all_findings):
        prescriptions.extend([
            "🫒 Olive oil: Cold-pressed for liver health",
            "🌱 Milk thistle: Traditional liver support herb",
            "🍋 Lemon water: Natural detoxifier for liver",
            "🫚 Turmeric: Anti-inflammatory for liver health",
            "🥕 Beetroot juice: Natural liver cleanser"
        ])

    # Kidney issues natural remedies (Based on nephrology research)
    if any("kidney" in finding or "creatinine" in finding or "urea" in finding for finding in all_findings):
        prescriptions.extend([
            "🥒 Cucumber: 1-2 daily (natural diuretic, supports kidney filtration)",
            "🍇 Unsweetened cranberry juice: 200ml daily (proanthocyanidins prevent UTIs)",
            "🌿 Dandelion root tea: 1 cup daily (natural diuretic, consult doctor first)",
            "🍍 Pineapple: 100g daily (bromelain reduces inflammation)",
            "🥕 Carrot juice: 200ml daily (beta-carotene supports kidney antioxidant defense)",
            "🫐 Blueberries: 1 cup daily (anthocyanins protect kidney cells)"
        ])

    # Cardiovascular risk natural remedies (Based on recent clinical research)
    if any("cholesterol" in finding.lower() or "cardiovascular" in finding.lower() or "ldl" in finding.lower() or "hdl" in finding.lower() for finding in all_findings):
        prescriptions.extend([
            "🫒 Mediterranean diet: 2024 studies show 30% reduced heart disease risk",
            "🧄 Aged garlic extract: 600-1200mg daily (meta-analysis shows LDL reduction)",
            "🫚 Ginger: 2g daily (research shows improved circulation and blood pressure)",
            "🌰 Almonds: 30g daily (clinical trials show LDL cholesterol reduction)",
            "🍎 Apples: 1-2 daily (pectin fiber reduces cholesterol absorption)",
            "🫐 Berries: Rich in anthocyanins for heart protection (blueberries, strawberries)"
        ])

    # Thyroid issues natural remedies (Based on endocrinology research)
    if any("thyroid" in finding or "tsh" in finding for finding in all_findings):
        prescriptions.extend([
            "🌰 Brazil nuts: 1-2 daily (selenium supports thyroid hormone conversion)",
            "🫚 Ginger tea: 2 cups daily (research shows anti-inflammatory thyroid benefits)",
            "🥑 Avocados: 1/2 daily (healthy fats support thyroid hormone production)",
            "🥕 Sweet potatoes: Rich in beta-carotene (supports thyroid hormone synthesis)",
            "🌿 Ashwagandha: 600mg daily (2023 studies show TSH normalization in hypothyroidism)",
            "🧄 Garlic: 600mg daily (contains allicin for thyroid support)"
        ])

    # Electrolyte imbalances natural remedies
    if any("sodium" in finding or "potassium" in finding or "electrolyte" in finding for finding in all_findings):
        prescriptions.extend([
            "🍌 Bananas: Rich in potassium for electrolyte balance",
            "🥥 Coconut water: Natural electrolyte replenisher",
            "🍊 Oranges: Potassium and magnesium source",
            "🥬 Leafy greens: Magnesium and potassium rich",
            "🥜 Nuts: Magnesium and potassium sources"
        ])

    # Vitamin deficiencies natural remedies
    if any("vitamin" in finding or "iron" in finding for finding in all_findings):
        prescriptions.extend([
            "🍊 Citrus fruits: Vitamin C for iron absorption",
            "🥕 Carrots: Beta-carotene (vitamin A precursor)",
            "🍅 Tomatoes: Lycopene and vitamin C",
            "🥬 Dark leafy greens: Multiple vitamins and minerals",
            "🌰 Sunflower seeds: Vitamin E and minerals"
        ])

    # Infection/Inflammation natural remedies
    if any("infection" in finding or "wbc" in finding for finding in all_findings):
        prescriptions.extend([
            "🫚 Ginger tea: Natural anti-inflammatory",
            "🧄 Raw garlic: Natural antibiotic properties",
            "🍯 Manuka honey: Natural antibacterial",
            "🫚 Turmeric: Powerful anti-inflammatory",
            "🍋 Lemon water: Immune system booster"
        ])

    # General natural remedies
    prescriptions.extend([
        "🫚 Warm lemon water: Morning detox drink",
        "🌱 Green tea: Antioxidant-rich daily drink",
        "🍯 Honey and cinnamon: Natural health tonic",
        "🥥 Virgin coconut oil: Healthy fat source",
        "🫒 Extra virgin olive oil: Anti-inflammatory oil"
    ])

    # Add prescription suggestions based on common medical practices
    prescription_suggestions = []

    # Anemia prescription suggestions
    if any("anemia" in finding or "low hemoglobin" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Ferrous sulfate 325mg daily (standard iron supplement for iron deficiency anemia)",
            "💊 Ferrous gluconate 300mg twice daily (gentler on stomach than ferrous sulfate)",
            "💊 Vitamin B12 injections if pernicious anemia suspected (1000mcg monthly)",
            "💊 Folic acid 1mg daily if folate deficiency confirmed"
        ])

    # Diabetes prescription suggestions
    if any("diabetes" in finding or "glucose" in finding or "hba1c" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Metformin 500mg twice daily (first-line treatment for type 2 diabetes)",
            "💊 Glipizide 5mg daily (sulfonylurea for blood sugar control)",
            "💊 Sitagliptin 100mg daily (DPP-4 inhibitor for glycemic control)",
            "💊 Insulin glargine (long-acting insulin for type 1 or advanced type 2 diabetes)"
        ])

    # Cardiovascular prescription suggestions
    if any("cholesterol" in finding or "cardiovascular" in finding or "ldl" in finding or "hdl" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Atorvastatin 20mg daily (statin for LDL cholesterol reduction)",
            "💊 Rosuvastatin 10mg daily (potent statin for high cholesterol)",
            "💊 Ezetimibe 10mg daily (cholesterol absorption inhibitor)",
            "💊 Aspirin 81mg daily (antiplatelet therapy for cardiovascular protection)"
        ])

    # Thyroid prescription suggestions
    if any("thyroid" in finding or "tsh" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Levothyroxine 25-100mcg daily (thyroid hormone replacement for hypothyroidism)",
            "💊 Liothyronine 5mcg daily (T3 thyroid hormone if needed)",
            "💊 Methimazole 5-10mg daily (for hyperthyroidism treatment)",
            "💊 Propranolol 10mg as needed (for thyroid-related rapid heartbeat)"
        ])

    # Liver issues prescription suggestions
    if any("liver" in finding or "alt" in finding or "ast" in finding or "bilirubin" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Ursodeoxycholic acid 300mg twice daily (for cholestasis and liver protection)",
            "💊 Silymarin 150mg twice daily (milk thistle extract for liver support)",
            "💊 Vitamin E 400 IU daily (antioxidant for liver protection)",
            "💊 N-acetylcysteine 600mg twice daily (for acetaminophen overdose or liver support)"
        ])

    # Kidney issues prescription suggestions
    if any("kidney" in finding or "creatinine" in finding or "urea" in finding for finding in all_findings):
        prescription_suggestions.extend([
            "💊 Losartan 25mg daily (ACE inhibitor for kidney protection)",
            "💊 Amlodipine 5mg daily (calcium channel blocker for blood pressure control)",
            "💊 Furosemide 20mg daily (diuretic for fluid retention)",
            "💊 Calcium acetate 667mg with meals (phosphate binder for kidney disease)"
        ])

    # Add prescription section if there are suggestions
    if prescription_suggestions:
        prescriptions.append("")
        prescriptions.append("💊 PRESCRIPTION SUGGESTIONS (For Healthcare Professional Review Only):")
        prescriptions.extend(prescription_suggestions)

    # Disclaimer
    prescriptions.insert(0, "🌿 Natural Remedies by INBLOODO AGENT: These are AI-suggested natural remedies. Always consult with a qualified healthcare professional before starting any treatment.")
    prescriptions.insert(1, "⚠️ IMPORTANT: The prescription suggestions below are for informational purposes only and must be prescribed by a licensed healthcare professional after proper diagnosis.")

    return prescriptions


def generate_medicines(interpretation: list, risks: list, parameters: dict):
    """
    Generate structured medicine/medication suggestions based on findings.
    Separates supplements, OTC medicines, and prescription medications.
    IMPORTANT: All medicines must be prescribed/approved by healthcare professionals.
    """
    medicines = {
        "supplements": [],
        "otc_medicines": [],
        "prescription_medicines": [],
        "dietary_measures": []
    }

    all_findings = [f.lower() for f in interpretation + risks]

    # ANEMIA - Medicines and Supplements
    if any("anemia" in finding or "low hemoglobin" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Iron Supplements: Ferrous sulfate 325mg or Ferrous gluconate 300mg daily",
            "Vitamin B12 Supplements: 1000mcg daily (methylcobalamin or cyanocobalamin)",
            "Folic Acid: 1mg daily (important for red blood cell production)",
            "Vitamin C: 500mg daily (enhances iron absorption)"
        ])
        medicines["otc_medicines"].extend([
            "Iron-fortified cereals and foods",
            "Fortified orange juice (Vitamin C + Iron)"
        ])
        medicines["dietary_measures"].extend([
            "Red meat: 2-3 times per week (beef, lamb)",
            "Spinach and leafy greens: 1 cup daily",
            "Lentils and legumes: Several times per week",
            "Pumpkin seeds and nuts: Daily snack portion"
        ])

    # DIABETES - Medicines and Supplements
    if any("diabetes" in finding or "glucose" in finding or "hba1c" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Cinnamon Extract: 1-2g daily (may improve insulin sensitivity)",
            "Chromium: 100-200mcg daily (supports glucose metabolism)",
            "Alpha Lipoic Acid: 300-600mg daily (antioxidant for blood sugar control)",
            "Berberine: 500mg 2-3 times daily (alternative to metformin in some studies)"
        ])
        medicines["otc_medicines"].extend([
            "Bitter melon supplements: 50-100mg daily",
            "Fenugreek seeds: 5-10g soaked overnight",
            "Gymnema sylvestre: 300-400mg daily",
            "Diabetic-friendly food products"
        ])
        medicines["dietary_measures"].extend([
            "Low glycemic index foods",
            "High fiber foods: 25-30g daily",
            "Whole grains instead of refined carbs",
            "Beans and legumes: Several times per week"
        ])

    # HYPERTENSION/CARDIOVASCULAR - Medicines and Supplements
    if any("cholesterol" in finding or "cardiovascular" in finding or "ldl" in finding or "blood pressure" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "CoQ10: 100-300mg daily (heart health and statin support)",
            "Omega-3 Fish Oil: 1000-2000mg daily (EPA/DHA for heart health)",
            "Plant Sterols: 2g daily (proven to lower LDL cholesterol)",
            "Red Yeast Rice: 1200-2400mg daily (natural statin alternative)",
            "Aged Garlic Extract: 600-1200mg daily (cardiovascular support)"
        ])
        medicines["otc_medicines"].extend([
            "Aspirin: 81mg daily (consult doctor) - prevention of heart attacks",
            "Niacin (Vitamin B3): 1-2g daily (raises HDL, lowers LDL)",
            "Soluble fiber supplements: Oats, psyllium husk"
        ])
        medicines["dietary_measures"].extend([
            "Mediterranean diet pattern",
            "Fatty fish: Salmon, sardines 2-3 times per week",
            "Nuts and seeds: 30g daily (almonds, walnuts)",
            "Olive oil: 2 tablespoons daily for cooking",
            "Dark chocolate: 70% cocoa, 30g daily"
        ])

    # THYROID ISSUES - Medicines and Supplements
    if any("thyroid" in finding or "tsh" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Selenium: 200mcg daily (supports thyroid hormone conversion)",
            "Zinc: 15-25mg daily (essential for thyroid function)",
            "Iron: 18-27mg daily (deficiency impairs thyroid function)",
            "Ashwagandha: 600-900mg daily (adaptogen for thyroid health)",
            "L-Tyrosine: 500-1000mg daily (amino acid for thyroid hormones)"
        ])
        medicines["otc_medicines"].extend([
            "Kelp/Seaweed supplements: Iodine-rich (use cautiously)",
            "B Complex Vitamins: Daily multivitamin"
        ])
        medicines["dietary_measures"].extend([
            "Brazil nuts: 1-2 daily (selenium source)",
            "Seafood: Fish, shrimp 2 times per week (iodine)",
            "Eggs: 1-2 daily (selenium, iodine, zinc)",
            "Dairy products: Milk, yogurt (iodine, selenium)"
        ])

    # LIVER ISSUES - Medicines and Supplements
    if any("liver" in finding or "alt" in finding or "ast" in finding or "bilirubin" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Milk Thistle: 150-300mg 2-3 times daily (silymarin for liver protection)",
            "Vitamin E: 400 IU daily (antioxidant for hepatic cells)",
            "Vitamin C: 500-1000mg daily (liver antioxidant)",
            "Glutathione: 250-500mg daily (master antioxidant for liver)",
            "N-Acetyl Cysteine (NAC): 600-1200mg daily (liver detoxification)"
        ])
        medicines["otc_medicines"].extend([
            "Liver-support multivitamins",
            "Artichoke supplements: 300-600mg daily"
        ])
        medicines["dietary_measures"].extend([
            "Coffee: 3-4 cups daily (protective polyphenols)",
            "Cruciferous vegetables: Broccoli, cabbage, Brussels sprouts",
            "Ginger: Fresh or tea form 1-2 cups daily",
            "Turmeric: 500mg daily with black pepper (piperine)"
        ])

    # KIDNEY ISSUES - Medicines and Supplements
    if any("kidney" in finding or "creatinine" in finding or "urea" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Vitamin D: 1000-2000 IU daily (kidney protection)",
            "Omega-3 Fish Oil: 1000mg daily (renoprotective)",
            "Coenzyme Q10: 100-200mg daily (kidney support)",
            "Potassium restriction: Based on lab values (consult doctor)",
            "Phosphate binders: With meals if prescribed"
        ])
        medicines["otc_medicines"].extend([
            "Kidney-support multivitamins (low sodium)",
            "Sodium-free seasonings"
        ])
        medicines["dietary_measures"].extend([
            "Low sodium diet: <2300mg daily",
            "Adequate water intake: 2-3 liters daily (consult doctor)",
            "Low potassium foods: Apples, green beans, carrots",
            "Limited protein: Adjust based on kidney function"
        ])

    # IMMUNE SUPPORT/INFECTION - Medicines and Supplements
    if any("infection" in finding or "low wbc" in finding or "immune" in finding for finding in all_findings):
        medicines["supplements"].extend([
            "Vitamin C: 500-1000mg daily (immune support)",
            "Vitamin D: 1000-2000 IU daily (immune modulation)",
            "Zinc: 15-25mg daily (infection prevention)",
            "Elderberry: 500-1500mg daily (antiviral)",
            "Probiotics: Multi-strain, 10+ billion CFU daily"
        ])
        medicines["otc_medicines"].extend([
            "Garlic supplements: 600-1200mg daily (antimicrobial)",
            "Echinacea: 300-600mg 3 times daily (at symptom onset)",
            "Honey and ginger lozenges"
        ])
        medicines["dietary_measures"].extend([
            "Citrus fruits: Oranges, lemons, limes daily",
            "Garlic and onions: Daily in cooking",
            "Probiotics: Yogurt, kefir, sauerkraut",
            "Mushrooms: Shiitake, maitake (immune-boosting)"
        ])

    # GENERAL WELLNESS - Medicines and Supplements
    medicines["supplements"].extend([
        "Multivitamin: Daily (if dietary intake insufficient)",
        "Magnesium: 300-400mg daily (stress, muscle, heart health)",
        "Probiotics: 10+ billion CFU daily (gut health)",
        "Vitamin B Complex: Daily (energy, stress management)"
    ])

    medicines["otc_medicines"].extend([
        "Over-the-counter pain relievers: Only as needed (consult doctor)",
        "Antacids: For acid reflux (if needed)"
    ])

    # Add header
    medicines_list = [
        "💊 RECOMMENDED MEDICINES & SUPPLEMENTS by INBLOODO AI",
        "⚠️  IMPORTANT: All medicines must be prescribed or approved by a licensed healthcare professional.",
        "🔍 Dosages shown are typical; your doctor may adjust based on your specific condition.",
        ""
    ]

    # Add sections
    if medicines["supplements"]:
        medicines_list.append("📋 SUPPLEMENTS & VITAMINS:")
        medicines_list.extend([f"   • {m}" for m in medicines["supplements"]])
        medicines_list.append("")

    if medicines["otc_medicines"]:
        medicines_list.append("💊 OVER-THE-COUNTER OPTIONS:")
        medicines_list.extend([f"   • {m}" for m in medicines["otc_medicines"]])
        medicines_list.append("")

    if medicines["dietary_measures"]:
        medicines_list.append("🥗 DIETARY MEASURES:")
        medicines_list.extend([f"   • {m}" for m in medicines["dietary_measures"]])
        medicines_list.append("")

    medicines_list.extend([
        "📌 CONSULTATION REQUIRED:",
        "   • Discuss all supplements with your healthcare provider",
        "   • Some supplements may interact with medications",
        "   • Dosages should be personalized to your health profile",
        "   • Report all medications and supplements to your doctor"
    ])

    return medicines_list
