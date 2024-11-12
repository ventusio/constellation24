import folium
import numpy as np
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from shared.models import Point


def main():
    st.title("Feather")

    galleria_loc = Point(lat=-26.08515380647537, lng=28.087210287422618)
    if "data" not in st.session_state:
        st.session_state.data = (
            np.random.normal(size=(100, 3)) * np.array([[0.05, 0.05, 1]])
            + np.array([[galleria_loc.lat, galleria_loc.lng, 1]])
        ).tolist()
    data = st.session_state.data
    print(data)

    m = folium.Map(location=galleria_loc.as_tuple(), zoom_start=14)

    folium.Marker(galleria_loc.as_tuple(), tooltip="The Galleria").add_to(m)
    HeatMap(data).add_to(m)

    st_data = st_folium(m, use_container_width=True)
    col1, col2, col3 = st.columns(3)

    def create_info_box(title: str, value: any) -> None:
        st.markdown(
            f"""
            <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                {title}: {value}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col1:
        create_info_box("Latitude", round(st_data["center"]["lat"], 6))
    with col2:
        create_info_box("Longitude", round(st_data["center"]["lng"], 6))
    with col3:
        create_info_box("Zoom", st_data["zoom"])


if __name__ == "__main__":
    main()
