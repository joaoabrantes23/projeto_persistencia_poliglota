import sqlite3
from typing import List, Dict, Any

DEFAULT_DB = "projeto_poliglota.sqlite"

CREATE_CIDADES_TABLE = """
CREATE TABLE IF NOT EXISTS cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    estado TEXT NOT NULL,
    pais TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);
"""


def get_conn(path: str = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str = DEFAULT_DB) -> None:
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute(CREATE_CIDADES_TABLE)
    conn.commit()
    conn.close()


def inserir_cidade(nome: str, estado: str, pais: str, latitude: float | None = None, longitude: float | None = None, path: str = DEFAULT_DB) -> int:
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cidades (nome, estado, pais, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
        (nome, estado, pais, latitude, longitude),
    )
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def listar_cidades(path: str = DEFAULT_DB) -> List[Dict[str, Any]]:
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades ORDER BY pais, estado, nome")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def buscar_cidade_por_id(cidade_id: int, path: str = DEFAULT_DB) -> Dict[str, Any] | None:
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades WHERE id = ?", (cidade_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def buscar_cidade_por_nome(nome: str, path: str = DEFAULT_DB) -> List[Dict[str, Any]]:
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades WHERE nome LIKE ?", (f"%{nome}%",))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
