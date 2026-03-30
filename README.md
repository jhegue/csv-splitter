# CSV Splitter

Aplicação Streamlit para dividir um arquivo CSV em múltiplos arquivos com base em uma coluna escolhida, entregando tudo em um único ZIP.

## Estrutura

```text
data_splitter/
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
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── tests/
```

## Responsabilidades

- `main.py`: ponto de entrada do Streamlit e orquestração da tela.
- `app/config.py`: constantes e configurações globais.
- `app/models.py`: dataclasses de domínio.
- `app/utils.py`: utilitários puros de formatação e sanitização.
- `app/processor.py`: leitura do CSV, serialização e geração do ZIP.
- `app/core.py`: regras de negócio e orquestração de alto nível.
- `ui/components.py`: componentes reutilizáveis da interface.
- `ui/styles.py`: configuração visual e de página do Streamlit.
- `tests/`: espaço reservado para testes automatizados futuros.

## Como executar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute a aplicação:

   ```bash
   streamlit run main.py
   ```

## Observações

- A lógica de leitura, separação e exportação foi removida do `main.py`.
- O comportamento funcional da aplicação foi mantido.
- A estrutura agora facilita testes, manutenção e evolução futura.
