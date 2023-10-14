import requests

def getTokenWvetro():
    url ='https://sistema.wvetro.com.br/wvetro/rest/api/Integracao/ValidarUsuario?Licencaid=2479&Secusername=Matheus Florentino de Carvalho&Secuserpassword=123456'
    response = requests.get(url)
    responseData = response.json()
    return responseData['ValidaUsuario']['token']

