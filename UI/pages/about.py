import streamlit as st
import streamlit.components.v1 as components
from utils.sidebar import get_sidebar_html

class AboutPage:
    def __init__(self):
        st.set_page_config(
            page_title="About STOCKIT",
            page_icon="ℹ️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        # Hide default Streamlit elements to make the custom HTML full-screen
        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        # Inject the native Streamlit DOM sidebar
        st.markdown(get_sidebar_html("About"), unsafe_allow_html=True)

        html_content = f"""
<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>About STOCKIT</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&amp;family=Space+Grotesk:wght@300..700&amp;family=Geist:wght@100..900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {{
          darkMode: "class",
          theme: {{
            extend: {{
              "colors": {{
                      "tertiary-container": "#d0d8ff",
                      "outline": "#849495",
                      "surface-dim": "#131313",
                      "primary-fixed": "#7df4ff",
                      "tertiary": "#f6f5ff",
                      "on-error": "#690005",
                      "on-secondary-fixed": "#23005b",
                      "background": "#131313",
                      "on-error-container": "#ffdad6",
                      "surface-container-highest": "#353534",
                      "inverse-on-surface": "#313030",
                      "error": "#ffb4ab",
                      "on-secondary": "#3c0090",
                      "inverse-primary": "#006970",
                      "on-tertiary-fixed": "#001551",
                      "on-primary-fixed-variant": "#004f54",
                      "surface-container-high": "#2a2a2a",
                      "tertiary-fixed-dim": "#b6c4ff",
                      "on-secondary-container": "#ddcdff",
                      "primary-fixed-dim": "#00dbe9",
                      "tertiary-fixed": "#dce1ff",
                      "surface-container-lowest": "#0e0e0e",
                      "on-primary-fixed": "#002022",
                      "on-primary-container": "#006970",
                      "surface": "#131313",
                      "on-primary": "#00363a",
                      "error-container": "#93000a",
                      "on-surface": "#e5e2e1",
                      "secondary-container": "#7000ff",
                      "on-tertiary-container": "#004eeb",
                      "surface-variant": "#353534",
                      "surface-tint": "#00dbe9",
                      "surface-container-low": "#1c1b1b",
                      "on-tertiary-fixed-variant": "#0039b3",
                      "inverse-surface": "#e5e2e1",
                      "primary-container": "#00f0ff",
                      "on-surface-variant": "#b9cacb",
                      "outline-variant": "#3b494b",
                      "secondary-fixed-dim": "#d1bcff",
                      "secondary-fixed": "#e9ddff",
                      "secondary": "#d1bcff",
                      "surface-container": "#201f1f",
                      "primary": "#dbfcff",
                      "on-background": "#e5e2e1",
                      "on-tertiary": "#002780",
                      "on-secondary-fixed-variant": "#5700c9",
                      "surface-bright": "#3a3939"
              }},
              "borderRadius": {{
                      "DEFAULT": "0.25rem",
                      "lg": "0.5rem",
                      "xl": "0.75rem",
                      "full": "9999px"
              }},
              "spacing": {{
                      "margin-mobile": "16px",
                      "unit": "4px",
                      "gutter": "16px",
                      "margin-desktop": "32px",
                      "grid-opacity": "0.05"
              }},
              "fontFamily": {{
                      "label-caps": [
                              "Space Mono"
                      ],
                      "display-lg": [
                              "Space Grotesk"
                      ],
                      "body-base": [
                              "Geist"
                      ],
                      "headline-md": [
                              "Space Grotesk"
                      ],
                      "data-mono": [
                              "Space Mono"
                      ]
              }},
              "fontSize": {{
                      "label-caps": [
                              "11px",
                              {{
                                      "lineHeight": "1.0",
                                      "letterSpacing": "0.1em",
                                      "fontWeight": "700"
                              }}
                      ],
                      "display-lg": [
                              "48px",
                              {{
                                      "lineHeight": "1.1",
                                      "letterSpacing": "-0.02em",
                                      "fontWeight": "700"
                              }}
                      ],
                      "body-base": [
                              "14px",
                              {{
                                      "lineHeight": "1.6",
                                      "letterSpacing": "0.01em",
                                      "fontWeight": "400"
                              }}
                      ],
                      "headline-md": [
                              "24px",
                              {{
                                      "lineHeight": "1.2",
                                      "letterSpacing": "0.02em",
                                      "fontWeight": "600"
                              }}
                      ],
                      "data-mono": [
                              "13px",
                              {{
                                      "lineHeight": "1.4",
                                      "letterSpacing": "0.05em",
                                      "fontWeight": "400"
                              }}
                      ]
              }}
      }},
          }},
        }}
      </script>
<style>
        .clip-faceted {{
            clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0 100%);
        }}
        .clip-faceted-sm {{
            clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
        }}
        .bg-grid-pattern {{
            background-image: linear-gradient(to right, rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
            background-size: 32px 32px;
        }}
        .glow-text {{
            text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
        }}
        .glow-border {{
            box-shadow: 0 0 4px rgba(0, 240, 255, 0.3), inset 0 0 4px rgba(0, 240, 255, 0.3);
        }}
        /* Custom scrollbar for iframe */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #131313;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #3b494b;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #00dbe9;
        }}
    </style>
</head>
<body class="bg-background text-on-background min-h-screen flex overflow-hidden m-0 p-0">
<!-- Background Grid -->
<div class="fixed inset-0 bg-grid-pattern z-[-1] pointer-events-none"></div>
<!-- TopAppBar for Mobile (Shared Component Logic - Alternative) -->
<header class="md:hidden flex justify-between items-center w-full px-margin-mobile h-16 border-b border-outline-variant/30 bg-surface-dim fixed top-0 left-0 z-50">
<div class="font-display-lg text-headline-md font-bold text-primary tracking-widest uppercase">STOCKIT</div>
<div class="flex gap-4 text-primary">
<span class="material-symbols-outlined">menu</span>
</div>
</header>
<!-- Main Content Canvas -->
<main class="flex-1 ml-0 md:ml-0 mt-16 md:mt-0 p-margin-mobile md:p-margin-desktop h-screen overflow-y-auto relative z-10">
<div class="max-w-4xl mx-auto h-full flex flex-col justify-center relative">
<!-- Floating Holographic Graphic Container -->
<div class="absolute right-0 top-1/4 w-96 h-96 opacity-20 pointer-events-none mix-blend-screen z-[-1] hidden lg:block">
<img alt="MPT Hologram" class="w-full h-full object-cover filter contrast-150 brightness-75 hue-rotate-180 sepia-[0.5]" data-alt="A highly complex, abstract holographic data visualization of Modern Portfolio Theory. Glowing cyan and deep blue lines intersect on a pure black background forming a dynamic 3D structural mesh. The technical aesthetic suggests advanced financial modeling in a cyberpunk, super-dark environment. Bright neon nodes connect wireframe paths simulating market efficiency and risk vectors." src="https://lh3.googleusercontent.com/aida-public/AB6AXuBasfaIkGsdlXa4zGEfo1Z5mqT9XehEPcqX3mb8uURbpk0X5wDJSxJMc2ULfktnDkLS_fs-gmI5nIbo3bt9flXWhyWLrYvFKKHISuqxIedz_gfZcOcDmeX3-eC_jX3fh7UZf-WMc0A4ensuANv7XO8ax1LhoYSnIaj6CCvLH_UGpYd84p7va3ZasbjJIfwZ4Jb-piWczupYe1rFFV_N882oQuw1NLwI0yEM7FVz3BlbMuUBvKAU97W1CXUIbN6QrN2iwWJEnwBVofck"/>
</div>
<!-- Content Panel -->
<section class="bg-surface-container-low/80 backdrop-blur-md border border-outline-variant/40 p-8 md:p-12 clip-faceted shadow-[inset_0_1px_0_rgba(0,240,255,0.1)] relative overflow-hidden">
<!-- Subtle inner accent line -->
<div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/50 to-transparent"></div>
<div class="flex items-center gap-4 mb-8 border-b border-outline-variant/30 pb-6">
<div class="p-3 bg-surface border border-primary/30 clip-faceted-sm glow-border flex items-center justify-center">
<span class="material-symbols-outlined text-primary text-[32px]">info</span>
</div>
<h2 class="font-display-lg text-display-lg text-on-surface mb-6 relative inline-block"><span class="text-primary glow-text">About</span> STOCKIT</h2>
</div>
<div class="space-y-8 max-w-2xl">
<p class="font-body-base text-headline-md text-on-surface-variant leading-relaxed">
                        Aplikasi ini menggunakan pendekatan Modern Portfolio Theory (MPT) untuk memberikan rekomendasi bobot investasi yang efisien.
                    </p>
<div class="pl-6 border-l-2 border-primary/50">
<p class="font-data-mono text-body-base text-on-surface-variant opacity-80 leading-loose tracking-wide">
                            Dikembangkan sebagai implementasi sains data dalam analisis pasar keuangan.
                        </p>
</div>
</div>
<!-- Technical Footer/Metadata -->
<div class="mt-12 pt-6 border-t border-outline-variant/20 flex flex-wrap gap-4">
<div class="inline-flex items-center gap-2 bg-surface-dim px-3 py-1.5 border border-outline-variant/30 clip-faceted-sm">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
<span class="font-label-caps text-label-caps text-on-surface-variant">SYS.STATUS: ONLINE</span>
</div>
<div class="inline-flex items-center gap-2 bg-surface-dim px-3 py-1.5 border border-outline-variant/30 clip-faceted-sm">
<span class="material-symbols-outlined text-[14px] text-outline">memory</span>
<span class="font-label-caps text-label-caps text-on-surface-variant">V 4.0.2</span>
</div>
</div>
</section>
</div>
</main>
</body></html>
        """
        # Render the custom HTML with a large enough height
        components.html(html_content, height=900, scrolling=True)

if __name__ == "__main__":
    AboutPage().render()