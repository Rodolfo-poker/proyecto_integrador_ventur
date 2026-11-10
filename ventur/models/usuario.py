"""Modelo: usuario de la sesión y su plan."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    nombre: str


@dataclass(frozen=True)
class Usuario:
    nombre: str
    plan: Plan
