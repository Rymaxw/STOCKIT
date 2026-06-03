import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import streamlit.components.v1 as components
from utils.sidebar import dapatkan_html_sidebar

class HalamanTentang:
    def __init__(self):
        st.set_page_config(
            page_title="About STOCKIT",
            page_icon="ℹ️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        gaya_sembunyikan = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stHeader"] {display: none !important;}
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            </style>
            """
        st.markdown(gaya_sembunyikan, unsafe_allow_html=True)

        st.markdown(dapatkan_html_sidebar("About"), unsafe_allow_html=True)

        konten_html = f"""
<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>About STOCKIT</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
  tailwind.config = {{
    darkMode: "class",
    theme: {{
      extend: {{
        "colors": {{
                "tertiary-container": "#89cbd9",
                "on-primary": "#003543",
                "on-tertiary": "#00363e",
                "inverse-on-surface": "#2f303b",
                "primary-fixed-dim": "#4cd6ff",
                "primary": "#a4e6ff",
                "on-tertiary-fixed": "#001f25",
                "surface-tint": "#4cd6ff",
                "surface-container-lowest": "#0c0e17",
                "surface-container-low": "#1a1b25",
                "secondary": "#c0c1ff",
                "outline": "#859399",
                "inverse-surface": "#e2e1f0",
                "background": "#11131d",
                "tertiary-fixed-dim": "#8ed1df",
                "on-error": "#690005",
                "on-surface": "#e2e1f0",
                "on-secondary-fixed-variant": "#2f2ebe",
                "on-secondary": "#1000a9",
                "error-container": "#93000a",
                "tertiary": "#a4e7f6",
                "surface-container-high": "#282934",
                "tertiary-fixed": "#aaedfc",
                "surface-dim": "#11131d",
                "surface-container": "#1e1f29",
                "secondary-container": "#3131c0",
                "surface-container-highest": "#33343f",
                "on-primary-fixed": "#001f28",
                "on-secondary-container": "#b0b2ff",
                "surface-bright": "#373844",
                "secondary-fixed": "#e1e0ff",
                "outline-variant": "#3c494e",
                "on-primary-fixed-variant": "#004e60",
                "error": "#ffb4ab",
                "primary-fixed": "#b7eaff",
                "on-secondary-fixed": "#07006c",
                "on-tertiary-container": "#005763",
                "on-surface-variant": "#bbc9cf",
                "surface": "#11131d",
                "secondary-fixed-dim": "#c0c1ff",
                "surface-variant": "#33343f",
                "on-tertiary-fixed-variant": "#004e5a",
                "on-primary-container": "#00566a",
                "on-background": "#e2e1f0",
                "inverse-primary": "#00677f",
                "primary-container": "#00d1ff",
                "on-error-container": "#ffdad6"
        }},
        "borderRadius": {{
                "DEFAULT": "0.25rem",
                "lg": "0.5rem",
                "xl": "0.75rem",
                "full": "9999px"
        }},
        "spacing": {{
                "section-margin": "4rem",
                "gutter": "1.5rem",
                "element-gap": "1rem",
                "container-padding": "2rem"
        }},
        "fontFamily": {{
                "headline-xl": [
                        "Space Grotesk"
                ],
                "body-md": [
                        "Space Grotesk"
                ],
                "headline-lg-mobile": [
                        "Space Grotesk"
                ],
                "headline-lg": [
                        "Space Grotesk"
                ],
                "label-sm": [
                        "Space Grotesk"
                ]
        }},
        "fontSize": {{
                "headline-xl": [
                        "48px",
                        {{
                                "lineHeight": "1.1",
                                "letterSpacing": "-0.02em",
                                "fontWeight": "600"
                        }}
                ],
                "body-md": [
                        "16px",
                        {{
                                "lineHeight": "1.6",
                                "letterSpacing": "0.01em",
                                "fontWeight": "400"
                        }}
                ],
                "headline-lg-mobile": [
                        "24px",
                        {{
                                "lineHeight": "1.2",
                                "fontWeight": "500"
                        }}
                ],
                "headline-lg": [
                        "32px",
                        {{
                                "lineHeight": "1.2",
                                "letterSpacing": "-0.01em",
                                "fontWeight": "500"
                        }}
                ],
                "label-sm": [
                        "12px",
                        {{
                                "lineHeight": "1",
                                "letterSpacing": "0.05em",
                                "fontWeight": "600"
                        }}
                ]
        }}
      }}
    }}
  }}
</script>
<style>
    .glass-panel {{
        background: rgba(26, 27, 37, 0.4);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(133, 147, 153, 0.15);
    }}
    .glass-card {{
        background: linear-gradient(145deg, rgba(30, 31, 41, 0.6) 0%, rgba(17, 19, 29, 0.8) 100%);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(164, 230, 255, 0.1);
        box-shadow: 0 32px 64px -16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }}
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: #11131d;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #3c494e;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #4cd6ff;
    }}
</style>
</head>
<body class="bg-background text-on-background min-h-screen flex overflow-hidden font-body-md antialiased selection:bg-primary/30 selection:text-primary m-0 p-0">
<!-- Smooth Premium Gradient Background -->
<div class="fixed inset-0 z-[-1] pointer-events-none bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-background to-background"></div>
<div class="fixed inset-0 z-[-1] pointer-events-none bg-[radial-gradient(circle_at_bottom_left,_var(--tw-gradient-stops))] from-secondary-container/10 via-transparent to-transparent"></div>

<!-- TopAppBar for Mobile -->
<header class="md:hidden flex justify-between items-center w-full px-6 h-16 border-b border-outline-variant/20 glass-panel fixed top-0 left-0 z-50">
<div class="font-headline-lg text-lg font-semibold text-on-surface tracking-wide uppercase">STOCKIT</div>
<div class="flex gap-4 text-on-surface-variant">
<span class="material-symbols-outlined">menu</span>
</div>
</header>

<!-- Main Content Canvas -->
<main class="flex-1 ml-0 md:ml-0 mt-16 md:mt-0 p-6 md:p-container-padding h-screen overflow-y-auto relative z-10 flex items-center justify-center">
<div class="w-full max-w-5xl mx-auto relative">
<!-- Glass Card -->
<section class="glass-card rounded-2xl overflow-hidden relative">
<!-- Holographic Background Element -->
<div class="absolute right-0 top-0 w-2/3 h-full opacity-30 mix-blend-screen pointer-events-none" style="mask-image: linear-gradient(to right, transparent, black); -webkit-mask-image: linear-gradient(to right, transparent, black);">
<img alt="MPT Hologram" class="w-full h-full object-cover filter contrast-125 brightness-110 hue-rotate-[190deg]" src="https://lh3.googleusercontent.com/aida/AP1WRLuCjtvyrA-Pk31p3r3iiwf_XY-lSPPT3jd65hXN9yGkfTKjdPYC9mjKiMgz4ffAhSMcyiCmmgWDjuteT55Tog0o0nE6ztt3LfamNt1M6Z6Mu7jaoI3dLvsk96vhcBago-CEqhsn6MMBo4JJ49qgY8SPDVzHWQQzOu66t0txOyYJokHA8jk0fKh2LgcoABN6dIvKueAM11VeROn0tW3SCHjT0ZZwu9Uk27RiEB2jYn0iK6tzPHoMPQePSbI"/>
</div>
<div class="relative z-10 p-8 md:p-16 flex flex-col gap-12">
<!-- Header -->
<div class="flex items-center gap-6">
<div class="w-16 h-16 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center shadow-[0_0_30px_rgba(164,230,255,0.15)]">
<span class="material-symbols-outlined text-primary text-3xl">info</span>
</div>
<div>
<h2 class="font-headline-xl text-headline-xl text-on-surface tracking-tight m-0">
                            About <span class="text-primary font-semibold">STOCKIT</span>
</h2>
</div>
</div>
<!-- Content -->
<div class="max-w-2xl space-y-8">
<p class="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface leading-snug m-0">
                        Aplikasi ini menggunakan pendekatan Modern Portfolio Theory (MPT) untuk memberikan rekomendasi bobot investasi yang efisien.
                    </p>
<div class="p-6 rounded-xl bg-surface-container-high/30 border border-outline-variant/20 backdrop-blur-sm">
<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed m-0">
                            Dikembangkan sebagai implementasi sains data dalam analisis pasar keuangan.
                        </p>
</div>
</div>
<!-- Technical Footer/Metadata -->
<div class="flex flex-wrap gap-4 pt-4">
<div class="inline-flex items-center gap-2 bg-surface-container-lowest/50 px-4 py-2 rounded-full border border-outline-variant/20 backdrop-blur-md">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse shadow-[0_0_8px_rgba(164,230,255,0.8)]"></span>
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-widest">SYS.STATUS: ONLINE</span>
</div>
<div class="inline-flex items-center gap-2 bg-surface-container-lowest/50 px-4 py-2 rounded-full border border-outline-variant/20 backdrop-blur-md">
<span class="material-symbols-outlined text-[14px] text-primary/70">memory</span>
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-widest">V 4.0.2</span>
</div>
</div>
</div>
</section>
</div>
</main>
</body></html>
        """
        components.html(konten_html, height=900, scrolling=True)

if __name__ == "__main__":
    HalamanTentang().render()