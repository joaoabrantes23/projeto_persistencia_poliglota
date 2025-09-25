from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "projeto_poliglota")

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_db():
    return get_client()[MONGO_DB]


def get_collection(name: str) -> Collection:
    return get_db()[name]


def inserir_local(document: Dict[str, Any], collection_name: str = "locais") -> str:
    col = get_collection(collection_name)
    res = col.insert_one(document)
    return str(res.inserted_id)


def listar_locais_por_cidade_id(cidade_id: int, collection_name: str = "locais") -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    docs = list(col.find({"cidade_id": cidade_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def listar_todos_locais(collection_name: str = "locais") -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    docs = list(col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def buscar_locais_no_raio(lat: float, lon: float, raio_km: float, collection_name: str = "locais") -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    delta = raio_km / 111.0
    min_lat, max_lat = lat - delta, lat + delta
    min_lon, max_lon = lon - delta, lon + delta
    cursor = col.find({
        "coordenadas.latitude": {"$gte": min_lat, "$lte": max_lat},
        "coordenadas.longitude": {"$gte": min_lon, "$lte": max_lon},
    })
    docs = list(cursor)
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs
