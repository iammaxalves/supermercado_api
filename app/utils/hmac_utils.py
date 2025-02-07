import hashlib
import hmac
import base64

# Chave secreta usada para assinar as mensagens (NUNCA exponha isso publicamente)
SECRET_KEY = "minha_chave_secreta_super_segura"

def generate_hmac(data: str) -> str:
    """
    Gera um HMAC baseado nos dados da requisição.
    """
    # Criar um objeto HMAC usando a chave secreta e o algoritmo SHA256
    hmac_obj = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256)
    
    # Retornar o HMAC codificado em base64 para facilitar o transporte
    return base64.b64encode(hmac_obj.digest()).decode()


def verify_hmac(data: str, received_hmac: str) -> bool:
    """
    Verifica se o HMAC recebido corresponde ao HMAC gerado pelo servidor.
    """
    expected_hmac = generate_hmac(data)
    
    # Verifica se o HMAC recebido é igual ao esperado
    return hmac.compare_digest(expected_hmac, received_hmac)
