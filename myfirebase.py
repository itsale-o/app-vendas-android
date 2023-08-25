from kivy.app import App
import requests


class MyFirebase():
    API_KEY = "AIzaSyAsAVHJr92LAm0dLL-PebM6cq3J5jC3_xc"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_json = requisicao.json()

        if requisicao.ok:
            print("Usuário Criado")
            refresh_token = requisicao_json['refreshToken']
            id_usuario = requisicao_json['localId']
            id_token = requisicao_json['idToken']

            app = App.get_running_app()
            app.id_usuario = id_usuario
            app.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get(f"https://app-vendas-hash-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}")
            id_vendedor = req_id.json()

            link = f"https://app-vendas-hash-default-rtdb.firebaseio.com/{id_usuario}.json?auth={id_token}"
            info_usuario = f'{{"avatar": "hash.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f"https://app-vendas-hash-default-rtdb.firebaseio.com/.json?auth={id_token}", data=info_id_vendedor)

            app.carregar_infos_usuarios()
            app.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_json["error"]["message"]
            app = App.get_running_app()
            pagina_login = app.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)
        print(requisicao_json)

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }
        requisicao = requests.post(link, data=info)
        requisicao_json = requisicao.json()

        if requisicao.ok:
            refresh_token = requisicao_json['refreshToken']
            id_usuario = requisicao_json['localId']
            id_token = requisicao_json['idToken']

            app = App.get_running_app()
            app.id_usuario = id_usuario
            app.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            app.carregar_infos_usuarios()
            app.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_json["error"]["message"]
            app = App.get_running_app()
            pagina_login = app.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        requisicao = requests.post(link, data=info)
        requisicao_json = requisicao.json()
        id_usuario = requisicao_json["user_id"]
        id_token = requisicao_json["id_token"]
        return id_usuario, id_token
