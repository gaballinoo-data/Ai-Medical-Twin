import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Medical Assistant | المساعد الطبي",
    page_icon="🏥",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    body { background-color: #0d1117; }
    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; }
    h1, h2, h3 { color: #00d4ff !important; }
    p, label { color: #cccccc !important; }
    .card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #161b22, #1f2937);
        border: 1px solid #00d4ff44;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .risk-high { color: #ff4444 !important; font-weight: bold; font-size: 20px; }
    .risk-medium { color: #ffaa00 !important; font-weight: bold; font-size: 20px; }
    .risk-low { color: #00cc88 !important; font-weight: bold; font-size: 20px; }
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0099bb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 30px;
        font-weight: bold;
        font-size: 16px;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0099bb, #006688);
    }
    .rtl { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# LANGUAGE SWITCHER
# =====================================================

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

col_lang1, col_lang2 = st.sidebar.columns(2)
with col_lang1:
    if st.button("🇬🇧 English"):
        st.session_state.lang = "EN"
with col_lang2:
    if st.button("🇪🇬 عربي"):
        st.session_state.lang = "AR"

lang = st.session_state.lang

# =====================================================
# TRANSLATIONS
# =====================================================

T = {
    "app_title":        {"EN": "🏥 AI Medical Assistant",                        "AR": "🏥 المساعد الطبي الذكي"},
    "app_subtitle":     {"EN": "Medical Data Analysis & Drug Intelligence System","AR": "نظام تحليل البيانات الطبية والأدوية"},
    "nav_title":        {"EN": "Navigation",                                      "AR": "القائمة"},
    "home":             {"EN": "🏠 Home",                                         "AR": "🏠 الرئيسية"},
    "drug_rec":         {"EN": "💊 Drug Recommendation",                          "AR": "💊 اقتراح الأدوية"},
    "side_effect":      {"EN": "⚠️ Side Effect Risk",                            "AR": "⚠️ مخاطر الأعراض الجانبية"},
    "hospital_map":     {"EN": "🗺️ Hospital Map Egypt",                          "AR": "🗺️ خريطة المستشفيات"},
    "ai_chat":          {"EN": "🤖 AI Chat Doctor",                               "AR": "🤖 الدكتور الذكي"},
    "dataset_stats":    {"EN": "📊 Dataset Stats",                                "AR": "📊 إحصائيات البيانات"},
    "total_drugs":      {"EN": "Total Drugs",                                     "AR": "إجمالي الأدوية"},
    "total_diseases":   {"EN": "Total Diseases",                                  "AR": "إجمالي الأمراض"},
    "total_se":         {"EN": "Total Side Effects",                              "AR": "إجمالي الأعراض الجانبية"},
    "records":          {"EN": "📋 Records",                                      "AR": "📋 السجلات"},
    "top_diseases":     {"EN": "🏆 Top 10 Diseases",                              "AR": "🏆 أكثر 10 أمراض"},
    "top_se_title":     {"EN": "⚠️ Top 10 Side Effects",                         "AR": "⚠️ أكثر 10 أعراض جانبية"},
    "disease_col":      {"EN": "Disease",                                         "AR": "المرض"},
    "drug_count_col":   {"EN": "Drug Count",                                      "AR": "عدد الأدوية"},
    "se_col":           {"EN": "Side Effect",                                     "AR": "العرض الجانبي"},
    "count_col":        {"EN": "Count",                                           "AR": "العدد"},
    "drug_rec_title":   {"EN": "💊 Drug Recommendation Engine",                   "AR": "💊 محرك اقتراح الأدوية"},
    "drug_rec_sub":     {"EN": "Select a disease to get recommended drugs",       "AR": "اختر مرضاً للحصول على الأدوية المناسبة"},
    "select_disease":   {"EN": "🔍 Select or Search Disease",                     "AR": "🔍 اختر أو ابحث عن مرض"},
    "get_drugs_btn":    {"EN": "Get Drug Recommendations",                        "AR": "احصل على الأدوية الموصى بها"},
    "found_drugs":      {"EN": "✅ Found {n} drugs for",                          "AR": "✅ تم العثور على {n} دواء لـ"},
    "no_drugs":         {"EN": "No drugs found for:",                             "AR": "لا توجد أدوية لـ:"},
    "se_title":         {"EN": "⚠️ Side Effect Risk Calculator",                  "AR": "⚠️ حاسبة مخاطر الأعراض الجانبية"},
    "se_sub":           {"EN": "Analyze the risk profile of any drug",            "AR": "تحليل مستوى خطورة أي دواء"},
    "select_drug":      {"EN": "💊 Select Drug",                                  "AR": "💊 اختر الدواء"},
    "calc_risk_btn":    {"EN": "Calculate Risk",                                  "AR": "احسب مستوى الخطورة"},
    "total_se_label":   {"EN": "Total Side Effects",                              "AR": "إجمالي الأعراض الجانبية"},
    "risk_level":       {"EN": "Risk Level",                                      "AR": "مستوى الخطورة"},
    "high_risk":        {"EN": "🔴 HIGH RISK",                                    "AR": "🔴 خطورة عالية"},
    "medium_risk":      {"EN": "🟡 MEDIUM RISK",                                  "AR": "🟡 خطورة متوسطة"},
    "low_risk":         {"EN": "🟢 LOW RISK",                                     "AR": "🟢 خطورة منخفضة"},
    "se_list":          {"EN": "📋 Side Effects List",                            "AR": "📋 قائمة الأعراض الجانبية"},
    "drug_not_found":   {"EN": "Drug not found",                                  "AR": "الدواء غير موجود"},
    "map_title":        {"EN": "🗺️ Hospital Map — Egypt",                        "AR": "🗺️ خريطة المستشفيات — مصر"},
    "map_sub":          {"EN": "Live data from OpenStreetMap",                    "AR": "بيانات مباشرة من OpenStreetMap"},
    "filter_disease":   {"EN": "🔍 Filter hospitals by disease specialty",        "AR": "🔍 فلتر المستشفيات حسب التخصص"},
    "show_all":         {"EN": "Show All Hospitals",                              "AR": "عرض كل المستشفيات"},
    "load_map_btn":     {"EN": "🗺️ Load Live Map",                               "AR": "🗺️ تحميل الخريطة"},
    "loading_map":      {"EN": "Loading hospitals from OpenStreetMap... ⏳",      "AR": "جاري تحميل المستشفيات... ⏳"},
    "total_facilities": {"EN": "🏥 Total Facilities",                             "AR": "🏥 إجمالي المنشآت"},
    "hospitals_label":  {"EN": "🏨 Hospitals",                                    "AR": "🏨 المستشفيات"},
    "clinics_label":    {"EN": "🩺 Clinics & Doctors",                            "AR": "🩺 العيادات والأطباء"},
    "recommended_for":  {"EN": "⭐ Recommended Hospitals for",                    "AR": "⭐ المستشفيات الموصى بها لـ"},
    "legend":           {"EN": "🔑 Map Legend",                                   "AR": "🔑 مفتاح الخريطة"},
    "legend_rec":       {"EN": "🔴 Recommended",                                  "AR": "🔴 موصى به"},
    "legend_hosp":      {"EN": "🔵 Hospital",                                     "AR": "🔵 مستشفى"},
    "legend_clinic":    {"EN": "🟢 Clinic/Doctor",                                "AR": "🟢 عيادة/طبيب"},
    "legend_health":    {"EN": "🟠 Health Post",                                  "AR": "🟠 وحدة صحية"},
    "facilities_list":  {"EN": "📋 Facilities List",                              "AR": "📋 قائمة المنشآت"},
    "press_load":       {"EN": "👆 Press **Load Live Map** to fetch real data",   "AR": "👆 اضغط **تحميل الخريطة** لجلب البيانات"},
    "osm_error":        {"EN": "Failed to load OSM data. Using backup data.",     "AR": "فشل تحميل بيانات OSM. يتم استخدام البيانات الاحتياطية."},
    "chat_title":       {"EN": "🤖 AI Chat Doctor",                               "AR": "🤖 الدكتور الذكي"},
    "chat_sub":         {"EN": "Ask about diseases, drugs, or symptoms",          "AR": "اسأل عن الأمراض والأدوية والأعراض"},
    "chat_input":       {"EN": "Ask about a disease or drug...",                  "AR": "اسأل عن مرض أو دواء..."},
    "chat_welcome":     {"EN": "👋 Hello! I'm your AI Medical Assistant. Ask me about any disease, drug, or symptom.", "AR": "👋 مرحباً! أنا مساعدك الطبي الذكي. اسألني عن أي مرض أو دواء أو عرض."},
    "chat_drugs_for":   {"EN": "💊 Recommended drugs for",                        "AR": "💊 الأدوية الموصى بها لـ"},
    "chat_se_for":      {"EN": "⚠️ Side effects of",                             "AR": "⚠️ الأعراض الجانبية لـ"},
    "chat_stats":       {"EN": "📊 Database Statistics:",                         "AR": "📊 إحصائيات قاعدة البيانات:"},
    "chat_top":         {"EN": "🏥 Top 5 Most Treated Diseases:",                 "AR": "🏥 أكثر 5 أمراض علاجاً:"},
    "chat_not_found":   {"EN": "🤔 Try asking:\n• What drugs treat hypertension?\n• Side effects of aspirin\n• How many drugs?\n• Top diseases", "AR": "🤔 جرب تسألني:\n• ما أدوية ارتفاع ضغط الدم؟\n• أعراض الأسبرين الجانبية\n• كم عدد الأدوية؟\n• أكثر الأمراض"},
    "name_col":         {"EN": "Name",                                            "AR": "الاسم"},
    "type_col":         {"EN": "Type",                                            "AR": "النوع"},
    "hosp_col":         {"EN": "Hospital",                                        "AR": "المستشفى"},
}

def t(key):
    return T[key][lang]


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    drug_names = pd.read_csv(r"C:\Users\MHGabAllah\Documents\AAA\project data\DEPI_Graduation\DEPI_Graduation\medical_project\drug_names.csv")
    meddra_indications = pd.read_csv(r"C:\Users\MHGabAllah\Documents\AAA\project data\DEPI_Graduation\DEPI_Graduation\medical_project\meddra_all_indications_2.csv")
    meddra_side_effects = pd.read_csv(r"C:\Users\MHGabAllah\Documents\AAA\project data\DEPI_Graduation\DEPI_Graduation\medical_project\meddra_side_effects.csv")
    meddra_freq = pd.read_csv(r"C:\Users\MHGabAllah\Documents\AAA\project data\DEPI_Graduation\DEPI_Graduation\medical_project\meddra_freq.csv")
    disease_symptoms = pd.read_csv(r"C:\Users\MHGabAllah\Documents\AAA\project data\DEPI_Graduation\DEPI_Graduation\medical_project\Disease and symptoms dataset.csv")
    drug_names["drug_name"] = drug_names["drug_name"].str.strip()
    meddra_indications["disease"] = meddra_indications["disease"].str.lower()
    meddra_side_effects["side_effect"] = meddra_side_effects["side_effect"].str.lower()
    return drug_names, meddra_indications, meddra_side_effects, meddra_freq, disease_symptoms

drug_names, meddra_indications, meddra_side_effects, meddra_freq, disease_symptoms = load_data()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown(f"## {t('app_title')}")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    t("nav_title"),
    [t("home"), t("drug_rec"), t("side_effect"), t("hospital_map"), t("ai_chat")]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{t('dataset_stats')}**")
st.sidebar.metric(t("total_drugs"), f"{drug_names.shape[0]:,}")
st.sidebar.metric(t("total_diseases"), f"{meddra_indications['disease'].nunique():,}")
st.sidebar.metric(t("total_se"), f"{meddra_side_effects['side_effect'].nunique():,}")


# =====================================================
# PAGE 1 : HOME
# =====================================================

if page == t("home"):

    if lang == "AR":
        st.markdown(f'<div class="rtl"><h1>{t("app_title")}</h1><h3>{t("app_subtitle")}</h3></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"# {t('app_title')}")
        st.markdown(f"### {t('app_subtitle')}")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"💊 {t('total_drugs')}", f"{drug_names.shape[0]:,}")
    with col2:
        st.metric(f"🏥 {t('total_diseases')}", f"{meddra_indications['disease'].nunique():,}")
    with col3:
        st.metric(f"⚠️ {t('total_se')}", f"{meddra_side_effects['side_effect'].nunique():,}")
    with col4:
        st.metric(t("records"), f"{meddra_side_effects.shape[0]:,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {t('top_diseases')}")
        top_diseases = meddra_indications["disease"].value_counts().head(10).reset_index()
        top_diseases.columns = [t("disease_col"), t("drug_count_col")]
        st.dataframe(top_diseases, use_container_width=True, hide_index=True)
    with col2:
        st.markdown(f"### {t('top_se_title')}")
        top_se = meddra_side_effects["side_effect"].value_counts().head(10).reset_index()
        top_se.columns = [t("se_col"), t("count_col")]
        st.dataframe(top_se, use_container_width=True, hide_index=True)


# =====================================================
# PAGE 2 : DRUG RECOMMENDATION
# =====================================================

elif page == t("drug_rec"):

    if lang == "AR":
        st.markdown(f'<div class="rtl"><h1>{t("drug_rec_title")}</h1><p>{t("drug_rec_sub")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"# {t('drug_rec_title')}")
        st.markdown(t("drug_rec_sub"))

    st.markdown("---")

    all_diseases = sorted(meddra_indications["disease"].unique().tolist())
    disease_input = st.selectbox(t("select_disease"), all_diseases)

    if st.button(t("get_drugs_btn")):
        drugs = meddra_indications[meddra_indications["disease"] == disease_input]
        merged = drugs.merge(drug_names, on="drug_id", how="left")
        result = merged["drug_name"].dropna().unique()

        if len(result) == 0:
            st.warning(f"{t('no_drugs')} {disease_input}")
        else:
            msg = t("found_drugs").replace("{n}", str(len(result)))
            st.success(f"{msg} **{disease_input}**")
            cols = st.columns(3)
            for i, drug in enumerate(result[:12]):
                with cols[i % 3]:
                    st.markdown(f'<div class="card"><h4 style="color:#00d4ff">💊 {drug}</h4></div>', unsafe_allow_html=True)


# =====================================================
# PAGE 3 : SIDE EFFECT RISK
# =====================================================

elif page == t("side_effect"):

    if lang == "AR":
        st.markdown(f'<div class="rtl"><h1>{t("se_title")}</h1><p>{t("se_sub")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"# {t('se_title')}")
        st.markdown(t("se_sub"))

    st.markdown("---")

    all_drugs = sorted(drug_names["drug_name"].dropna().unique().tolist())
    drug_input = st.selectbox(t("select_drug"), all_drugs)

    if st.button(t("calc_risk_btn")):
        drug_id_row = drug_names[drug_names["drug_name"] == drug_input]
        if drug_id_row.empty:
            st.warning(t("drug_not_found"))
        else:
            drug_id = drug_id_row["drug_id"].iloc[0]
            effects = meddra_side_effects[meddra_side_effects["drug_id"] == drug_id]["side_effect"].dropna().unique()
            total = len(effects)

            if total > 20:
                risk, risk_class = t("high_risk"), "risk-high"
            elif total > 10:
                risk, risk_class = t("medium_risk"), "risk-medium"
            else:
                risk, risk_class = t("low_risk"), "risk-low"

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="metric-card"><h3>{t("total_se_label")}</h3><h1 style="color:#00d4ff">{total}</h1></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h3>{t("risk_level")}</h3><p class="{risk_class}">{risk}</p></div>', unsafe_allow_html=True)

            st.markdown(f"### {t('se_list')}")
            st.dataframe(pd.DataFrame({t("se_col"): effects}), use_container_width=True, hide_index=True)


# =====================================================
# PAGE 4 : HOSPITAL MAP
# =====================================================

elif page == t("hospital_map"):

    if lang == "AR":
        st.markdown(f'<div class="rtl"><h1>{t("map_title")}</h1><p>{t("map_sub")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"# {t('map_title')}")
        st.markdown(t("map_sub"))

    st.markdown("---")

    import osmnx as ox

    specialty_map = {
        "cardiology":        ["heart", "cardiac", "cardiovascular", "hypertension", "angina"],
        "oncology":          ["cancer", "tumor", "lymphoma", "leukemia", "carcinoma"],
        "neurology":         ["brain", "stroke", "epilepsy", "migraine", "alzheimer"],
        "orthopedics":       ["bone", "fracture", "arthritis", "spine", "joint"],
        "pediatrics":        ["child", "infant", "pediatric", "neonatal"],
        "gynecology":        ["pregnancy", "uterus", "ovarian", "cervical"],
        "pulmonology":       ["lung", "asthma", "pneumonia", "bronchitis"],
        "gastroenterology":  ["stomach", "liver", "intestine", "colon", "hepatitis"],
        "urology":           ["kidney", "bladder", "prostate", "urinary"],
        "endocrinology":     ["diabetes", "thyroid", "hormone", "obesity"],
        "general":           ["infection", "fever", "fatigue", "pain"],
    }

    hospitals_with_specialty = {
        "Kasr Al Ainy Hospital":           ["cardiology", "oncology", "neurology", "general"],
        "Ain Shams University Hospital":   ["cardiology", "pediatrics", "neurology", "general"],
        "El Demerdash Hospital":           ["oncology", "gastroenterology", "general"],
        "Dar Al Fouad Hospital":           ["cardiology", "orthopedics", "general"],
        "Cleopatra Hospital":              ["gynecology", "pediatrics", "general"],
        "As-Salam International Hospital": ["cardiology", "oncology", "general"],
        "Alexandria University Hospital":  ["neurology", "oncology", "general"],
        "Mansoura University Hospital":    ["urology", "general"],
        "National Cancer Institute":       ["oncology"],
        "Maadi Military Hospital":         ["general", "orthopedics"],
    }

    @st.cache_data(show_spinner=False)
    def load_hospitals_osm():
        try:
            tags = {'amenity': ['hospital', 'clinic', 'doctors', 'health_post']}
            gdf = ox.features_from_place("Egypt", tags=tags)
            gdf = gdf[gdf.geometry.geom_type == 'Point'].copy()
            gdf["lat"] = gdf.geometry.y
            gdf["lon"] = gdf.geometry.x
            gdf["name"] = gdf.get("name", "Unknown")
            gdf["amenity_type"] = gdf.get("amenity", "hospital")
            result = gdf[["name", "lat", "lon", "amenity_type"]].dropna(subset=["lat", "lon"])
            result = result[result["name"] != "Unknown"]
            return result.reset_index(drop=True)
        except:
            return None

    all_diseases_map = sorted(meddra_indications["disease"].unique().tolist())
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_disease_map = st.selectbox(t("filter_disease"), [t("show_all")] + all_diseases_map)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button(t("load_map_btn"))

    if load_btn or "hospitals_df" in st.session_state:
        if "hospitals_df" not in st.session_state:
            with st.spinner(t("loading_map")):
                df = load_hospitals_osm()
                if df is not None:
                    st.session_state.hospitals_df = df
                else:
                    st.error(t("osm_error"))
                    st.session_state.hospitals_df = pd.DataFrame([
                        {"name": "Kasr Al Ainy Hospital",          "lat": 30.0356, "lon": 31.2294, "amenity_type": "hospital"},
                        {"name": "Ain Shams University Hospital",  "lat": 30.0776, "lon": 31.2797, "amenity_type": "hospital"},
                        {"name": "Dar Al Fouad Hospital",          "lat": 30.0131, "lon": 31.1958, "amenity_type": "hospital"},
                        {"name": "Cleopatra Hospital",             "lat": 30.0784, "lon": 31.3366, "amenity_type": "hospital"},
                        {"name": "Alexandria University Hospital", "lat": 31.1991, "lon": 29.9058, "amenity_type": "hospital"},
                        {"name": "Mansoura University Hospital",   "lat": 31.0364, "lon": 31.3807, "amenity_type": "hospital"},
                        {"name": "Assiut University Hospital",     "lat": 27.1824, "lon": 31.1837, "amenity_type": "hospital"},
                        {"name": "Tanta University Hospital",      "lat": 30.7865, "lon": 30.9980, "amenity_type": "hospital"},
                        {"name": "Aswan University Hospital",      "lat": 24.0889, "lon": 32.8998, "amenity_type": "hospital"},
                        {"name": "Suez Canal University Hospital", "lat": 30.5965, "lon": 32.2715, "amenity_type": "hospital"},
                    ])

        hospitals_df = st.session_state.hospitals_df

        recommended_hospitals = []
        if selected_disease_map != t("show_all"):
            matched_specialties = []
            for specialty, keywords in specialty_map.items():
                if any(kw in selected_disease_map for kw in keywords):
                    matched_specialties.append(specialty)
            if not matched_specialties:
                matched_specialties = ["general"]
            for hosp_name, specialties in hospitals_with_specialty.items():
                if any(s in matched_specialties for s in specialties):
                    recommended_hospitals.append(hosp_name)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t("total_facilities"), f"{len(hospitals_df):,}")
        with col2:
            amenity_counts = hospitals_df["amenity_type"].value_counts()
            st.metric(t("hospitals_label"), f"{amenity_counts.get('hospital', 0):,}")
        with col3:
            clinics = amenity_counts.get("clinic", 0) + amenity_counts.get("doctors", 0)
            st.metric(t("clinics_label"), f"{clinics:,}")

        m = folium.Map(location=[26.8206, 30.8025], zoom_start=6, tiles="CartoDB dark_matter")
        for _, row in hospitals_df.iterrows():
            name = str(row["name"]) if pd.notna(row["name"]) else "Unknown"
            amenity = str(row["amenity_type"]) if pd.notna(row["amenity_type"]) else "hospital"
            is_recommended = name in recommended_hospitals
            if is_recommended:
                color, icon = "red", "star"
            elif amenity == "hospital":
                color, icon = "blue", "plus-sign"
            elif amenity in ["clinic", "doctors"]:
                color, icon = "green", "heart"
            else:
                color, icon = "orange", "info-sign"
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(f"<b>{name}</b><br>{amenity}<br>{'⭐ ' + selected_disease_map if is_recommended else ''}", max_width=250),
                tooltip=name,
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(m)

        st_folium(m, width=1200, height=600)

        if recommended_hospitals and selected_disease_map != t("show_all"):
            st.markdown(f"### {t('recommended_for')} **{selected_disease_map}**")
            st.dataframe(pd.DataFrame({t("hosp_col"): recommended_hospitals}), use_container_width=True, hide_index=True)

        st.markdown(f"### {t('legend')}")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"**{t('legend_rec')}**")
        with col2: st.markdown(f"**{t('legend_hosp')}**")
        with col3: st.markdown(f"**{t('legend_clinic')}**")
        with col4: st.markdown(f"**{t('legend_health')}**")

        st.markdown(f"### {t('facilities_list')}")
        st.dataframe(
            hospitals_df[["name", "amenity_type"]].head(100).rename(columns={"name": t("name_col"), "amenity_type": t("type_col")}),
            use_container_width=True, hide_index=True
        )
    else:
        st.info(t("press_load"))


# =====================================================
# PAGE 5 : AI CHAT DOCTOR
# =====================================================

elif page == t("ai_chat"):

    if lang == "AR":
        st.markdown(f'<div class="rtl"><h1>{t("chat_title")}</h1><p>{t("chat_sub")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"# {t('chat_title')}")
        st.markdown(t("chat_sub"))

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": t("chat_welcome")}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input(t("chat_input"))

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        query = user_input.lower()
        response = ""

        matched_disease = None
        for disease in meddra_indications["disease"].unique():
            if disease in query:
                matched_disease = disease
                break

        if matched_disease:
            drugs = meddra_indications[meddra_indications["disease"] == matched_disease]
            merged = drugs.merge(drug_names, on="drug_id", how="left")
            drug_list = merged["drug_name"].dropna().unique()[:8]
            response = f"**{t('chat_drugs_for')} {matched_disease}:**\n\n"
            for d in drug_list:
                response += f"• {d}\n"

        elif any(w in query for w in ["side effect", "risk", "عرض", "أعراض", "خطر"]):
            for drug in drug_names["drug_name"].dropna().unique():
                if drug.lower() in query:
                    drug_id = drug_names[drug_names["drug_name"] == drug]["drug_id"].iloc[0]
                    effects = meddra_side_effects[meddra_side_effects["drug_id"] == drug_id]["side_effect"].unique()[:8]
                    response = f"**{t('chat_se_for')} {drug}:**\n\n"
                    for e in effects:
                        response += f"• {e}\n"
                    break

        elif any(w in query for w in ["how many", "total", "كم", "عدد", "إجمالي"]):
            response = f"**{t('chat_stats')}**\n"
            response += f"• {t('total_drugs')}: {drug_names.shape[0]:,}\n"
            response += f"• {t('total_diseases')}: {meddra_indications['disease'].nunique():,}\n"
            response += f"• {t('total_se')}: {meddra_side_effects['side_effect'].nunique():,}\n"

        elif any(w in query for w in ["top", "أكثر", "common"]):
            top = meddra_indications["disease"].value_counts().head(5)
            response = f"**{t('chat_top')}**\n\n"
            for disease, count in top.items():
                response += f"• {disease}: {count}\n"

        else:
            response = t("chat_not_found")

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
