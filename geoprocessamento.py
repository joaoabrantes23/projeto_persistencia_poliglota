from geopy.distance import geodesic
from typing import Tuple, List, Dict, Any


def distancia_km(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return geodesic(p1, p2).kilometers


def filtrar_por_raio(ponto: Tuple[float, float], locais: List[Dict[str, Any]], raio_km: float) -> List[Dict[str, Any]]:
    resultado = []
    for l in locais:
        c = l.get("coordenadas") or {}
        if c.get("latitude") is None or c.get("longitude") is None:
            continue
        d = distancia_km(ponto, (c["latitude"], c["longitude"]))
        l_copy = dict(l)
        l_copy["dist_km"] = d
        if d <= raio_km:
            resultado.append(l_copy)
    resultado.sort(key=lambda x: x["dist_km"])
    return resultado
