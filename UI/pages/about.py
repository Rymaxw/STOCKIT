import streamlit as st

class AboutPage:
    def render(self):
        st.title("About Optimal")
        st.write("Aplikasi ini menggunakan pendekatan Modern Portfolio Theory (MPT) untuk memberikan rekomendasi bobot investasi yang efisien.")
        st.write("Dikembangkan sebagai implementasi sains data dalam analisis pasar keuangan.")

if __name__ == "__main__":
    AboutPage().render()