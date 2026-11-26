from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Category:
    category_id: int
    name: str
    description: str = ""


@dataclass
class Course:
    course_id: int
    category_id: int
    name: str
    description: str
    workload_hours: int
    level: str
    price: float
    active: bool = True
    # Metadados auxiliares de apresentação na UI desktop
    summary: str = ""
    art_key: str = "ai"
    image_url: Optional[str] = None
    learnings: List[str] = field(default_factory=list)

    @property
    def formatted_price(self) -> str:
        value = f"{self.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {value}"

    @property
    def formatted_meta(self) -> str:
        return f"{self.workload_hours}H  •  {self.level.upper()}  •  ONLINE"

    @classmethod
    def from_dict(cls, data: dict) -> Course:
        return cls(
            course_id=int(data["id_curso"]),
            category_id=int(data.get("id_categoria", 1)),
            name=data.get("nome", ""),
            description=data.get("descricao", ""),
            workload_hours=int(data.get("carga_horaria", 0)),
            level=data.get("nivel", "Iniciante"),
            price=float(data.get("preco", 0.0)),
            active=bool(data.get("ativo", True)),
            summary=data.get("resumo") or data.get("descricao", ""),
            art_key=data.get("art_key", "ai"),
            image_url=data.get("imagem_url"),
            learnings=data.get("aprendizados") or [],
        )