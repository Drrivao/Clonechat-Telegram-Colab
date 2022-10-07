# Clonechat Telegram Colab

Para utilizar o [clonechat no colab](https://colab.research.google.com/github/Drrivao/Clonechat-Telegram-Colab/blob/master/Clonechat_Telegram_Colab.ipynb), execute a 1º célula clicando ou apertando no símbolo de "play" do lado esquerdo dela e siga as instruções abaixo.

### Inserindo credenciais e configurando o modo bot

Na 2º célula:

1) Substitua o texto `PUT YOUR API ID HERE` pela sua [api id](https://t.me/c/1297554030/69);
2) Troque o texto `PUT YOUR API HASH HERE` pela sua [api hash](https://t.me/c/1297554030/69);
3) Se quiser clonar em modo bot, altere o texto `PUT YOUR BOT TOKEN HERE` para o [token](https://t.me/BotFather) do seu bot;
4) Execute a célula.

>Atenção \
Uma caixa de diálogo será aberta para inserir o seu número de telefone para realizar a autenticação 2FA. Não insira outro dado além desse. Segue um exemplo de como inserir o nº: 556795874621


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


* Por fim, substitua os textos `NOME DO CANAL PARA CLONAR` e `NOME DO CANAL DE DESTINO` pelos nomes dos canais de origem/destino. Ou insira somente o nome do canal de origem e deixe o campo de "DEST" vazio para que o clonechat crie um novo canal automaticamente.

**Atenção: o Telegram limita para cada usuário a criação de até 50 canais por dia. Veja mais mais sobre esse e outros limites neste [site](https://limits.tginfo.me/en). Ademais, lembre-se de inserir os nomes dos canais entre aspas simples ou duplas, conforme encontra-se no exemplo da célula.**

### Notas

* Vale ressaltar que o colab possui uma [cota](https://research.google.com/colaboratory/faq.html#idle-timeouts) por tempo de atividade. Sendo necessário, portanto, salvar os seus arquivos do clonechat em algum local de armazenamento fora dele. Por isso, esses são salvos dentro de uma pasta chamada `Clonechat-Telegram-Colab` no seu Google Drive.

* A 1º célula deve ser executada sempre que o colab der o "reset" após atingir o limite da cota.

* O modo bot está disponível somente para canais em que você é um administrador.

* As configurações de delay podem ser modificadas, contudo, o mínimo recomendado para a execução do clonechat em modo user é de 25 segundos. Valores menores que esse podem acarretar em banimento de sua conta permanentemente por flood.

* É possível criar uma fila de canais para clonar, basta copiar a última célula e preenchê-la com os novos valores desejados para as flags. Contudo, não inicie mais de uma instância do clonechat na mesma conta e não utilize as mesmas credenciais para outras contas.

* Na primeira vez ao utilizar o clonechat, é preciso fazer a autenticação com a sua conta no Telegram, então será aberta uma caixa de diálogo para você inserir o seu número de telefone e, em seguida, o código de verificação. Em alguns celulares pode não ser possível realizar essa etapa pelo colab, sendo necessário que seja feita, primeiramente, no navegador de uma máquina local. Outra alternativa é enviar para dentro da pasta `Clonechat-Telegram-Colab` uma sessão já salva com o arquivo `user.session`.

* Caso queira utilizar o clonechat na sua máquina local, baixe-o no [repositório oficial](https://github.com/apenasrr/clonechat) e [clique aqui](https://upolar.github.io/clonechats-docs/) para ver o tutorial completo.

### Erros frequentes

* [Método channels.editAdmin](https://core.telegram.org/method/channels.editAdmin#bots-can-use-this-method)

      1) pyrogram.errors.exceptions.bad_request_400.FreshChangeAdminsForbidden: Telegram says: [400 FRESH_CHANGE_ADMINS_FORBIDDEN] - You can't change administrator settings in this chat because your session was logged-in recently (caused by "channels.EditAdmin")
      2) pyrogram.errors.exceptions.not_acceptable_406.FreshChangeAdminsForbidden: Telegram says: [406 FRESH_CHANGE_ADMINS_FORBIDDEN] - You were just elected admin, you can't add or modify other admins yet (caused by "channels.EditAdmin")

Causa: possivelmente já tenha sido realizada uma tarefa de clonar o mesmo canal em uma sessão diferente do pyrogram no modo bot e, por isso, a API do Telegram rejeita a nova chamada, sendo necessário clonar em modo user no novo cliente.

Solução: a única forma de resolver esse problema (sem modificações no script) é recuperando o arquivo `user.session` dessa sessão antiga e excluindo o `user.session` existente na pasta `Clonechat-Telegram-Colab`.
