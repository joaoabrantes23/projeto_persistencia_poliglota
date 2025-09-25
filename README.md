# Projeto Persistência Poliglota (SQLite + MongoDB) + GeoApp (Streamlit)

Aplicação didática que mostra como usar persistência poliglota: dados tabulares (SQLite) e documentos JSON com coordenadas (MongoDB).

Aplicação desenvolvida por Arthur Henrique Lima e João Victor Abrantes, para a cadeira de tendências em ciência da computação, ministrada pelo professor Ricardo Roberto.

## Arquitetura
Monólito modular que integra os dois banco de dados em uma única aplicação. Separado queries e bancos por módulos e utilizado em conjunto nas telas

## Instalando dependencias
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
