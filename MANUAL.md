# Manual de Uso - DataManager

## 1. O que e o DataManager

O DataManager e um app desktop para aprender SQLite de forma visual.
Com ele voce pode:
- criar bancos `.db`
- criar e excluir tabelas
- inserir, editar e excluir registros

## 2. Como abrir o app

### Opcao A: Executavel
1. Abra `DataManager.exe`.

### Opcao B: Modo desenvolvimento
1. No terminal, entre na pasta do projeto.
2. Execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python datamanager.py
```

## 3. Primeiro fluxo recomendado (aula)

1. Clique em `Criar DB` e salve um arquivo `.db`.
2. Clique em `Criar Tabela`.
3. Defina o nome da tabela e as colunas.
4. Selecione a tabela na barra lateral.
5. Use `Inserir`, `Editar` e `Excluir` para praticar CRUD.

## 4. Criacao de colunas (explicacao rapida)

- `Nome`: nome da coluna.
- `Tipo`: tipo de dado (`INTEGER`, `TEXT`, `REAL`, etc).
- `PK`: define a coluna como chave primaria.
- `AI`: auto incremento (geralmente usado com `INTEGER` + `PK`).
- `NN`: `NOT NULL` (nao permite valor vazio/NULL).
- `UNQ`: `UNIQUE` (nao permite valores repetidos).
- `Default`: valor padrao da coluna.
- `FK Tabela` e `FK Coluna`: cria relacao com outra tabela (chave estrangeira).
- `On Delete` e `On Update`: comportamento da FK em alteracoes/exclusoes.

## 5. Dicas para estudantes

- Comece com tabelas simples (`id`, `nome`, `email`).
- Use `id INTEGER PK AI` para facilitar exemplos.
- Teste erros de modelagem para entender as restricoes.
- Compare tabelas com e sem `NN` e `UNQ`.

## 6. Problemas comuns

- "Nenhum banco aberto": abra ou crie um banco antes.
- "Selecione uma tabela": escolha uma tabela na lista lateral.
- Falha ao abrir `.exe`: execute o app no modo desenvolvimento para validar dependencias.
