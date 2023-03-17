# Auto Forward Messages

> Projeto inspirado no [clonechat](https://github.com/apenasrr/clonechat).

### Como usar

Primeiro, obtenha as suas [credenciais](https://upolar.github.io/clonechats-docs/#obtendo-credenciais-da-api-do-telegram) e siga o [tutorial](https://t.me/auto_forward_messages_drrivao).


### Utilizando filtros e outros argumentos

- MODE: "user" é o modo de clonagem mais lenta e "bot" o mais rápido, porém é necessário que o usuário seja um administrador dos canais ou dos grupos de origem e de destino.
- FILTER: filtra as mensagens pelo tipo. Para escolher múltiplos tipos, coloque-os separados por vírgulas, por exemplo: "photo,document".
- QUERY: filtra as mensagens que contêm determinados termos, por exemplo, inserindo "python" o programa irá encaminhar somente as mensagens com o termo "python" na descrição, no texto ou no nome do arquivo.
- LIMIT: define um limite para a quantidade de mensagens a serem encaminhadas.
- RESUME: o programa retoma um processo de clonagem anterior.
- RESTART: o programa será reiniciado automaticamente a cada 4 horas para encaminhar novas mensagens do chat de origem.

### Avisos

- A primeira célula deve ser executada a cada nova sessão iniciada. Já a segunda pode ser excluída depois de feita a autenticação.
- Você também pode acessar o colab pelo browser de seu celular, porém, não conseguirá concluir a 2º etapa. Sendo, por isso, necessário que essa etapa seja feita através de um ambiente desktop (PC/laptop/notebook). Então, poderá continuar utilizando o programa em qualquer dispositivo móvel via colab.
- Pelo colab, automaticamente é baixada a versão mais recente do programa sempre que a 1º célula é executada. Caso queira desativar a atualização automática, basta apagar as duas últimas linhas do código dessa mesma célula.
- É possível criar até 50 canais por dia. E o limite recomendado de encaminhamentos de mensagens é de 1000 por dia.
- Lembre-se de inserir os textos entre aspas simples ou duplas no campo "QUERY".
- Ao inserir a "QUERY" desejada e o tipo de mensagem para encaminhar, o programa irá selecionar as mensagens que atendam a ambos os critérios.
- Se desejar que o canal de destino seja criado automaticamente, deixe o campo "DEST" vazio.
- Caso queira encaminhar mensagens de um chat de uma conversa com outra pessoa, insira no campo "ORIG" o username ou a ID do usuário. E, se precisar encaminhar as suas "menssagens salvas", basta inerir "me" em "ORIG" ou a sua ID.
### Rodando o programa localmente (uso básico)

Primeiro, instale a versão 3.7 ou superior do [python](https://www.python.org/downloads/) e execute no terminal:

```
pip uninstall pyrogram && pip install tgcrypto https://github.com/Drrivao/pyrogram/archive/refs/heads/master.zip
```

Em seguida, realize a autenticação 2FA:

```
python auto_forward_messages.py -i <api id> -s <api hash>
```

Por fim, comece a clonar:

```
python auto_forward_messages.py -o <id/username/link>
```

Para abrir o menu de ajuda de como usar as flags:

```
python auto_forward_messages.py --help
```