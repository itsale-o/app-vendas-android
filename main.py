from kivy.app import App
from kivy.lang import Builder
from bannervenda import BannerVenda
from telas import *
from botoes import *
from functools import partial
from myfirebase import MyFirebase
from bannervendedor import BannerVendedor
from datetime import date
import requests
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
GUI = Builder.load_file("main.kv")


class MainApp(App):
    cliente = None
    produto = None
    unidade = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # carregar os avatares de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # carregar as fotos dos clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionar_clientes = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionar_clientes.ids["lista_clientes"]

        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}",
                                 on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        # carregar as fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionar_clientes = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionar_clientes.ids["lista_produtos"]

        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}",
                                 on_release=partial(self.selecionar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_produto, foto_produto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        # carregar a data
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        label_data = pagina_adicionar_vendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

        self.carregar_infos_usuarios()

    def carregar_infos_usuarios(self):
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()

            id_usuario, id_token = self.firebase.trocar_token(refresh_token)
            self.id_usuario = id_usuario
            self.id_token = id_token

            # info usuário
            requisicao = requests.get(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}.json?auth={self.id_token}")
            requisicao_json = requisicao.json()

            # foto de perfil usuario
            avatar = requisicao_json['avatar']
            self.avatar = avatar
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher o id único do usuário
            id_vendedor = requisicao_json['id_vendedor']
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID único: {id_vendedor}"

            # preencher o total de vendas do usuário
            total_vendas = requisicao_json['total_vendas']
            self.total_vendas = total_vendas
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"

            # preencher equipe
            self.equipe = requisicao_json["equipe"]

            # informação de vendas do usuário
            try:
                vendas = requisicao_json['vendas']
                self.vendas = vendas
                pagina_homepage = self.root.ids["homepage"]
                lista_vendas = pagina_homepage.ids["lista_vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"],
                                         unidade=venda["unidade"], quantidade=venda["quantidade"])
                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                print(excecao)

            equipe = requisicao_json["equipe"]
            lista_equipe = equipe.split(",")
            pagina_listavendedores = self.root.ids["listarvendedorespage"]
            lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)

            self.mudar_tela("homepage")
        except:
            pass

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"
        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}.json?auth={self.id_token}",
                                    data=info)

        self.mudar_tela("ajustespage")

    def adicionar_vendedor(self, id_vendedor_adicionado):
        link = f'https://app-vendas-hash-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_json = requisicao.json()

        pagina_adicionar_vendedor = self.root.ids["adicionarvendedorpage"]
        mensagem_texto = pagina_adicionar_vendedor.ids["mendagem_outro_vendedor"]

        if requisicao_json == {}:
            mensagem_texto.text = "Ususário não encontrado"
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Vendedor já faz parte da sua equipe"
            else:
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}.json?auth={self.id_token}",
                               data=info)
                mensagem_texto.text = "Vendedor adicionado com sucesso à equipe"
                # adicionar um novo banner na de vendedores
                pagina_listavendedores = self.root.ids["listarvendedorespage"]
                lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

    def selecionar_cliente(self, foto, *args):
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]
        self.cliente = foto.replace(".png", "")

        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_produto(self, foto, *args):
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]
        self.produto = foto.replace(".png", "")

        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        self.unidade = id_label.replace("unidade_", "")

        pagina_adicionar_vendas.ids["unidade_kg"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidade_unidade"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidade_litros"].color = (1, 1, 1, 1)

        pagina_adicionar_vendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade

        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        data = pagina_adicionar_vendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionar_vendas.ids["preco_total"].text
        quantidade = pagina_adicionar_vendas.ids["quantidade_total"].text

        if not cliente:
            pagina_adicionar_vendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)
        if not produto:
            pagina_adicionar_vendas.ids["label_selecione_produto"].color = (1, 0, 0, 1)
        if not unidade:
            pagina_adicionar_vendas.ids["unidade_kg"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidade_unidade"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidade_litros"].color = (1, 0, 0, 1)
        if not preco:
            pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        if not quantidade:
            pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        # depois que o usuário preencheu todas as informações
        if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade == float)):
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            info = (f'{{"cliente": "{cliente}", '
                    f'"produto": "{produto}",'
                    f'"foto_cliente": "{foto_cliente}",'
                    f'"foto_produto": "{foto_produto}",'
                    f'"data": "{data}",'
                    f'"unidade": "{unidade}",'
                    f'"preco": "{preco}",'
                    f'"quantidade": "{quantidade}"}}')

            requests.post(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}/vendas.json?auth={self.id_token}",
                          data=info)

            banner = BannerVenda(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto,
                                 data=data, preco=preco, quantidade=quantidade, unidade=unidade)

            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            requisicao = requests.get(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}/total_vendas.json?auth={self.id_token}")
            total_vendas = float(requisicao.json())
            total_vendas += preco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}.json?auth={self.id_token}",
                           data=info)

            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"
            self.mudar_tela("homepage")

        self.cliente = None
        self.produto = None
        self.unidade = None

    def carregar_todas_vendas(self):
        pagina_todasvendas = self.root.ids["todasvendaspage"]
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]

        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)

        # pegar informações da empresa
        requisicao = requests.get(f'https://app-vendas-hash-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_json = requisicao.json()

        # foto de perfil usuario
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/hash.png"

        total_vendas = 0
        for id_usuario in requisicao_json:
            try:
                vendas = requisicao_json[id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"])
                    banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"],
                                         foto_cliente=venda["foto_cliente"], foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"],
                                         quantidade=venda["quantidade"], unidade=venda["unidade"])
                    lista_vendas.add_widget(banner)
            except:
                pass

        # preencher o total de vendas do usuário
        pagina_todasvendas.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"

        # redirecionar para pagina todasvendaspage
        self.mudar_tela("todasvendaspage")

    def sair_todas_vendas(self, id_tela):
        requisicao = requests.get(f"https://app-vendas-hash-default-rtdb.firebaseio.com/{self.id_usuario}.json?auth={self.id_token}")
        requisicao_json = requisicao.json()

        # foto de perfil usuario
        avatar = requisicao_json['avatar']
        self.avatar = avatar
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        self.mudar_tela(id_tela)

    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):
        try:
            vendas = dic_info_vendedor["vendas"]
            pagina_vendasoutrovendedor = self.root.ids["vendasoutrovendedorpage"]
            lista_vendas = pagina_vendasoutrovendedor.ids["lista_vendas"]

            # limpar vendas anteriores
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)

            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"],
                                     foto_cliente=venda["foto_cliente"], foto_produto=venda["foto_produto"],
                                     data=venda["data"], preco=venda["preco"],
                                     quantidade=venda["quantidade"], unidade=venda["unidade"])
                lista_vendas.add_widget(banner)
        except:
            pass

        # preencher total de vendas
        total_vendas = dic_info_vendedor["total_vendas"]
        pagina_vendasoutrovendedor.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R$ {total_vendas}[/b]"

        # preencher foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]
        avatar = dic_info_vendedor["avatar"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        self.mudar_tela("vendasoutrovendedorpage")


MainApp().run()
