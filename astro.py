import streamlit as st
from geopy.geocoders import Nominatim
import folium
import requests
import pandas as pd


def main():
    st.title("Astro A.I.")

    min_date = pd.to_datetime("1920-01-01")
    max_date = pd.to_datetime("today")
    services = ['dosha', 'dashas', 'extended-horoscope',
                'horoscope', 'panchang', 'predictions']
    planets = ["Sun", "Moon", "Mercury", "Venus", "Mars",
               "Saturn", "Jupiter", "Rahu", "Ketu", "Ascendant"]
    divs = ['D1', 'D2', 'D3', 'D3-s', 'D4', 'D5', 'D7', 'D8', 'D9', 'D10', 'D10-R', 'D12', 'D16',
            'D20', 'D24', 'D24-R', 'D27', 'D40', 'D45', 'D60', 'D30', 'chalit', 'sun', 'moon', 'kp_chalit']

    typ = st.selectbox('enter the type of astrology:', services)
    if typ == 'dosha':
        Dosha_options = ['mangal-dosh', 'kaalsarp-dosh',
                         'manglik-dosh', 'pitra-dosh', 'papasamaya']
        selected_sub_option = st.selectbox('Select Sub-option:', Dosha_options)
    elif typ == 'dashas':
        Dashas_options = ['maha-dasha', 'maha-dasha-predictions', 'antar-dasha', 'char-dasha-current', 'char-dasha-main', 'char-dasha-sub',
                          'current-mahadasha-full', 'current-mahadasha', 'parayantar-dasha', 'specific-dasha', 'yogini-dasha-main', 'yogini-dasha-sub']
        selected_sub_option = st.selectbox(
            'Select Sub-option:', Dashas_options)
    elif typ == 'extended-horoscope':
        ext_horo_options = ['find-moon-sign', 'find-sun-sign', 'find-ascendant', 'current-sade-sati', 'extended-kundli-details', 'sade-sati-table', 'friendship-table',
                            'kp-houses', 'kp-planets', 'gem-suggestion', 'numero-table', 'rudraksh-suggestion', 'varshapal-details', 'varshapal-month-chart', 'varshapal-year-chart', 'yoga-list']
        selected_sub_option = st.selectbox(
            'Select Sub-option:', ext_horo_options)
    elif typ == 'horoscope':
        selected_planet = None
        selected_div = None
        horo_options = ['planet-details', 'ascendant-report', 'planet-report', 'personal-characteristics',
                        'divisional-charts', 'chart-image', 'ashtakvarga', 'binnashtakvarga', 'western-planets']
        selected_sub_option = st.selectbox('Select Sub-option:', horo_options)
        if selected_sub_option in ['planet-report', 'binnashtakvarga']:
            selected_planet = st.selectbox('Select Planet:', planets)
        elif selected_sub_option in ['divisional-charts', 'chart-image']:
            selected_div = st.selectbox('Select Division:', divs)
    else:
        selected_sub_option = None

    dob = st.date_input('Select your Date of Birth:',
                        min_value=min_date, max_value=max_date, key="dob")
    tob = st.time_input('Select your Time of Birth:', key="tob")
    lang = st.selectbox('Select Language:', ['en', 'hi'])

    location_name = st.text_input("Enter location:", "India")
    selected_location = get_coordinates(location_name)

    map_html = get_map(location_name)
    st.components.v1.html(map_html, width=800, height=600)

    if st.button("Get Vedic Astrology Details"):
        if selected_location is not None:
            latitude, longitude = selected_location
            # if selected_sub_option == 'planet-report' or 'divisional-charts' or 'chart-image' or 'binnashtakvarga' :
            #     astro_api_url = get_astro_api_url(typ,selected_sub_option, selected_planet,dob, tob, latitude, longitude, lang)
            # else:
            if typ == "horoscope":
                if selected_planet is not None and selected_div is not None:
                    astro_api_url = get_astro_api_url(
                        typ, selected_sub_option, dob, tob, latitude, longitude, lang, selected_planet, selected_div)
                elif selected_planet is not None:
                    astro_api_url = get_astro_api_url(
                        typ, selected_sub_option, dob, tob, latitude, longitude, lang, selected_planet, "D1")
                elif selected_div is not None:
                    astro_api_url = get_astro_api_url(
                        typ, selected_sub_option, dob, tob, latitude, longitude, lang, "Sun", selected_div)
                else:
                    astro_api_url = get_astro_api_url(
                        typ, selected_sub_option, dob, tob, latitude, longitude, lang, "Sun", "D1")
            else:
                astro_api_url = get_astro_api_url(
                    typ, selected_sub_option, dob, tob, latitude, longitude, lang, "Sun", "D1")
            response = requests.get(astro_api_url)

            st.write("Vedic Astrology API Response:")
            if selected_sub_option == 'chart-image':
                svg_content = response.text
                st.image(svg_content, output_format="auto")
            else:
                st.json(response.json())
        else:
            st.error("Location not found. Please enter a valid location.")


def get_map(location_name):
    geolocator = Nominatim(user_agent="location_selector")
    location = geolocator.geocode(location_name)

    if location is not None:
        m = folium.Map(location=[location.latitude,
                       location.longitude], zoom_start=6)
        folium.Marker([location.latitude, location.longitude],
                      popup=location_name).add_to(m)
        return m._repr_html_()
    else:
        return "<p>Location not found</p>"


def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="location_selector")
    location = geolocator.geocode(location_name)

    if location is not None:
        return location.latitude, location.longitude
    else:
        return None

    # service,sub_option,


def append_params(astro_api_url, selected_sub_option, selected_planet, selected_div):
    print(selected_sub_option, selected_planet, selected_div)
    formatted_url = f"{astro_api_url}"
    if selected_sub_option == 'planet-report' or selected_sub_option == 'binnashtakvarga':
        formatted_url += f"&planet={selected_planet}"
    if selected_sub_option == 'divisional-charts' or selected_sub_option == 'chart-image':
        formatted_url += f"&div={selected_div}"
    if selected_sub_option == 'chart-image':
        formatted_url += f"&color=%23ff3366&style=north&font_size=14&font_style=roboto&colorful_planets=1&size=300&stroke=2&format=utf8"
    print("formatted_url", formatted_url)
    return formatted_url


def get_astro_api_url(typ, selected_sub_option, dob, tob, lat, lon, lang, selected_planet, selected_div):
    print("extra args:>>", selected_planet, selected_div)
    api_key = 'dfa2b8e6-d4f5-584a-b08c-e0a1e0150047'

    # Format date and time for the API request
    formatted_dob = dob.strftime('%d/%m/%Y')
    formatted_tob = tob.strftime('%H:%M')
   # astro_api_url = f"https://api.vedicastroapi.com/v3-json/dosha/mangal-dosha?dob={formatted_dob}&tob={formatted_tob}&lat={latitude}&lon={longitude}&tz=5.5&api_key={api_key}&lang={lang}"
    astro_api_url = f"https://api.vedicastroapi.com/v3-json/{typ}/{selected_sub_option}?dob={formatted_dob}&tob={formatted_tob}&lat={lat}&lon={lon}&tz=5.5&api_key={api_key}&lang={lang}"
    if selected_sub_option == 'planet-report' or selected_sub_option == 'divisional-charts' or selected_sub_option == 'chart-image' or selected_sub_option == 'binnashtakvarga':
        print("inside-----------")
        astro_api_url = append_params(
            astro_api_url, selected_sub_option,  selected_planet, selected_div)
    print("astro_api_url", astro_api_url)
    return astro_api_url


if __name__ == "__main__":
    main()
