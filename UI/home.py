import streamlit as st

class HomePage:
    def __init__(self):
        st.set_page_config(
            page_title="Optimal - Stock Portfolio",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def render(self):
        st.title("Optimal 🎯")
        st.subheader("Data Science App for Stock Portfolio Optimization")
        st.markdown("---")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Aplikasi ini membantu merancang portofolio saham menggunakan pendekatan kuantitatif.")
            st.write("Gunakan navigasi di sidebar untuk mengeksplorasi data dan menjalankan algoritma optimasi.")
        
        with col2:
            st.info("Pilih menu untuk memulai.")

if __name__ == "__main__":
    app = HomePage()
    app.render()