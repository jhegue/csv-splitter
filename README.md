# CSV Splitter

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/status-active-2ea44f)
![License](https://img.shields.io/badge/license-MIT-blue)

Aplicação Streamlit para dividir um arquivo CSV grande em múltiplos arquivos menores com base em uma coluna escolhida pelo usuário, entregando tudo em um único arquivo `.zip`.

Também chamada de **Divisor CSV**, a aplicação foi pensada para simplificar fluxos operacionais em que um dataset precisa ser separado por unidade, categoria, regional, cliente ou qualquer outro valor único existente em uma coluna.

## ✨ Visão Geral

Com o **Data Splitter**, você pode:

- fazer upload de um arquivo CSV diretamente pela interface;
- detectar automaticamente o separador do arquivo de entrada;
- escolher dinamicamente a coluna usada para a divisão;
- definir o formato de saída entre `CSV`, `Parquet` e `JSON`;
- escolher o delimitador dos arquivos gerados quando a saída for `CSV`;
- baixar todos os arquivos gerados em um único pacote `.zip`.

## 🚀 Funcionalidades Principais

| Funcionalidade | Descrição |
| --- | --- |
| Upload de CSV | Carregamento de arquivos CSV via interface Streamlit |
| Detecção automática de separador | Identifica delimitadores comuns como `;`, `,`, `\t` e `\|` |
| Divisão dinâmica por coluna | Permite escolher qualquer coluna existente no arquivo enviado |
| Exportação flexível | Gera arquivos em `CSV`, `Parquet` ou `JSON` |
| Download consolidado | Entrega todos os arquivos em um único `.zip` |
| Prévia dos dados | Exibe uma tabela com os dados carregados |
| Métricas rápidas | Mostra linhas, colunas, delimitador e tipo de saída |

## 📋 Pré-requisitos

Antes de executar a aplicação, tenha instalado:

- `Python 3.10` ou superior
- `pip` atualizado
- ambiente virtual recomendado (`venv`)

## 🛠️ Como Instalar e Rodar

### 1. Clone o repositório

```bash
git clone https://github.com/jhegue/data-splitter.git
```

```bash
cd data-splitter
```

### 2. Crie e ative um ambiente virtual

No Windows:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
streamlit run main.py
```

Após iniciar, o Streamlit abrirá a aplicação no navegador padrão ou exibirá a URL local no terminal.

## 🧭 Como Usar

O fluxo da aplicação é simples e linear:

### 1. Upload

- Faça upload de um arquivo CSV.
- A aplicação detecta automaticamente o separador do arquivo.
- Assim que o upload for concluído, uma mensagem de sucesso e as métricas básicas serão exibidas.

### 2. Configurar

- Escolha a coluna que será usada para dividir os dados.
- Selecione o formato dos arquivos gerados:
  - `CSV`
  - `Parquet`
  - `JSON`
- Caso o formato escolhido seja `CSV`, selecione também o delimitador de saída.

### 3. Download

- A aplicação gera um arquivo para cada valor único da coluna selecionada.
- Todos os arquivos são compactados automaticamente em um único `.zip`.
- Clique em **Download ZIP** para baixar o resultado.

## 🖼️ Fluxo da Interface

```text
Upload CSV -> Escolher coluna -> Definir formato/Delimitador -> Gerar ZIP -> Download
```

## 🗂️ Estrutura do Projeto

```text
data-splitter/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── core.py
│   ├── models.py
│   ├── processor.py
│   └── utils.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   └── styles.py
├── tests/
│   └── .gitkeep
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## 🧱 Organização da Arquitetura

### `main.py`

Responsável apenas pelo fluxo principal da aplicação Streamlit e pela orquestração da interface.

### `app/`

Camada de regra de negócio:

- `config.py`: constantes e configurações globais
- `models.py`: modelos de dados com `dataclasses`
- `utils.py`: funções utilitárias puras
- `processor.py`: leitura, serialização e geração dos arquivos
- `core.py`: orquestração principal da lógica de negócio

### `ui/`

Camada de interface:

- `components.py`: widgets e componentes reutilizáveis do Streamlit
- `styles.py`: configuração visual e de página

### `tests/`

Espaço reservado para a futura suíte de testes automatizados.

## 🧰 Tecnologias Utilizadas

- **Python**: linguagem principal da aplicação
- **Streamlit**: interface web interativa
- **Pandas**: leitura, manipulação e divisão dos dados
- **PyArrow**: suporte à exportação em `Parquet`

## 🔮 Melhorias Futuras

Algumas evoluções possíveis para o projeto:

- adicionar testes automatizados em `tests/`;
- suportar upload de arquivos maiores com feedback de progresso;
- permitir filtros antes da divisão;
- incluir histórico de execuções;
- adicionar exportação para mais formatos;
- disponibilizar deploy em ambiente cloud.

## 📄 Licença

Este projeto pode ser distribuído sob a licença **MIT**.

Se desejar, você pode adicionar um arquivo `LICENSE` na raiz com o texto oficial da licença MIT.
