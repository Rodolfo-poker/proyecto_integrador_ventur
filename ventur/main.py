"""Punto de entrada de Ventur.

    python main.py
"""
from controllers.app_controller import AppController


def main():
    AppController().iniciar()


if __name__ == "__main__":
    main()
