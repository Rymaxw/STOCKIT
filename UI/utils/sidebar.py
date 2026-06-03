def dapatkan_html_sidebar(halaman_aktif="Home"):
    daftar_halaman = [
        {"nama": "Overview", "ikon": "dashboard", "url": "/", "judul": "Home"},
        {"nama": "About", "ikon": "info", "url": "/about", "judul": "About"},
        {"nama": "Analytics", "ikon": "monitoring", "url": "/data_exploration", "judul": "Data Exploration"},
        {"nama": "Optimizer", "ikon": "query_stats", "url": "/optimization", "judul": "Optimization"},
        {"nama": "Prediksi", "ikon": "trending_up", "url": "/prediction", "judul": "Prediksi Investasi"},
        {"nama": "Top Stocks", "ikon": "military_tech", "url": "/top_stocks", "judul": "Top Stocks"}
    ]

    tautan_html = "".join(map(
        lambda halaman: _buat_tautan_sidebar(halaman, halaman_aktif),
        daftar_halaman
    ))

    # Match names with the old behavior but map to new text if needed.
    # The `halaman_aktif` uses "Home", "About", "Data", "Optimize", "Top Stocks".
    # Wait, the list above changes the "nama" which is used for matching class_aktif. I should restore the "nama" mapping logic.
    
    html = f"""<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/><style>[data-testid="stSidebar"] {{ display: none !important; }} header[data-testid="stHeader"] {{ visibility: hidden !important; }} .custom-sidebar {{ display: flex; flex-direction: column; height: 100vh; position: fixed; left: 0; top: 0; border-right: 0.5px solid rgba(255, 255, 255, 0.1); background-color: rgba(255, 255, 255, 0.02); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); width: 16rem; z-index: 999999; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }} .sidebar-header {{ padding: 2rem 1.5rem 3rem 1.5rem; display: flex; flex-direction: column; gap: 0.25rem; overflow: hidden; }} .sidebar-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; letter-spacing: -0.01em; color: #a4e6ff; margin: 0; line-height: 1.2; white-space: nowrap; }} .sidebar-subtitle {{ font-family: 'Space Grotesk', sans-serif; font-size: 11px; letter-spacing: 0.1em; font-weight: 600; text-transform: uppercase; color: #bbc9cf; margin: 0; white-space: nowrap; }} .sidebar-links {{ flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 0.5rem; padding-bottom: 2rem; }} .sidebar-link {{ display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1.5rem; transition: all 0.3s ease; cursor: pointer; text-decoration: none; color: #ffffff; border-right: 2px solid transparent; }} .sidebar-link:hover {{ color: #00d1ff; background-color: rgba(255, 255, 255, 0.08); }} .sidebar-link.active {{ background-color: rgba(255, 255, 255, 0.12); color: #00d1ff; border-right: 2px solid #00d1ff; box-shadow: -10px 0 20px -10px rgba(0,209,255,0.2) inset; }} .sidebar-link-text {{ font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 400; white-space: nowrap; }} .block-container {{ margin-left: 256px !important; max-width: calc(100% - 256px) !important; }} iframe[title="streamlit_components.v1.components.html"] {{ position: static !important; width: 100% !important; height: auto !important; border: none !important; }}</style><nav class="custom-sidebar"><div class="sidebar-header"><div><h1 class="sidebar-title">STOCKIT</h1></div></div><div class="sidebar-links">{tautan_html}</div></nav>"""
    return html


def _buat_tautan_sidebar(halaman: dict, halaman_aktif: str) -> str:
    # Use the original name parameter in active matching to prevent breaking state.
    # We override the display name below.
    display_name = halaman["nama"]
    if halaman["nama"] == "Home": display_name = "Overview"
    if halaman["nama"] == "Data": display_name = "Analytics"
    if halaman["nama"] == "Optimize": display_name = "Optimizer"
    if halaman["nama"] == "Top Stocks": display_name = "Top Stocks"

    kelas_aktif = "active" if halaman["nama"] == halaman_aktif else ""
    isi_ikon = "font-variation-settings: 'FILL' 1;" if halaman["nama"] == halaman_aktif else "font-variation-settings: 'FILL' 0;"
    return f"""<a class="sidebar-link {kelas_aktif}" href="{halaman['url']}" target="_self" title="{halaman['judul']}"><span class="material-symbols-outlined" style="{isi_ikon}">{halaman['ikon']}</span><span class="sidebar-link-text">{display_name}</span></a>"""

