"""
Dashboard Desa Silurah — SDG 11 Digital Mapping Project
Custom high-end UI built on top of Streamlit primitives.
"""

import base64
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Desa Silurah | Peta Digital Desa",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# LANGUAGE SWITCHER (PENGATUR BAHASA)
# --------------------------------------------------------------------------
col_space, col_lang = st.columns([8.5, 1.5])
with col_lang:
    lang_choice = st.radio(
        "Bahasa",
        ["🇮🇩 ID", "🇬🇧 EN"],
        horizontal=True,
        label_visibility="collapsed",
        key="language_selector",
    )

is_eng = lang_choice == "🇬🇧 EN"

def tr(id_text, en_text):
    return en_text if is_eng else id_text

# --------------------------------------------------------------------------
# ASSET HELPERS
# --------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"
HERO_IMAGE_PATH = ASSETS_DIR / "foto_desa.jpg"


@st.cache_data(show_spinner=False)
def get_base64_image(path: Path):
    """Encode a local image to base64 for CSS background-image use."""
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return None


hero_b64 = get_base64_image(HERO_IMAGE_PATH)

if hero_b64:
    hero_bg_css = f"url('data:image/jpg;base64,{hero_b64}')"
else:
    hero_bg_css = (
        "linear-gradient(135deg, #3E5C48 0%, #2C4C3B 45%, #4A3525 100%)"
    )

# --------------------------------------------------------------------------
# DATA
# --------------------------------------------------------------------------
STATS = [
    {"label": tr("Destinasi Wisata", "Tourist Destinations"), "value": "7", "icon": "🏞️", "anchor": "info-wisata"},
    {"label": tr("Dusun Wilayah", "Hamlets"), "value": "6", "icon": "🏘️", "anchor": "info-dusun"},
    {"label": tr("Sekolah", "Schools"), "value": "5", "icon": "🏫", "anchor": "info-sekolah"},
    {"label": tr("Posyandu", "Healthcare Centers"), "value": "5", "icon": "🩺", "anchor": "info-posyandu"},
]

WISATA_DATA = [
    {
        "nama": "Curug Bidadari",
        "desc": tr(
            "Air terjun alami dengan pemandangan pegunungan yang asri dan udara sejuk.",
            "Explore the beauty of a hidden waterfall flowing from pure mountain springs."
        ),
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari_EN.jpg')}",
        "lat": -7.08135339729419, "lon": 109.75483311219776,
        "link_maps": "https://maps.app.goo.gl/CncoFsTgcREPtZXd7",
    },
    {
        "nama": "Curug Kalirogno",
        "desc": tr(
            "Destinasi air terjun tersembunyi dengan aliran sungai jernih dan kolam alami.",
            "A hidden waterfall destination with clear stream flows and a natural pool."
        ),
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno_EN.jpg')}",
        "lat": -7.1185, "lon": 109.8680,
        "link_maps": "https://maps.app.goo.gl/CncoFsTgcREPtZXd7",
    },
    {
        "nama": "Taman Syailendra",
        "desc": tr(
            "Kawasan taman wisata alam dan edukasi dengan lanskap pegunungan yang menawan.",
            "An educational nature park area with charming mountain landscapes."
        ),      
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra_EN.jpg')}",
        "lat": -7.083100470745881, "lon": 109.77427505676775,
        "link_maps": "https://maps.app.goo.gl/9TAwJFkZ1qjrwEB8A",
    },
    {
        "nama": "Situs Punden Berundak",
        "desc": tr(
            "Situs cagar budaya prasejarah megalitikum peninggalan leluhur desa.",
            "A megalithic prehistoric cultural heritage site from the village ancestors."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak_EN.jpg')}",
        "dusun": "Dusun Batur", 
        "lat": -7.085509531467704, "lon": 109.76952706821783,
        "link_maps": "https://maps.app.goo.gl/Lz3ryLVuD4LwWt4GA",
    },
    {
        "nama": "Arca Ganesha",
        "desc": tr(
            "Situs arca kuno peninggalan era sejarah klasik di Desa Silurah.",
            "An ancient statue site from the classical historical era in Silurah Village."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha_EN.jpg')}",
        "lat": -7.077144063062202, "lon": 109.7575725307554,
        "link_maps": "https://maps.app.goo.gl/Mkh1fp25AHCmWLPq5",
    },
    {
        "nama": "Gunung Kobar",
        "desc": tr(
            "Spot dataran tinggi favorit untuk menikmati sunrise dan lautan kabut pagi.",
            "A favorite highland spot to enjoy the sunrise and morning sea of fog."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar_EN.jpg')}",
        "lat": -7.109675292850821, "lon": 109.76024696252469,
        "link_maps": "https://maps.app.goo.gl/oy7aev5VSkBiaVqZ7",
    },
]

MAP_POINTS = pd.DataFrame(
    {
        "lat": -7.1123 + np.random.randn(18) * 0.004,
        "lon": 109.8654 + np.random.randn(18) * 0.004,
    }
)

POPULATION_DATA = pd.DataFrame(
    {
        "Dusun": ["Krajan", "Batur", "Sipudang", "Simangli", "Pomahan", "Pomahan"],
        "Laki-laki": [1, 1, 1, 1, 1, 1],
        "Perempuan": [1, 1, 1, 1, 1, 1],
    }
).set_index("Dusun")

AGE_DATA = pd.DataFrame(
    {
        "Kelompok Usia": ["0-14", "15-24", "25-54", "55-64", "65+"],
        "Jumlah Jiwa": [820, 615, 1740, 430, 260],
    }
).set_index("Kelompok Usia")

LAND_USE_DATA = pd.DataFrame(
    {
        "Penggunaan Lahan": ["Pemukiman", "Persawahan", "Perkebunan", "Kuburan", "Pekarangan", "Perkantoran", "Prasarana Umum"],
        "Luas (Ha)": [0.51, 36.00, 67.98, 2.00, 25.00, 0.29, 8.31],
    }
).set_index("Penggunaan Lahan")

# --------------------------------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

    <style>
    :root{
        --primary:#2C4C3B;
        --primary-light:#3E5C48;
        --secondary:#4A3525;
        --bg:#FAF9F5;
        --card-bg:#FFFFFF;
        --text-dark:#22281F;
        --text-muted:#6B6459;
        --border-soft:#E9E4D8;
    }

    html, body, [class*="css"]{
        font-family:'Inter', sans-serif;
        color:var(--text-dark);
        scroll-behavior: smooth;
        overflow-x: hidden !important;
    }

    .stApp{
        background:var(--bg);
        overflow-x: hidden !important;
    }

    #MainMenu, footer, [data-testid="stToolbar"], header[data-testid="stHeader"], div[data-testid="stDecoration"] {
        display: none !important;
        pointer-events: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
    }

    .block-container{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.hero-anchor){
        margin-top: -1rem;
    }

    h1, h2, h3, h4{
        font-family:'Plus Jakarta Sans', sans-serif;
        color:var(--text-dark);
        font-weight:700;
    }

    .stTabs [data-baseweb="tab-list"]{
        gap:6px;
        background:var(--card-bg);
        padding:0.6rem 2.5rem 0rem 2.5rem;
        border-bottom:1px solid var(--border-soft);
        position:sticky;
        top:0;
        z-index:9999 !important;
    }

    .stTabs [data-baseweb="tab"]{
        height:46px;
        white-space:pre-wrap;
        border-radius:8px 8px 0 0;
        padding:0px 20px;
        font-family:'Plus Jakarta Sans', sans-serif;
        font-weight:600;
        font-size:0.95rem;
        color:var(--text-muted);
        background:transparent;
        border:none;
        transition:all 0.2s ease;
        cursor:pointer !important;
        pointer-events: auto !important;
    }

    .stTabs [data-baseweb="tab"]:hover{
        color:var(--primary);
        background:rgba(44,76,59,0.06);
    }

    .stTabs [aria-selected="true"]{
        color:var(--primary) !important;
        background:rgba(44,76,59,0.08) !important;
        border-bottom:3px solid var(--primary) !important;
    }

    .stTabs [data-baseweb="tab-highlight"]{
        background-color:var(--primary);
    }

    .stTabs [data-baseweb="tab-panel"]{
        padding-top:0rem;
    }

    .hero-anchor{height:0;}

    .hero-banner{
        position: relative !important;
        width: 100vw !important;
        left: 50% !important;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        height: 420px;
        margin-top: -1.5rem !important;
        background-image: __HERO_BG__;
        background-size: cover;
        background-position: center;
        -webkit-mask-image: linear-gradient(to bottom, black 62%, transparent 100%);
        mask-image: linear-gradient(to bottom, black 62%, transparent 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-overlay{
        position:absolute;
        inset:0;
        background:linear-gradient(180deg, rgba(20,30,22,0.55) 0%, rgba(20,30,22,0.72) 55%, rgba(20,30,22,0.9) 100%);
    }

    .hero-content{
        position:relative;
        z-index:2;
        text-align:center;
        color:#FFFFFF;
        padding:0 1rem;
    }

    .hero-eyebrow{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-size:0.8rem;
        font-weight:600;
        letter-spacing:0.22em;
        text-transform:uppercase;
        color:#D8CBB2;
        margin-bottom:0.9rem;
    }

    .hero-content h1{
        font-size:3.6rem;
        font-weight:800;
        color:#FFFFFF;
        margin:0;
        letter-spacing:-0.01em;
        text-shadow:0 2px 18px rgba(0,0,0,0.25);
    }

    .hero-content p{
        font-size:1.08rem;
        color:#EDE7D9;
        max-width:560px;
        margin:0.9rem auto 0 auto;
        line-height:1.6;
        font-weight:400;
    }

    .stat-card-container {
        max-width: 1180px;
        margin: -50px auto 1.5rem auto;
        padding: 0 2.5rem;
        position: relative;
        z-index: 10;
    }

    .stat-card{
        background:var(--card-bg);
        border-top:4px solid var(--primary);
        border-radius:12px;
        box-shadow:0 10px 25px rgba(0, 0, 0, 0.08);
        padding:1.5rem 1.2rem;
        text-align:center;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        transition:transform 0.22s ease, box-shadow 0.22s ease;
        width: 100%;
        margin-bottom: 10px;
        cursor: pointer;
    }

    .stat-card:hover{
        transform:translateY(-5px);
        box-shadow:0 15px 30px rgba(0, 0, 0, 0.15);
        border-top:4px solid var(--secondary);
    }

    .stat-icon{font-size:1.8rem; margin-bottom:0.4rem; display:block;}

    .stat-value{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-size:2rem;
        font-weight:800;
        color:var(--secondary);
        line-height:1;
    }

    .stat-label{
        font-size:0.85rem;
        color:var(--text-muted);
        margin-top:0.4rem;
        font-weight:600;
    }

    .section{
        max-width: 100% !important;
        margin: 2.5rem 0 1rem 0 !important;
        padding: 0 !important;
    }

    .section-eyebrow{
        font-size:0.78rem;
        font-weight:700;
        letter-spacing:0.16em;
        text-transform:uppercase;
        color:var(--primary);
        margin-bottom:0.4rem;
    }

    .section-title{
        font-size:1.7rem;
        font-weight:700;
        margin-bottom:0.6rem;
    }

    .section-body{
        color:var(--text-muted);
        font-size:0.98rem;
        line-height:1.7;
        max-width: 100% !important;
    }

    .wisata-card {
        background: var(--card-bg);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border: 1px solid var(--border-soft);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        margin: 10px 0px 25px 0px !important;
    }

    .wisata-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    .wisata-img-wrapper {
        width: 100%;
        height: 200px;
        overflow: hidden;
        position: relative;
        background: #E9E4D8;
    }

    .wisata-img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .wisata-card:hover .wisata-img-wrapper img {
        transform: scale(1.05);
    }

    .wisata-content {
        padding: 1.2rem;
        flex-grow: 1;
    }

    .wisata-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text-dark);
        margin-bottom: 0.4rem;
    }

    .wisata-desc {
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    .feature-grid{
        display:grid;
        grid-template-columns:repeat(3, 1fr);
        gap:1.2rem;
        margin-top:1.6rem;
    }

    .feature-card{
        background:var(--card-bg);
        border:1px solid var(--border-soft);
        border-radius:12px;
        padding:1.4rem;
        transition:box-shadow 0.2s ease, transform 0.2s ease;
    }

    .feature-card:hover{
        box-shadow:0 12px 26px rgba(30,40,25,0.1);
        transform:translateY(-3px);
    }

    .feature-card h4{
        color:var(--secondary);
        font-size:1.02rem;
        margin-bottom:0.4rem;
    }

    .feature-card p{
        color:var(--text-muted);
        font-size:0.88rem;
        line-height:1.6;
        margin:0;
    }

    .panel{
        background:var(--card-bg);
        border:1px solid var(--border-soft);
        border-radius:12px;
        padding:1.6rem 1.8rem;
        box-shadow:0 6px 18px rgba(30,40,25,0.05);
    }

    .panel-title{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-weight:700;
        font-size:1.05rem;
        color:var(--secondary);
        margin-bottom:0.9rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"]{
        border-radius:12px;
    }

    @media (max-width:900px){
        .stat-card-container {
            margin-top: -30px;
            padding: 0 1.5rem;
        }
        .feature-grid{grid-template-columns:repeat(1, 1fr);}
        .hero-content h1{font-size:2.4rem;}
    }
    </style>
    """.replace("__HERO_BG__", hero_bg_css),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# NAVIGATION
# --------------------------------------------------------------------------
tab_beranda, tab_peta, tab_wisata, tab_statistik = st.tabs([
    tr("Beranda", "Home"),
    tr("Peta Digital", "Digital Map"),
    tr("Destinasi Wisata", "Destinations"),
    tr("Statistik", "Statistics")
])

# --------------------------------------------------------------------------
# TAB 1 — BERANDA
# --------------------------------------------------------------------------
with tab_beranda:
    st.markdown('<div class="hero-anchor"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-eyebrow">Kecamatan Wonotunggal · Kabupaten Batang</div>
                <h1>Desa Silurah</h1>
                <p>Peta digital dan basis data desa untuk mendukung perencanaan
                pembangunan berkelanjutan, selaras dengan SDG 11 — Kota dan
                Permukiman yang Berkelanjutan.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="stat-card-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, s in zip(cols, STATS):
        with col:
            st.markdown(
                f"""
                <a href="#{s['anchor']}" style="text-decoration: none; color: inherit;">
                    <div class="stat-card">
                        <span class="stat-icon">{s['icon']}</span>
                        <div class="stat-value">{s['value']}</div>
                        <div class="stat-label">{s['label']}</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section">
            <div class="section-eyebrow">{tr("Tentang Desa", "About the Village")}</div>
            <div class="section-title">{tr("Selayang Pandang Desa Silurah", "Overview of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Tersembunyi di balik sejuknya perbukitan Wonotunggal, Desa Silurah bernapas melalui suburnya lahan agrowisata dan perkebunan yang menjadi urat nadi warganya. Dashboard interaktif ini hadir sebagai jendela digital untuk memetakan potensi desa, membuka transparansi data, dan menjadi pijakan pembangunan berkelanjutan berbasis bukti nyata.",
                    "Hidden behind the cool hills of Wonotunggal, Silurah Village thrives through its fertile agrotourism lands and plantations that serve as the lifeblood of its citizens. This interactive dashboard serves as a digital window to map village potentials, open data transparency, and become a foundation for evidence-based sustainable development."
                )}
            </p>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🗺️ {tr("Pemetaan Spasial", "Spatial Mapping")}</h4>
                    <p>{tr(
                        "Sebaran fasilitas umum, batas dusun, dan titik potensi wisata terdokumentasi secara digital dan dapat diakses publik.",
                        "The distribution of public facilities, hamlet boundaries, and tourism potential points are digitally documented and publicly accessible."
                    )}</p>
                </div>
                <div class="feature-card">
                    <h4>📊 {tr("Data Kependudukan", "Demographic Data")}</h4>
                    <p>{tr(
                        "Statistik demografi diperbarui secara berkala untuk mendukung perencanaan program desa yang tepat sasaran.",
                        "Demographic statistics are regularly updated to support targeted village program planning."
                    )}</p>
                </div>
                <div class="feature-card">
                    <h4>🌱 {tr("Keberlanjutan", "Sustainability")}</h4>
                    <p>{tr(
                        "Mendukung pencapaian SDG 11 melalui data terbuka yang mendorong pembangunan permukiman yang inklusif dan aman.",
                        "Supporting the achievement of SDG 11 through open data that encourages the development of inclusive and safe human settlements."
                    )}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # =========================================================================
    # SECTION 1: DESTINASI WISATA
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-wisata" class="section" style="margin-bottom: 1rem;">
            <div class="section-eyebrow">🏞️ {tr("Destinasi Wisata", "Tourist Destinations")}</div>
            <div class="section-title">{tr("Potensi Wisata Desa Silurah", "Tourism Potential of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Sekilas potensi wisata unggulan Desa Silurah. Untuk melihat informasi lengkap, fasilitas, dan peta lokasi interaktif, silakan buka tab <b>Destinasi Wisata</b> di menu atas.",
                    "An overview of Silurah Village's prime tourism potential. To view complete information, facilities, and interactive location maps, please open the <b>Destinations</b> tab in the top menu."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i in range(0, len(WISATA_DATA), 3):
        wisata_cols = st.columns(3)
        row_data = WISATA_DATA[i : i + 3]

        for col, w in zip(wisata_cols, row_data):
            with col:
                st.markdown(
                    f"""
                    <div class="wisata-card">
                        <div class="wisata-img-wrapper">
                            <img src="{w['img']}" alt="{w['nama']}">
                        </div>
                        <div class="wisata-content">
                            <div class="wisata-title">{w['nama']}</div>
                            <p class="wisata-desc">{w['desc']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =========================================================================
    # SECTION 2: DUSUN
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-dusun" class="section" style="margin-top: 4rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">🏘️ {tr("Wilayah Administratif", "Administrative Area")}</div>
            <div class="section-title">{tr("Daftar Dusun di Desa Silurah", "List of Hamlets in Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Jelajahi denyut kehidupan masyarakat di enam dusun yang tersebar melintasi kontur perbukitan Silurah. Saling terhubung oleh urat nadi jalan desa, setiap dusun memegang peran penting dalam menjaga kerukunan warga, tradisi leluhur, dan roda perekonomian lokal.",
                    "Explore the heartbeat of community life across six hamlets spread across the hilly contours of Silurah. Interconnected by village roads, each hamlet plays an essential role in maintaining community harmony, ancestral traditions, and the local economy."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        dusun_df = pd.DataFrame({
            tr("Nama Dusun", "Hamlet Name"): [
                tr("Dusun Krajan", "Dusun Krajan"),
                tr("Dusun Batur", "Dusun Batur"),
                tr("Dusun Sipudang", "Dusun Sipudang"),
                tr("Dusun Simangli", "Dusun Simangli"),
                tr("Dusun Pomahan", "Dusun Pomahan"),
                tr("Dusun Pedati", "Dusun Pedati")
            ],
            tr("Kepala Dusun", "Hamlet Head"): [
                "-", "-", "-", 
                tr("Bpk. Sutari", "Mr. Sutari"), 
                tr("Bpk. Dwi Kurniawan", "Mr. Dwi Kurniawan"), 
                tr("Bpk. Wanudin", "Mr. Wanudin")
            ],
            tr("Jumlah RT/RW", "RT/RW Count"): ["2 RT / 1 RW", "1 RT / 1 RW", "1 RT / 0 RW", "2 RT / 1 RW", "2 RT / 1 RW", "2 RT / 1 RW"],
        })
        st.dataframe(dusun_df, use_container_width=True, hide_index=True)

    # BATAS WILAYAH
    st.markdown(
        f"""
        <div id="info-batas-wilayah" class="section" style="margin-top: 1rem; margin-bottom: 1rem;">
            <div class="section-title">{tr("Batas Wilayah Desa Silurah", "Regional Boundaries of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Menempati posisi strategis di ketinggian Kabupaten Batang, Desa Silurah menjadi titik simpul yang berbatasan langsung dengan empat kecamatan berbeda. Letak geografis ini menjadikannya kawasan yang kaya akan interaksi sosial, budaya, dan mobilitas ekonomi antarwilayah.",
                    "Occupying a strategic position in the highlands of Batang Regency, Silurah Village serves as a connecting hub bordered directly by four different sub-districts. This geographical location makes it an area rich in social, cultural interaction, and inter-regional economic mobility."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        batas_df = pd.DataFrame({
            tr("Arah", "Direction"): [
                tr("Utara", "North"), 
                tr("Selatan", "South"), 
                tr("Timur", "East"), 
                tr("Barat", "West")
            ],
            tr("Desa / Kecamatan Border", "Bordering Village / Sub-district"): [
                tr("Desa Sodong, Kecamatan Wonotunggal", "Sodong Village, Wonotunggal Sub-district"),
                tr("Desa Klindon, Kecamatan Petungkriyono", "Klindon Village, Petungkriyono Sub-district"),
                tr("Desa Trombo, Kecamatan Bandar", "Trombo Village, Bandar Sub-district"),
                tr("Desa Jolotigo, Kecamatan Talun", "Jolotigo Village, Talun Sub-district")
            ],
        })
        st.dataframe(batas_df, use_container_width=True, hide_index=True)

    # LUAS WILAYAH
    st.markdown(
        f"""
        <div id="info-luas-wilayah" class="section" style="margin-top: 1rem; margin-bottom: 1rem;">
            <div class="section-title">{tr("Luas Wilayah Desa Silurah", "Area Size of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Membentang seluas 140,09 Hektar, hamparan tanah Silurah didominasi oleh sabuk hijau perkebunan dan persawahan yang subur. Optimalisasi tata guna lahan ini menjadi fondasi utama dalam menjaga ketahanan pangan dan kelestarian ekosistem desa.",
                    "Spanning an area of 140.09 Hectares, the vast land of Silurah is dominated by a green belt of fertile plantations and rice fields. Optimizing land use is the primary foundation for maintaining food security and village ecosystem preservation."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        luas_df = pd.DataFrame({
            tr("Penggunaan Lahan", "Land Use"): [
                tr("Pemukiman", "Residential Area"),
                tr("Persawahan", "Rice Fields"),
                tr("Perkebunan", "Plantations"),
                tr("Kuburan", "Cemetery"),
                tr("Pekarangan", "Homeyards"),
                tr("Perkantoran", "Offices"),
                tr("Prasarana Umum", "Public Infrastructure")
            ],
            tr("Luas (Ha)", "Area (Ha)"): tr(
                ["0,51", "36,00", "67,98", "2,00", "25,00", "0,29", "8,31"],
                ["0.51", "36.00", "67.98", "2.00", "25.00", "0.29", "8.31"]
            ),
        })
        st.dataframe(luas_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SECTION 3: SEKOLAH
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-sekolah" class="section" style="margin-top: 4rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">🏫 {tr("Pendidikan", "Education")}</div>
            <div class="section-title">{tr("Fasilitas Pendidikan", "Educational Facilities")}</div>
            <p class="section-body">
                {tr(
                    "Membangun masa depan dari bangku sekolah. Dari jenjang usia dini hingga sekolah menengah, fasilitas pendidikan di Silurah terus berkembang untuk memastikan setiap anak desa mendapatkan hak belajar dan fondasi ilmu pengetahuan yang kokoh.",
                    "Building the future from the classroom. From early childhood to middle school, educational facilities in Silurah continue to develop to ensure every village child receives the right to learn and a solid academic foundation."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric(label=tr("Gedung SD/Sederajat", "Elementary Schools"), value=tr("1 Unit", "1 Unit"))
    with m2:
        with st.container(border=True):
            st.metric(label=tr("Gedung SMP/Sederajat", "Middle Schools"), value=tr("1 Unit", "1 Unit"))
    with m3:
        with st.container(border=True):
            st.metric(label=tr("Taman Bermain & Bacaan", "Playgrounds & Reading Parks"), value=tr("2 Unit", "2 Units"))
    with m4:
        with st.container(border=True):
            st.metric(label=tr("Sarana Lainnya", "Other Facilities"), value=tr("4 Unit", "4 Units"))

    with st.container(border=True):
        sekolah_df = pd.DataFrame({
            tr("Nama Sekolah", "School Name"): ["PAUD Tunas Hati", "PAUD Ganesha Mulya", "SD Negeri 01 Silurah", "MI Daru Hikmah", "SMP Negeri 03 Wonotunggal SATAP"],
            tr("Jenjang", "Level"): [
                tr("PAUD", "Early Childhood"), 
                tr("PAUD", "Early Childhood"), 
                tr("SD", "Elementary"), 
                tr("SD", "Elementary"), 
                tr("SMP", "Middle School")
            ],
            tr("Lokasi", "Location"): [
                tr("Dusun Krajan", "Krajan Hamlet"),
                tr("Dusun Sipudang", "Sipudang Hamlet"),
                tr("Dusun Krajan", "Krajan Hamlet"),
                tr("Dusun Sipudang", "Sipudang Hamlet"),
                tr("Dusun Krajan", "Krajan Hamlet")
            ],
            tr("Status", "Status"): [
                tr("Swasta", "Private"), 
                tr("Swasta", "Private"), 
                tr("Negeri", "Public"), 
                tr("Swasta", "Private"), 
                tr("Negeri", "Public")
            ]
        })
        st.dataframe(sekolah_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SECTION 4: POSYANDU
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-posyandu" class="section" style="margin-top: 4rem; margin-bottom: 2rem;">
            <div class="section-eyebrow">🩺 {tr("Kesehatan", "Healthcare")}</div>
            <div class="section-title">{tr("Layanan Posyandu & Kesehatan", "Posyandu & Healthcare Services")}</div>
            <p class="section-body">
                {tr(
                    "Menjaga kualitas hidup warga sejak usia dini hingga senja. Lewat lima titik Posyandu yang beroperasi rutin di setiap dusun, layanan kesehatan dasar hadir lebih dekat untuk memantau tumbuh kembang balita, kesehatan ibu hamil, hingga kesejahteraan lansia.",
                    "Maintaining community quality of life from early childhood to twilight years. Through five Posyandu centers operating routinely in each hamlet, basic healthcare services are closer at hand to monitor toddler growth, maternal health, and elderly well-being."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        posyandu_df = pd.DataFrame({
            tr("Nama Posyandu", "Posyandu Name"): ["Posyandu Krajan", "Posyandu Sipudang", "Posyandu Simangli", "Posyandu Pomahan", "Posyandu Pedati"],
            tr("Wilayah", "Coverage Area"): ["RT 01 & RT 02", "RT 03 & RT 04", "RT 05 & RT 06", "RT 07 & RT 08", "RT 09, RT 10, & RT 11"],
            tr("Alamat", "Address"): [
                tr("Dukuh Krajan RT 01/RW 01", "Krajan Hamlet RT 01/RW 01"),
                tr("Dukuh Sipudang RT 04/RW 02", "Sipudang Hamlet RT 04/RW 02"),
                tr("Dukuh Simangli RT 05/RW 04", "Simangli Hamlet RT 05/RW 04"),
                tr("Dukuh Pomahan RT 08/RW 04", "Pomahan Hamlet RT 08/RW 04"),
                tr("Dusun Pedati RT 09/RW 05", "Pedati Hamlet RT 09/RW 05")
            ]
        })
        st.dataframe(posyandu_df, use_container_width=True, hide_index=True)

    st.markdown(
        f"""
        <div id="info-posyandu" class="section" style="margin-top: 4rem; margin-bottom: 2rem;">
            <div class="section-title">{tr("Tenaga & Sarana Kesehatan Desa", "Village Healthcare Personnel & Facilities")}</div>
            <p class="section-body">
                {tr(
                    "Harmoni antara ilmu medis modern dan kearifan tradisional. Pelayanan kesehatan masyarakat desa ditopang oleh dedikasi bidan desa serta kolaborasi erat bersama mitra bersalin terlatih dan pengobatan alternatif yang terdata resmi.",
                    "A harmony between modern medical science and traditional wisdom. Village healthcare services are supported by the dedication of village midwives and close collaboration with trained birth partners and registered alternative practitioners."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        nakes_df = pd.DataFrame({
            tr("Jenis Tenaga / Sarana Kesehatan", "Type of Personnel / Facility"): [
                tr("Bidan Desa", "Village Midwife"), 
                tr("Dukun Bersalin Terlatih", "Trained Traditional Birth Attendant"), 
                tr("Dukun Pengobatan Alternatif", "Alternative Medicine Practitioner"), 
                tr("Sarana Kesehatan Lainnya", "Other Healthcare Facilities")
            ],
            tr("Jumlah Ketersediaan", "Availability Count"): [
                tr("1 Orang", "1 Person"), 
                tr("3 Orang", "3 People"), 
                tr("4 Orang", "4 People"), 
                tr("1 Unit", "1 Unit")
            ],
            tr("Keterangan", "Description"): [
                tr("Tenaga medis profesional utama desa", "Primary professional medical personnel in the village"), 
                tr("Mitra bidan dalam penanganan persalinan", "Midwife partners in assisting childbirth"), 
                tr("Pelayanan pengobatan tradisional warga", "Traditional healing services for citizens"), 
                tr("Fasilitas pendukung kesehatan desa", "Supporting healthcare facilities in the village")
            ]
        })
        st.dataframe(nakes_df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------------------
# TAB 2 — PETA DIGITAL
# --------------------------------------------------------------------------
with tab_peta:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">{tr("Peta Wilayah", "Regional Map")}</div>
            <div class="section-title">{tr("Peta Digital Desa Silurah", "Digital Map of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Sekilas pandang peta persebaran fasilitas umum dan zonasi lahan Desa Silurah berdasarkan data spasial terbaru.",
                    "An overview of the distribution map of public facilities and land zoning in Silurah Village based on the latest spatial data."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section" style="margin-top:0;">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f'<div class="panel-title">{tr("Sebaran Titik Fasilitas", "Facility Point Distribution")}</div>', unsafe_allow_html=True)
        st.map(MAP_POINTS, size=40, color="#2C4C3B")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Legenda Kategori", "Category Legend")}</div>', unsafe_allow_html=True)
            legend_items = [
                ("🏞️", tr("Destinasi Wisata", "Tourist Destinations")),
                ("🏫", tr("Sekolah", "Schools")),
                ("🩺", tr("Posyandu", "Healthcare Centers")),
                ("🕌", tr("Fasilitas Ibadah", "Worship Facilities")),
            ]
            for icon, label in legend_items:
                st.markdown(f"**{icon} {label}**")
    with col2:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Penggunaan Lahan (Ha)", "Land Use (Ha)")}</div>', unsafe_allow_html=True)
            
            chart_data = LAND_USE_DATA.reset_index()
            
            col_lahan = tr("Penggunaan Lahan", "Land Use")
            col_luas = tr("Luas (Ha)", "Area (Ha)")
            
            chart_data.columns = [col_lahan, col_luas]
            
            bars = alt.Chart(chart_data).mark_bar(color="#2C4C3B", cornerRadiusEnd=4).encode(
                x=alt.X(f'{col_luas}:Q', scale=alt.Scale(type='sqrt'), title=col_luas),
                y=alt.Y(f'{col_lahan}:N', sort='-x', title=None),
                tooltip=[col_lahan, col_luas]
            )
            
            text = bars.mark_text(
                align='left',
                baseline='middle',
                dx=3,
                color='#4A3525',
                fontWeight='bold'
            ).encode(
                text=f'{col_luas}:Q'
            )
            
            st.altair_chart(bars + text, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 3 — WISATA (Layout Baru: Kiri Foto+Deskripsi, Kanan Maps)
# --------------------------------------------------------------------------
with tab_wisata:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">{tr("Jelajah Silurah", "Explore Silurah")}</div>
            <div class="section-title">{tr("Pesona & Daya Tarik Wisata", "Charm & Tourist Attractions")}</div>
            <p class="section-body">
                {tr(
                    "Eksplorasi keindahan alam perbukitan, kesejukan air terjun alami, serta rekam jejak warisan sejarah leluhur yang tersimpan di Desa Silurah. Pilih nama destinasi di bawah ini untuk melihat informasi mendetail dan peta lokasi GPS.",
                    "Explore the beauty of the hilly nature, the coolness of natural waterfalls, and the traces of ancestral historical heritage stored in Silurah Village. Select a destination name below to view detailed information and GPS location maps."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nama_destinasi = [w["nama"] for w in WISATA_DATA]
    sub_tabs = st.tabs(nama_destinasi)

    for tab, w in zip(sub_tabs, WISATA_DATA):
        with tab:
            with st.container(border=True):
                col_left, col_right = st.columns([1, 1.2], gap="large")

                # ==========================================================
                # KOLOM KIRI: FOTO WISATA + DESKRIPSI
                # ==========================================================
                # ==========================================================
                # KOLOM KIRI: FOTO WISATA + DESKRIPSI (VERSI PALING AMAN)
                # ==========================================================
                with col_left:
                    # Logika langsung mendeteksi file _ID.jpg atau _EN.jpg berdasarkan nama file asli
                    nama_file_dasar = w['nama'].replace("Situs ", "").replace("Arca ", "") # Menyesuaikan jika ada awalan
                    
                    if is_eng and (ASSETS_DIR / f"{w['nama']}_EN.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{w['nama']}_EN.jpg"
                    elif (ASSETS_DIR / f"{w['nama']}_ID.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{w['nama']}_ID.jpg"
                    elif (ASSETS_DIR / f"{nama_file_dasar}_ID.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{nama_file_dasar}_ID.jpg"
                    else:
                        # Fallback otomatis mengambil foto bersih utama jika versi teks belum ada
                        foto_tampil = ASSETS_DIR / f"{w['nama']}.jpg"
                        if not foto_tampil.exists():
                            # Pilihan cadangan terakhir jika nama file aslinya tanpa kata Situs
                            foto_tampil = ASSETS_DIR / f"{nama_file_dasar}.jpg"
                        
                    st.image(str(foto_tampil), use_container_width=True)
                    
                    st.markdown(
                        f'<div style="margin-top: 15px; line-height: 1.7; font-size: 0.95rem; color: var(--text-dark); text-align: justify;"></div>',
                        unsafe_allow_html=True,
                    )

                # ==========================================================
                # KOLOM KANAN: JUDUL, TOMBOL MAPS & PETA 3D
                # ==========================================================
                with col_right:
                    st.markdown(f"### {w['nama']}")
                    dusun_text = w.get('dusun', tr('Desa Silurah', 'Silurah Village'))
                    st.caption(f"{tr('Wilayah:', 'Area:')} {dusun_text}")
         
                    st.markdown(
                        f"**{tr('Peta Lokasi:', 'Location Map:')}** {tr('Titik GPS', 'GPS Coordinates')} ({w['lat']}, {w['lon']})"
                    )

                    if "link_maps" in w:
                        st.link_button(tr("Buka Lokasi di Google Maps", "Open Location in Google Maps"), w["link_maps"], use_container_width=True)

                    df_lokasi = pd.DataFrame(
                        {
                            "lat": [w["lat"]],
                            "lon": [w["lon"]],
                            "nama": [w["nama"]],
                        }
                    )

                    view_state = pdk.ViewState(
                        latitude=w["lat"],
                        longitude=w["lon"],
                        zoom=15,
                        pitch=45,
                    )

                    layer_point = pdk.Layer(
                        "ScatterplotLayer",
                        data=df_lokasi,
                        get_position="[lon, lat]",
                        get_fill_color=[44, 76, 59, 255],
                        get_radius=40,
                        pickable=True,
                    )

                    r = pdk.Deck(
                        layers=[layer_point],
                        initial_view_state=view_state,
                        tooltip={"text": "{nama}"},
                    )
                    st.pydeck_chart(r, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 4 — STATISTIK
# --------------------------------------------------------------------------
with tab_statistik:
    st.markdown(
        """
        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">Data & Demografi</div>
            <div class="section-title">Profil Kependudukan</div>
            <p class="section-body">
                Ringkasan data demografi Desa Silurah berdasarkan dusun dan
                kelompok usia (data dummy untuk keperluan demonstrasi tampilan).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section" style="margin-top:0;">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Total Penduduk", "1950", None),
        ("Kepala Keluarga", "633", None),
        ("Luas Wilayah", "140,09 Ha", None),
        ("Rasio Gender", "105,26", None),
    ]
    for col, (label, value, delta) in zip([m1, m2, m3, m4], metrics):
        with col:
            with st.container(border=True):
                st.metric(label, value, delta)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Penduduk per Dusun</div>', unsafe_allow_html=True)
            st.bar_chart(POPULATION_DATA, color=["#2C4C3B", "#4A3525"])
    with c2:
        with st.container(border=True):
            st.markdown('<div class="panel-title">Struktur Usia</div>', unsafe_allow_html=True)
            st.bar_chart(AGE_DATA, color="#4A3525")
    st.markdown("</div>", unsafe_allow_html=True)