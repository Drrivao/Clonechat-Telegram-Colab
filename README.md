# Auto Forward Messages

> Projeto baseado no [clonechat](https://github.com/apenasrr/clonechat).

### Como usar

Primeiro, obtenha as suas [credenciais](https://upolar.github.io/clonechats-docs/#obtendo-credenciais-da-api-do-telegram) e siga o [tutorial](https://t.me/auto_forward_messages_drrivao).


### Utilizando filtros e outros argumentos

- MODE: "user" é o modo de clonagem mais lenta e "bot" o mais rápido, porém é necessário que o usuário seja um adm dos canais de orig/dest.
- FILTER: filtra as mensagens pelo tipo. Para escolher múltiplos tipos, coloque-os separados por vírgulas, por exemplo: "photo,document".
- QUERY: filtra as mensagens que contêm determinados termos, por exemplo, inserindo "python" o programa irá encaminhar somente as mensagens com o termo "python" na descrição, no texto ou no nome do arquivo.
- LIMIT: define um limite para a quantidade de mensagens a serem encaminhadas; o recomendado é um limite de até 1000 msgs por dia.
- RESUME: o programa retoma um processo de clonagem anterior.
- RESTART: o programa será reiniciado automaticamente a cada 4 horas para encaminhar novas mensagens do chat de origem.

### Avisos

- Ao abrir o colab, no painel superior você encontrará o botão "Copiar para o Drive". Ao apertá-lo será criada a cópia do notebook no seu drive dentro de uma pasta chamada "Colab Notebooks". Então, quando precisar utilizar o programa novamente, abra essa cópia e não o notebook salvo neste repositório.
- Lembre-se de inserir os textos entre aspas simples ou duplas no campo "QUERY".
- Se desejar que o canal de destino seja criado automaticamente, deixe o campo "DEST" vazio.
- Caso queira encaminhar mensagens de um chat de uma conversa com outra pessoa, insira no campo "ORIG" o username ou a ID do usuário.
- A primeira célula deve ser executada a cada nova sessão iniciada. Já a segunda pode ser excluída depois de feita a autenticação.
- Você também pode acessar o colab pelo browser de seu celular, porém, não conseguirá concluir a 2º etapa. Sendo, por isso, necessário que essa seja feita através de um ambiente desktop (PC/laptop/notebook). Então, poderá continuar utilizando o programa em qualquer dispositivo móvel via colab.
- É possível criar até 50 canais por dia. E o limite recomendado de encaminhamentos de mensagens é de 1000 por dia.

### Rodando o programa localmente

Primeiro, instale qualquer versão do [python](https://www.python.org/downloads/) acima da v3.7 e execute no terminal:

```
pip uninstall pyrogram && pip install tgcrypto https://github.com/Drrivao/pyrogram/archive/refs/heads/master.zip
```

Em seguida, realize a autenticação 2FA:

```
python auto_forward_messages.py -i "API ID" -s "API HASH"
```

Por fim, comece a clonar:

```
python auto_forward_messages.py -o "origin chat title"
```

Para abrir o menu de ajuda de como usar as flags:

```
python auto_forward_messages.py --help
```