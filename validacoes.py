import re
#Importação da biblioteca re que é usada para validar os padroes dos inputs fornecidos do usuario


#Verifica se a string do email segue o padrao(caracteres antes do @ e se tem o dominio gmail e hotmail), e retorna um valor booleano
def emailValido(email):
    email = email.strip()
    if ' ' in email:
        return False
    padrao = r'^[\w\.-]+@(gmail\.com|hotmail\.com)$'
    return re.match(padrao, email)


#Verifica se a senha nao tem espaços, se tem no minimo 8 caracteres e se contem pelo menos 1 letra e 1 numero
def senhaValida(senha):
    if senha != senha.strip():
        return False
    if ' ' in senha:
        return False
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Za-z]', senha):
        return False
    if not re.search(r'[0-9]', senha):
        return False
    return True


#Verifica se a string contem apenas numeros e se é igual a 11(DDD+Numero)
def telefoneValido(telefone):
    return telefone.isdigit() and len(telefone) == 11
