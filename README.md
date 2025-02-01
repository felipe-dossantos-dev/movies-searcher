# Movies Searcher
Desafio Técnico Luiza Labs - Sistema de busca em arquivos de texto

## Dependências e Versões

- Python 3.12+
- pytest (para testes)
- pytest-cov (para coverage dos testes)

## Instalação

1. Clone o repositório:

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências de desenvolvimento:
```bash
pip install -r requirements.txt
```

## Uso

O sistema é composto por dois scripts principais:

### Indexador (index.py)

Cria um índice dos arquivos para otimizar as buscas:

```bash
python index.py --data-dir ./data --index-dir ./index --indexer ngram
```

Argumentos:
- `--data-dir`: Diretório contendo os arquivos a serem indexados (default: ./data)
- `--index-dir`: Diretório onde o índice será salvo (default: ./index)
- `--indexer`: Tipo de indexador (file ou ngram, default: ngram)

### Buscador (query.py)

Realiza buscas nos arquivos indexados:

```bash 
python query.py "palavra1 palavra2" --data-dir ./data --index-dir ./index --indexer ngram
```

Argumentos:
- `query`: Palavras a serem buscadas (critério AND - todas devem existir no arquivo)
- `--data-dir`: Diretório com os arquivos (default: ./data)
- `--index-dir`: Diretório do índice (default: ./index)
- `--indexer`: Tipo de indexador (file, memory ou ngram, default: ngram)

## Testes

Para executar os testes:

```bash
python -m pytest tests/
```

Para gerar relatório de cobertura:

```bash
python -m pytest --cov=src tests/
```