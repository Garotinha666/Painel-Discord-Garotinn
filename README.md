## **VaiXourar Bot Manager**

O **VaiXourar Bot Manager** é uma ferramenta de gerenciamento e controle para bots no Discord. Com este bot, você pode realizar várias operações administrativas em servidores, como criar canais, excluir canais, enviar mensagens em massa, banir membros e muito mais. O bot foi projetado para ser uma solução poderosa e prática para administradores de servidores do Discord que precisam de recursos automatizados para gerenciamento em larga escala.

### **Funcionalidades Principais**

1. **Criação e Exclusão de Canais**

   * O bot permite a criação e exclusão em massa de canais em servidores do Discord. Isso é útil para admins que precisam de operações rápidas em vários canais.

2. **Spam em Canais**

   * É possível enviar mensagens em massa para todos os canais de texto de um servidor. Ideal para comunicações rápidas ou testes.

3. **Banimento em Massa**

   * O bot tem a capacidade de banir todos os membros (exceto bots e o dono do servidor) com um simples comando.

4. **Modificação de Nicks**

   * Permite mudar os nicks de todos os membros do servidor, com exceção de bots e do dono.

5. **Auditoria e Permissões**

   * O bot pode listar as permissões dos membros e também mostrar os logs de auditoria, permitindo um controle completo sobre o que ocorre no servidor.

6. **Webhooks e Banner**

   * O bot lista todas as informações dos webhooks configurados nos canais de texto do servidor e também exibe o banner do servidor.

7. **Gerenciamento de Bots**

   * A ferramenta permite o registro, remoção e utilização de múltiplos bots por usuário. O usuário pode escolher qual bot controlar em cada sessão de operação.

8. **Painel de Controle**

   * O bot inclui um painel interativo de controle via linha de comando, onde o usuário pode escolher diversas opções de administração para um servidor, como criação de canais, banimento de membros, alteração do nome do servidor, e muito mais.

9. **Personalização de Tema**

   * O bot permite que os usuários personalizem o tema visual do seu perfil, escolhendo cores diferentes para o prompt e interface.

### **Funcionalidades Avançadas**

* **Suporte a múltiplos bots:** O bot pode gerenciar múltiplos bots, com a possibilidade de cadastrar novos bots e utilizá-los em diferentes servidores.
* **Interface interativa:** O bot oferece um menu interativo onde o usuário pode escolher diversas opções de administração do servidor e bot.
* **Controle de raids:** O bot facilita a execução de raids (ações em massa), como exclusão de canais e spam de mensagens.

### **Estrutura do Código**

O código é estruturado de maneira modular e utiliza as bibliotecas do Python, como `discord.py` para interação com a API do Discord, e `colorama` para a customização da interface com cores.

1. **Bibliotecas Importadas**

   * `discord`: Para interagir com a API do Discord e realizar ações no servidor.
   * `colorama`: Para aplicar cores ao terminal e melhorar a aparência da interface de linha de comando.
   * `json`: Para salvar e carregar os dados dos usuários e bots.
   * `os` e `time`: Para gerenciar o sistema de arquivos e criar delays no código.
   * `threading` e `asyncio`: Para realizar tarefas assíncronas e paralelizar operações como a atualização do título do terminal.

2. **Funções Principais**

   * **`atualizar_titulo()`**: Atualiza o título do terminal com informações sobre os usuários, raids e bots online.
   * **`load_data()` e `save_data()`**: Funções para carregar e salvar dados dos usuários e bots em um arquivo JSON.
   * **Funções de gerenciamento de servidor**: Incluem funções para excluir canais, criar canais, banir membros, enviar mensagens em massa, entre outras.

3. **Menu de Perfil e Inicialização**

   * O bot possui uma tela inicial onde o usuário pode criar ou usar um perfil existente. Cada perfil pode ter seus próprios bots registrados.
   * O menu do perfil permite ao usuário realizar ações como cadastrar novos bots, alterar o tema da interface ou verificar estatísticas do perfil.

4. **Painel de Controle Interativo**

   * O painel oferece uma série de opções para administração do servidor, como modificar o nome do servidor, listar permissões dos membros, criar ou excluir canais, e muito mais.

### **Como Usar**

1. **Instalação das Dependências**

   Antes de executar o bot, instale as dependências necessárias. Crie um ambiente virtual e instale as bibliotecas com o comando:

   ```bash
   pip install -r requirements.txt
   ```

   Certifique-se de ter as versões corretas das bibliotecas, principalmente a `discord.py`.

2. **Rodando o Bot**

   Para rodar o bot, basta iniciar o script Python. Ele pedirá que você insira um nome de usuário e escolher um tema para o perfil. Após isso, você poderá usar os bots cadastrados e executar as funcionalidades administrativas.

   ```bash
   python bot.py
   ```

3. **Cadastro de Bots**

   * O bot permite cadastrar múltiplos bots e controlá-los. Para cada bot, será necessário fornecer um **token** do Discord, o **nome** do bot e o **ID do servidor**.

4. **Comandos e Interação**

   * O bot funciona principalmente por meio de um menu de interface de linha de comando, onde o usuário escolhe as operações a serem realizadas. Você pode realizar tarefas como criar canais, banir membros, entre outras, interagindo com o menu do bot.

5. **Controle e Gerenciamento de Bots**

   * O bot oferece um sistema para gerenciar múltiplos bots em um único perfil de usuário. Isso facilita o controle de bots em vários servidores Discord ao mesmo tempo.

### **Configurações e Personalização**

* **Temas Personalizáveis**: O bot oferece temas de cores para personalizar a aparência da interface de linha de comando.

  Temas disponíveis:

  * **azul**
  * **verde**
  * **vermelho**
  * **roxo**
  * **padrão**

### **Requisitos**

* Python 3.x
* discord.py
* colorama

### **Notas de Segurança**

* **Uso Responsável**: Este bot possui funcionalidades que podem afetar gravemente servidores Discord, como a exclusão de canais e banimento de membros. Use com cautela e sempre tenha permissão do administrador do servidor.
* **Permissões do Bot**: Certifique-se de que o bot tenha as permissões adequadas para realizar as ações desejadas (como criar/excluir canais, banir membros, etc.).
