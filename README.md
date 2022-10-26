# Clonechat Telegram Colab

Para utilizar o [clonechat no colab](https://colab.research.google.com/github/Drrivao/Clonechat-Telegram-Colab/blob/master/Clonechat_Telegram_Colab.ipynb), execute a 1º célula clicando ou apertando no símbolo de "play" do lado esquerdo dela e siga as instruções abaixo.

### Inserindo credenciais e configurando o modo bot

Na 2º célula:

1) Substitua o texto `PUT YOUR API ID HERE` pela sua [api id](https://t.me/c/1297554030/69);
2) Troque o texto `PUT YOUR API HASH HERE` pela sua [api hash](https://t.me/c/1297554030/69);
3) Se quiser clonar em modo bot, altere o texto `PUT YOUR BOT TOKEN HERE` para o [token](https://t.me/BotFather) do seu bot;
4) Execute a célula.

>Atenção: Insira na caixa de diálogo que será aberta somente o seu número de telefone para realizar a autenticação 2FA. Ignore o aviso da mensagem para colocar o bot token. Segue um exemplo de como inserir o nº: 556795874621


### Adicionando as flags

* A 3º célula contém alguns campos a serem preenchidos, indicando as flags para a execução do script. Segue a descrição de cada um:


      ORIG               Nome do canal/grupo de origem

      DEST               Nome do canal/grupo de destino

      MODE {user,bot}    Modo a ser utilizado

      NEW {1,2}          1 para iniciar uma nova tarefa e 2 para retomar

      TYPE               Listar os tipos de mensagens a serem clonadas. Ex.:
                         para documentos e vídeos: 3,8 

                         Opções disponíveis: 

                         0 = Todos os arquivos
                         1 = Fotos
                         2 = Mensagens de texto
                         3 = Documentos (pdf, zip, rar...)
                         4 = Figurinhas (Stickers)
                         5 = Animações
                         6 = Arquivos de áudio (mp3)
                         7 = Mensagens de voz
                         8 = Vídeos
                         9 = Enquetes

      LIMIT              Limite de encaminhamento de mensagens

      QUERY              Filtro de mensagens

* Por fim, substitua os textos `NOME DO CANAL PARA CLONAR` e `NOME DO CANAL DE DESTINO` pelos nomes dos canais de origem/destino. Ou insira somente o nome do canal de origem e selecione a opção "auto" no campo "DEST" para que o clonechat crie um novo canal automaticamente.

>Atenção: o Telegram limita para cada usuário a criação de até 50 canais por dia. Veja mais mais sobre esse e outros limites neste [site](https://limits.tginfo.me/en). Ademais, lembre-se de inserir os nomes dos canais entre aspas simples ou duplas, conforme encontra-se no exemplo da célula.

* Digite o valor 0 para "LIMIT" se deseja encaminhar todas as mensagens do chat de origem. Se não, coloque o número máximo de encaminhamentos desejado.

* Em "QUERY" coloque entre as aspas simples ou duplas um nome para filtrar as mensagens a serem encaminhadas. Por exemplo, escreva "python" para encaminhar as mensagens que contêm esse termo. Caso precise encaminhar todas as mensagens, coloque "all".

*Se você receber o aviso: "Confirm the data export request first.", busque pela mesma notificação em que foi recebida a mensagem com o código de verificação. Logo abaixo dela haverá uma mensagem requisitando a autorização para exportar dados para permitir que o clonechat possa ler o histórico do canal a ser clonado e filtrar as mensagens úteis, tornando o processo muito mais eficiente. Então, basta selecionar a opção "Allow".*

### Notas

* Vale ressaltar que o colab possui uma [cota](https://research.google.com/colaboratory/faq.html#idle-timeouts) por tempo de atividade. Sendo necessário, portanto, salvar os seus arquivos do clonechat em algum local de armazenamento fora dele. Por isso, esses são salvos dentro de uma pasta chamada `Clonechat-Telegram-Colab` no seu Google Drive.

* A 1º célula deve ser executada sempre que o colab der o "reset" após atingir o limite da cota.

* O modo bot está disponível somente para canais em que você é um administrador.

* As configurações de delay podem ser modificadas no arquivo `config.ini` dentro da pasta do programa. Contudo, o mínimo recomendado para a execução do clonechat em modo user é de 10 segundos. Valores menores que esse podem acarretar em banimento de sua conta permanentemente por flood.

* É possível criar uma fila de canais para clonar, basta copiar a última célula e preenchê-la com os novos valores desejados para as flags. Contudo, não inicie mais de uma instância do clonechat na mesma conta e não utilize as mesmas credenciais para outras contas.

* Em alguns celulares pode não ser possível realizar a etapa de autenticação com a sua conta no Telegram pelo colab, sendo necessário que seja feita, primeiramente, no navegador de uma máquina local. Outra alternativa é enviar para dentro da pasta `Clonechat-Telegram-Colab` uma sessão já salva com o arquivo `user.session`.

### Executando localmente

* Caso queira utilizar o programa em seu ambiente desktop, baixe o repositório e rode no terminal o comando abaixo.

```
pip install pyrogram tgcrypto && python menu.py
```

### Créditos

- [Repositório oficial](https://github.com/apenasrr/clonechat)
- Tutorial em [texto](https://upolar.github.io/clonechats-docs/) do clonechat oficial

### Erros frequentes

* [Método channels.editAdmin](https://core.telegram.org/method/channels.editAdmin#bots-can-use-this-method)

```
pyrogram.errors.exceptions.bad_request_400.FreshChangeAdminsForbidden: Telegram says: [400 FRESH_CHANGE_ADMINS_FORBIDDEN] - You can't change administrator settings in this chat because your session was logged-in recently (caused by "channels.EditAdmin")
```
```
pyrogram.errors.exceptions.not_acceptable_406.FreshChangeAdminsForbidden: Telegram says: [406 FRESH_CHANGE_ADMINS_FORBIDDEN] - You were just elected admin, you can't add or modify other admins yet (caused by "channels.EditAdmin")
```
Causa: possivelmente já tenha sido realizada uma tarefa de clonar o mesmo canal em uma sessão diferente do pyrogram no modo bot e, por isso, a API do Telegram rejeita a nova chamada.

Solução: Entre na sua conta do Telegram e siga este caminho: `Settings > Devices (or Privacy & Security > Active Sessions)`. Em "Active Sessions" desative todas as sessões ativas com os nomes "Cpython" ou "Pyrogram". Por fim, faça refaça a etapa de autenticação.

* [Método get_dialogs](https://docs.pyrogram.org/api/methods/get_dialogs#pyrogram.Client.get_dialogs)

```
AttributeError: 'NoneType' object has no attribute 'get_dialogs'
```
Causas: os títulos dos chats inseridos não existem ou você não participa deles. Além disso, pode não ter sido feita a autorização para 'Data export request' no seu telegram.