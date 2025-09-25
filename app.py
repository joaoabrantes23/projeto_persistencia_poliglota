import streamlit as st
import pandas as pd
from db_sqlite import init_db, inserir_cidade, listar_cidades, buscar_cidade_por_id
from db_mongo import inserir_local, listar_locais_por_cidade_id, listar_todos_locais, buscar_locais_no_raio
from geoprocessamento import filtrar_por_raio
from utils import SQLITE_PATH
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Persistência Poliglota - GeoApp", layout="wide")

init_db(SQLITE_PATH)

st.title("Persistência Poliglota (SQLite + MongoDB) — GeoApp")

with st.sidebar:
    st.header("Inserções")
    tab = st.radio("Tipo de cadastro", ["Cidade (SQLite)", "Local (MongoDB)"])

    if tab == "Cidade (SQLite)":
        nome = st.text_input("Nome da cidade")
        estado = st.text_input("Estado")
        pais = st.text_input("País", value="Brasil")
        lat = st.text_input("Latitude (opcional)")
        lon = st.text_input("Longitude (opcional)")
        if st.button("Salvar cidade"):
            latf = float(lat) if lat else None
            lonf = float(lon) if lon else None
            idc = inserir_cidade(nome.strip(), estado.strip(), pais.strip(), latf, lonf, SQLITE_PATH)
            st.success(f"Cidade inserida com id {idc}")

    else:
        st.subheader("Cadastrar local (MongoDB)")
        nome_local = st.text_input("Nome do local")
        cidades = listar_cidades(SQLITE_PATH)
        cidade_options = {f"{c['nome']} ({c['estado']})": c['id'] for c in cidades}
        selected_cidade_nome = None
        selected_cidade_id = None
        if cidade_options:
            selected_nome = st.selectbox("Cidade", options=list(cidade_options.keys()))
            selected_cidade_id = cidade_options[selected_nome]
            selected_cidade_nome = selected_nome.split(" (")[0]
        else:
            st.warning("Cadastre pelo menos uma cidade antes de cadastrar locais.")
        descricao = st.text_area("Descrição")
        lat = st.text_input("Latitude")
        lon = st.text_input("Longitude")
        if st.button("Salvar local"):
            try:
                latf = float(lat)
                lonf = float(lon)
            except Exception:
                st.error("Latitude/Longitude inválidos")
            else:
                doc = {
                    "nome_local": nome_local.strip(),
                    "cidade_id": selected_cidade_id,
                    "cidade_nome": selected_cidade_nome,
                    "coordenadas": {"latitude": latf, "longitude": lonf},
                    "descricao": descricao.strip(),
                }
                idd = inserir_local(doc)
                st.success(f"Local inserido com id {idd}")

st.markdown("---")
cols = st.columns((1, 2))

with cols[0]:
    st.header("Consulta integrada")
    cidades = listar_cidades(SQLITE_PATH)
    df_cidades = pd.DataFrame(cidades)
    selected = None
    if not df_cidades.empty:
        df_cidades_display = df_cidades[["id", "nome", "estado", "pais"]]
        st.dataframe(df_cidades_display)
        selected_id = st.selectbox("Selecionar cidade (por id)", options=[None] + df_cidades["id"].tolist())
        if selected_id:
            selected = buscar_cidade_por_id(selected_id)
            st.write("Cidade selecionada:")
            st.json(selected)
            locais = listar_locais_por_cidade_id(selected["id"])
            if locais:
                st.subheader("Locais na cidade")
                st.table(pd.DataFrame(locais))
                lats = [d['coordenadas']['latitude'] for d in locais if d.get('coordenadas')]
                lons = [d['coordenadas']['longitude'] for d in locais if d.get('coordenadas')]
                if lats and lons:
                    center = [sum(lats)/len(lats), sum(lons)/len(lons)]
                    m = folium.Map(location=center, zoom_start=12)
                    for d in locais:
                        c = d.get('coordenadas') or {}
                        if c.get('latitude') is None or c.get('longitude') is None:
                            continue
                        popup = f"<b>{d.get('nome_local')}</b><br/>{d.get('cidade_nome')}<br/>{d.get('descricao','')}"
                        folium.Marker(location=[c['latitude'], c['longitude']], popup=popup).add_to(m)
                    st_folium(m, width=700, height=500)
    else:
        st.info("Nenhuma cidade cadastrada. Cadastre pela barra lateral.")

    st.markdown("---")
    st.header("Filtro por coordenada / raio")
    lat = st.text_input("Latitude (ex: -7.11532)", key="lat_input")
    lon = st.text_input("Longitude (ex: -34.861)", key="lon_input")
    raio_km = st.number_input("Raio (km)", value=10.0, min_value=0.1, key="raio_input")
    if "proximos" not in st.session_state:
        st.session_state.proximos = []
        st.session_state.origem = None
        st.session_state.raio = None

    if st.button("Buscar proximidade"):
        try:
            latf = float(lat)
            lonf = float(lon)
        except Exception:
            st.error("Lat/Lon inválidos")
        else:
            candidatos = buscar_locais_no_raio(latf, lonf, max(raio_km, 1.0))
            proximos = filtrar_por_raio((latf, lonf), candidatos, raio_km)
            st.session_state.proximos = proximos
            st.session_state.origem = (latf, lonf)
            st.session_state.raio = raio_km

    if st.session_state.proximos:
        st.write(f"Encontrados {len(st.session_state.proximos)} locais dentro de {st.session_state.raio} km")
        st.table(pd.DataFrame(st.session_state.proximos))
        latf, lonf = st.session_state.origem
        m = folium.Map(location=[latf, lonf], zoom_start=12)
        folium.Marker(location=[latf, lonf], tooltip="Origem", icon=folium.Icon(color='red')).add_to(m)
        for p in st.session_state.proximos:
            c = p['coordenadas']
            folium.Marker(location=[c['latitude'], c['longitude']], tooltip=p['nome_local']).add_to(m)
        st_folium(m, width=700, height=500)

with cols[1]:
    st.header("Mapa — todos os locais (MongoDB)")
    todos = listar_todos_locais()
    if todos:
        lats = [d['coordenadas']['latitude'] for d in todos if d.get('coordenadas')]
        lons = [d['coordenadas']['longitude'] for d in todos if d.get('coordenadas')]
        if lats and lons:
            center = [sum(lats)/len(lats), sum(lons)/len(lons)]
        else:
            center = [0, 0]
        m = folium.Map(location=center, zoom_start=5)
        for d in todos:
            c = d.get('coordenadas') or {}
            if c.get('latitude') is None or c.get('longitude') is None:
                continue
            popup = f"<b>{d.get('nome_local')}</b><br/>{d.get('cidade_nome')}<br/>{d.get('descricao','')}"
            folium.Marker(location=[c['latitude'], c['longitude']], popup=popup).add_to(m)
        st_folium(m, width=900, height=700)
    else:
        st.info("Nenhum local no MongoDB. Cadastre pela barra lateral.")

st.markdown("---")