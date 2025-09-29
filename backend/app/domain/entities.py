from datetime import datetime
from typing import Optional


class Imagem:
    """
    Entidade que representa uma imagem utilizada no sistema.
    """

    def __init__(
        self,
        caminho_arquivo: str,
        formato: Optional[str] = None,
        tamanho_bytes: Optional[int] = None,
        largura: Optional[int] = None,
        altura: Optional[int] = None,
        data_upload: Optional[datetime] = None
    ):
        self.caminho_arquivo = caminho_arquivo  # Caminho local ou na nuvem
        self.formato = formato                  # Ex: 'jpg', 'png'
        self.tamanho_bytes = tamanho_bytes      # Tamanho do arquivo em bytes
        self.largura = largura                  # Largura em pixels
        self.altura = altura                    # Altura em pixels
        self.data_upload = data_upload or datetime.now()  # Data do upload

    def __repr__(self):
        return (
            f"<Imagem caminho='{self.caminho_arquivo}' formato='{self.formato}' "
            f"tamanho={self.tamanho_bytes}B {self.largura}x{self.altura} upload={self.data_upload}>"
        )