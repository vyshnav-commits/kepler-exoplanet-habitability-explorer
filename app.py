import streamlit as st
import pandas as pd

# Setting up page config
st.set_page_config(page_title="Exoplanet Habitability Finder", page_icon="🌌", layout="wide")

st.title("🌌 Exoplanet Habitability & Location Explorer")
st.write("Explore potential habitable exoplanets filtered from NASA's Kepler dataset based on Earth-like properties.")

# Loading the filtered datasets
@st.cache_data
def load_data():
    df_hab = pd.read_csv('habitable_planets.csv')
    df_loc = pd.read_csv('planet_locations.csv')
    return df_hab, df_loc

try:
    df_hab, df_loc = load_data()

    # Sidebar for planet selection
    st.sidebar.header("Filter & Select")
    planet_list = df_hab['kepler_name'].dropna().unique().tolist()
    selected_planet = st.sidebar.selectbox("Choose an Exoplanet:", planet_list)

    if selected_planet:
        st.subheader(f"🪐 Planet Report: {selected_planet}")
        
        # Filtering data for the selected planet
        planet_info = df_hab[df_hab['kepler_name'] == selected_planet].iloc[0]
        planet_pos = df_loc[df_loc['rowid'] == planet_info['rowid']].iloc[0]
        
        # Grid layout for properties
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Physical Properties")
            st.write(f"**Orbital Period:** {planet_info['koi_period']:.2f} Days")
            st.write(f"**Planet Radius:** {planet_info['koi_prad']:.2f} x Earth Radius")
            st.write(f"**Equilibrium Temp:** {planet_info['koi_teq']:.1f} K (Approx. {planet_info['koi_teq']-273.15:.1f}°C)")
            
        with col2:
            st.markdown("### 📍 Sky Coordinates")
            st.write(f"**Right Ascension (RA):** {planet_pos['ra']:.4f}")
            st.write(f"**Declination (DEC):** {planet_pos['dec']:.4f}")
            
            # Dynamic link to NASA's Sky Map form
            sky_map_url = f"https://archive.stsci.edu/cgi-bin/dss_form?ra={planet_pos['ra']}&dec={planet_pos['dec']}"
            st.markdown(f"[🔗 View on NASA Sky Map]({sky_map_url})")

except FileNotFoundError:
    st.error("Error: CSV files not found! Please run the Jupyter notebook data cleaning script first.")