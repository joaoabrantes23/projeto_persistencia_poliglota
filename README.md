# Projeto Persistência Poliglota (SQLite + MongoDB) + GeoApp (Streamlit)

Aplicação didática que mostra como usar persistência poliglota: dados tabulares (SQLite) e documentos JSON com coordenadas (MongoDB).


```bash
python -m venv .venv
source .venv/bin/activate
.\.venv\Scripts\activate 

pip install -r requirements.txt
```

## Execução

```
streamlit run app.py
```

## Funcionalidades

- Cadastro de cidades no SQLite
- Cadastro de locais no MongoDB
- Consulta integrada
- Consulta de proximidade
- Visualização em mapa com Folium
