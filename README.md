# Hash - Aplicativo de vendas

## Sumário
- [Visão Geral](#visão-geral)
  - [Funcionamento do aplicativo](#funcionamento-do-aplicativo)

## Visão Geral

Hash é um aplicativo para gerenciamento de vendas de uma empresa. A situação é a seguinte: uma empresa hipotética realiza vendas de produtos para supermercados e com o aplicativo os funcionários da empresa podem realizar suas vendas, podem acompanhar as vendas de outros funcionários da empresa e também ter uma visão geral de todas as vendas da empresa. 

O aplicativo foi completamente construído com Python.

## Funcionamento do aplicativo

Nesta seção estão disponíveis algumas capturas de tela e uma descrição de como cada seção do aplicativo funciona

**Tela de Login/Criar Conta -** Tela inicial ao abrir o aplicativo pela primeira vez. Permite que o funcionário da empresa crie sua conta no aplicativo ou realize o login, caso já tenha uma conta e tenha realizado o logout em algum momento

<div align="center">

![Tela de login/criar conta](/images/login-criar-conta.png)

</div>

**Tela Inicial -** Após fazer o login ou criar uma nova conta, o usuário é redirecionado para a página inicial que contém o seu total de vendas e todas as vendas individuais com seus respectivos valores, data da venda e o cliente para o qual a venda foi realizada. Caso o usuário ainda não tenha realizado nenhuma venda, o total de vendas estará como R$0 (o valor é atualizado dinamicamente sempre que o usuário realiza uma nova venda) e as vendas individuais estarão vazias. Na parte inferior da tela existem três botões que são (da esquerda para a direita): realizar uma nova venda, acompanhar outro usuário, menu de ajustes. 

<div align="center">

![Tela inicial](/images/homepage.png)

</div>

**Realizar Nova Venda -** Ao clicar no botão de realizar ma nova venda o usuário é redirecionado para esta página. Ela contém dois banners horizontalmente roláveis. O primeiro com os clientes que estão disponíveis e o segundo com os produtos disponíveis para venda. A parte inferior é uma seção para que o usuário especifique a quantidade do produto a ser vendido, a unidade (unidade, quilogramas, litros) e o valor total da venda. Ao realizar a venda, o usuário é automaticamente redirecionado para a tela inicial, onde um novo banner com a sua venda mais recente terá sido criado e o total de vendas terá sido atualizado.

<div align="center">

![Realizar Venda](/images/add-venda.png)

</div>

**Acompanhar Vendedor -** O usuário tem a possibilidade de acompanhar outros vendedores da empreasa. Ao clicar no botão acompanhar outro usuário, o usuário é redirecionado para sua lista de vendedores que já está acompanhando

<div align="center">

![Acompanhar Vendedor](/images/acompanhar-vendedor.png)

</div>

**Perfil Outro Vendedor -** Quando o usuário clica no perfil de algum outro vendedor, o perfil do vendedor em questão será aberto, contendo o seu total de vendas tal como suas vendas individuais.

<div align="center">

![Outro Vendedor](/images/perfil-outro-vendedor.png)

</div>

**Página de Ajustes -** Ao clicar no botão de ajustes, o usuário é redirecionado para a página de configurações. A página possui três opções: "mudar foto de perfil", "acompanhar vendedor" e "ver todas as vendas".

<div align="center">

![Página de Ajustes](/images/pagina-ajustes.png)

</div>

**Mudar Foto de Perfil -** Permite que o usuário selecione uma nova foto para o seu perfil. Ao mudar a foto, o usuário é automaticamente redirecionado para a página de ajustes novamente.

<div align="center">

![Mudar Foto de Perfil](/images/mudar-foto-perfil.png)

</div>

**Acompanhar Vendedor -** Ao clicar no botão "Acompanhar Vendedor" o usuário é redirecionado para a tela abaixo. Nela é necessário que o usuário informe o ID de outro vendedor da equipe para que ele possa acompanhar as suas vendas. Ao adicionar o vendedor a página "acompanhar vendedor" é automaticamente atualizada.

<div align="center">

![Adicionar outro Vendedor](/images/adicionar-vendedor.png)

</div>

**Ver Todas as Vendas -** Ao clicar neste botão, o usuário é redirecionado para a página que contém todas as vendas da empresa e o total de vendas. É a soma das vendas de todos os usuários.

<div align="center">

![Ver Todas as Vendas](/images/ver-todas-vendas.png)

</div>






