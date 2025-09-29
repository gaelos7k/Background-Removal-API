from typing import Optional

# Importa a entidade do domínio
from app.domain.entities import Imagem


class RemocaoFundoService:
    """
    Serviço de aplicação responsável por orquestrar a remoção de fundo de imagens.
    """
    def __init__(self, segmentador):
        """
        segmentador: instância de um serviço de segmentação (ex: U2NetService)
        """
        self.segmentador = segmentador

    def remover_fundo(self, imagem: Imagem, caminho_saida: str) -> Optional[Imagem]:
        """
        Orquestra a remoção de fundo da imagem.
        - imagem: objeto Imagem de entrada
        - caminho_saida: onde salvar a imagem sem fundo
        Retorna um novo objeto Imagem com o caminho do arquivo de saída.
        """
        sucesso = self.segmentador.remover_fundo(imagem.caminho_arquivo, caminho_saida)
        if sucesso:
            # Cria novo objeto Imagem para o resultado
            return Imagem(caminho_arquivo=caminho_saida)
        return None