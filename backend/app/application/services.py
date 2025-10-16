from typing import Optional
from io import BytesIO

# Importa a entidade do domínio
from app.domain.entities import Imagem


class RemocaoFundoService:
    """
    Serviço de aplicação responsável por orquestrar a remoção de fundo de imagens.
    Processa imagens em memória sem salvar arquivos localmente.
    """
    def __init__(self, segmentador):
        """
        segmentador: instância de um serviço de segmentação (ex: U2NetService)
        """
        self.segmentador = segmentador

    def remover_fundo(self, imagem_bytes: bytes, formato_saida: str = "PNG") -> Optional[BytesIO]:
        """
        Orquestra a remoção de fundo da imagem processando em memória.
        
        Args:
            imagem_bytes: Bytes da imagem de entrada
            formato_saida: Formato da imagem de saída (PNG, JPEG, etc.)
        
        Returns:
            BytesIO contendo a imagem processada ou None se houver erro
        """
        resultado = self.segmentador.remover_fundo(imagem_bytes, formato_saida)
        return resultado