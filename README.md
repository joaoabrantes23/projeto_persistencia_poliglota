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

## Como usar?
#### Cadastre uma cidade
<img width="837" height="703" alt="image" src="https://github.com/user-attachments/assets/964bf065-f702-425d-a1d4-d166ae7a140f" />

#### Clique em 'Local (mongodb)'
<img width="246" height="131" alt="image" src="https://github.com/user-attachments/assets/b1f663b2-8378-4e95-8984-6487e0c4289b" />

#### Cadastre um local

<img width="370" height="750" alt="image" src="https://github.com/user-attachments/assets/0d5a0640-c019-4655-9ccf-9db2fc9629d8" />

#### Pesquise locais por proximidade utilizando coordenadas (latitude e longitude)

<img width="577" height="407" alt="image" src="https://github.com/user-attachments/assets/b440415d-220b-443f-9eb0-a036c2a4881b" />

#### Caso encontrado algum local, mostrará uma tabela e sua posição no mapa

<img width="553" height="753" alt="image" src="https://github.com/user-attachments/assets/1abeb64a-dc7d-4c44-b362-782703f9b078" />

<img width="563" height="547" alt="image" src="https://github.com/user-attachments/assets/0687ce10-10f6-40e8-b53c-a9639c6ae739" />





