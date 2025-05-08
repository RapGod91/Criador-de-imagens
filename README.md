# Gerador de Imagens

Este é um aplicativo web que permite gerar imagens com texto personalizado sobre uma imagem de fundo.

## Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie uma pasta chamada `static/images` no diretório do projeto
2. Adicione uma imagem de fundo chamada `background.jpg` na pasta `static/images`

## Executando o aplicativo

1. Execute o comando:
```bash
python app.py
```

2. Abra seu navegador e acesse `http://localhost:5000`

## Como usar

1. Digite o texto desejado no campo de entrada
2. Clique no botão "Gerar Imagem"
3. A imagem será gerada e exibida na tela

## API

O aplicativo também oferece uma API REST que pode ser acessada via POST para `/generate` com um JSON contendo o campo `text`.

Exemplo de uso da API:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"Seu texto aqui"}' http://localhost:5000/generate
``` 