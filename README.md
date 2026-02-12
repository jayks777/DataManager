# DataManager

Aplicativo desktop em Python (Tkinter) para estudar modelagem e manipulacao de dados em SQLite.

Projeto pensado para uso didatico em sala, com interface visual para:
- criar banco `.db`
- criar/excluir tabelas
- inserir/editar/excluir registros
- navegar rapidamente pelos dados

## Publico-alvo

Estudantes iniciando com banco de dados relacional e SQLite.

## Tecnologias

- Python 3
- Tkinter
- Peewee (driver/ORM leve para SQLite)
- PyInstaller (geracao do `.exe`)
- Inno Setup (instalador Windows)

## Como executar (modo desenvolvimento)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python datamanager.py
```

## Como gerar o executavel

```powershell
.\build.ps1
```

Saida:

```text
dist\DataManager.exe
```

## Como gerar o instalador

Pre-requisito: Inno Setup instalado e `iscc.exe` disponivel no `PATH`.

```powershell
.\build_installer.ps1
```

Saida:

```text
installer\output\DataManagerSetup.exe
```

## Estrutura do projeto

```text
datamanager.py                # Entry point
datamanager_app/
  app.py                      # Inicializacao do app
  db/manager.py               # Operacoes de banco
  ui/browser.py               # Interface principal
  ui/theme.py                 # Tema visual
installer/
  DataManager.iss             # Script do instalador
build.ps1                     # Build do executavel
build_installer.ps1           # Build do instalador
```

## Fluxo didatico sugerido para aula

1. Criar um banco novo com "Criar DB".
2. Criar tabela com PK, tipos e restricoes.
3. Inserir registros.
4. Editar e excluir registros.
5. Discutir diferenca entre estrutura (schema) e dados.

## Publicacao no GitHub (checklist)

- manter no repositorio apenas codigo-fonte e scripts
- nao versionar `build/`, `dist/` e `.venv/`
- publicar release com `DataManagerSetup.exe`
- documentar mudancas no texto da release

## Licenca

MIT. Veja `LICENSE`.
