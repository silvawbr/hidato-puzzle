# Seminário 2 — Projeto e Análise de Algoritmos (PROCC0083 - UFS)

## 🎓 Tema: Hidato Puzzle — Um Caminho Hamiltoniano com Números (NP-Difícil)

Este repositório contém os materiais apresentados por **Wagner Silva** e **Wagner Lucena** no **Seminário 2 da disciplina PROCC0083 – Projeto e Análise de Algoritmos**, ministrada pelo professor **Leonardo Nogueira Matos** no Programa de Pós-Graduação em Ciência da Computação da **Universidade Federal de Sergipe (UFS)**.

---

## 📚 Sumário

- [Descrição](#-descrição)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Problema Abordado](#-problema-abordado)
- [Classificação na Complexidade](#-classificação-na-complexidade)
- [Algoritmo Utilizado](#-algoritmo-utilizado)
- [Vídeo da Apresentação](#-vídeo-da-apresentação)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Referências](#-referências)
- [Autores](#-autores)
- [Licença](#-licença)

---

## 📌 Descrição

Neste seminário, estudamos o **Hidato Puzzle**, um jogo lógico em grade no qual é preciso preencher o tabuleiro com os números de `1` até `N`, de forma que:

> As células contendo `k` e `k+1` sejam adjacentes (horizontal, vertical ou diagonalmente).

Do ponto de vista de Projeto e Análise de Algoritmos, mostramos que:

- o Hidato pode ser modelado como um **Problema de Caminho Hamiltoniano em Grafos de Grade**;
- o problema de decisão associado é **NP-Difícil / NP-Completo**, via redução de problemas Hamiltonianos em grafos de grade;
- a solução prática é naturalmente formulada com **Backtracking (DFS)**, utilizando poda agressiva do espaço de busca.

---

## 📁 Estrutura do Projeto

```text
📦 hidato-puzzle/
├── 📂 src/
│   ├── 📄 hidato_puzzle_example.py    # Exemplo de uso do solver de Hidato
│   └── 📂 hidato/
│       ├── 📄 hidato_puzzle.py               # Algoritmo de Backtracking (DFS) para Hidato
│       ├── 📄 grid.py                 # Representação do tabuleiro e geração de vizinhos
│       ├── 📄 utils.py                # Funções auxiliares (leitura, impressão, etc.)
│       ├── 📄 __init__.py
│       └── 📄 py.typed
├── 📂 tests/                          # Testes automatizados
├── 📄 slides.pdf                      # Slides da apresentação do seminário
├── 📄 README.md                       # Este arquivo
├── 📄 pyproject.toml                  # Configuração do projeto (dependências via uv)
└── 📄 uv.lock                         # Lockfile de dependências
```

---

## 🧠 Problema Abordado

Dado um tabuleiro de tamanho \( n 	imes m \) com algumas casas já preenchidas por números (tipicamente incluindo `1` e `N`), o problema é:

> **Preencher todas as células com os números de 1 até \( N = n \cdot m \) de forma que cada par \( (k, k+1) \) ocupe células adjacentes.**

Modelagem em grafos:

- Cada célula do grid é um **vértice**.
- Há uma **aresta** entre duas células se elas são adjacentes (8 vizinhanças).
- Uma solução completa é um **caminho Hamiltoniano** que visita todos os vértices exatamente uma vez, respeitando as posições fixas.

---

## 🔍 Classificação na Complexidade

### ✔️ Hidato ∈ NP

Dada uma atribuição de números ao tabuleiro, é possível verificar em tempo polinomial:

- se cada número de `1` a `N` aparece exatamente uma vez;
- se cada par `k, k+1` está em células adjacentes;
- se todas as pistas (números fixos) do puzzle são respeitadas.

A verificação é \( O(N) \), onde \( N = n \cdot m \).

### ✔️ Hidato é NP-Difícil / NP-Completo

A versão de decisão do Hidato pode ser mostrada **NP-Difícil** por redução polinomial a partir de:

- **Hamiltonian Path in Grid Graphs**, um problema clássico NP-completo,
- construindo um Hidato cujo grafo subjacente é exatamente a grade original e cujas restrições de numeração não diminuem a dificuldade do problema.

Intuitivamente:

- Encontrar uma solução para o Hidato equivale a encontrar um caminho Hamiltoniano no grafo de grade associado;
- As pistas (números previamente preenchidos) apenas restringem o conjunto de caminhos válidos.

---

## 🧮 Algoritmo Utilizado

### 🎯 Técnica: Backtracking (Busca em Profundidade – DFS)

A solução é construída incrementalmente:

1. Começamos de `1`, em sua posição fixa.
2. Tentamos colocar `2` em uma das células adjacentes válidas.
3. Em seguida, `3` adjacente a `2`, e assim por diante, até `N`.
4. Quando alguma escolha leva a um estado sem solução possível, o algoritmo **retrocede** (backtrack) e tenta uma alternativa.

### ⏱️ Complexidade

No pior caso, o algoritmo tem tempo **exponencial**:

\[
T(N) = O(8^N)
\]

pois cada número pode, em teoria, ser colocado em até 8 posições adjacentes.  
Na prática, **heurísticas de poda** reduzem drasticamente o espaço de busca:

- checagem de validade local,
- detecção de “ilhas” desconectadas,
- ordenação heurística dos próximos passos.

---

## ▶️ Vídeo da Apresentação

📺 [Link Apresentação Youtube](https://youtu.be/6xGmRnn-tpc)

---

## 💻 Como Executar o Projeto

### 1. Criar ambiente virtual e instalar dependências (via `uv`)

```bash
uv venv
uv sync --all-groups
```

> Certifique-se de que o comando `uv` esteja instalado:  
> https://github.com/astral-sh/uv

---

### 2. Executar o exemplo de solução de Hidato

```bash
uv run python src/hidato_puzzle_example.py
```

---

## 📚 Referências

- CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C.  
  **Introduction to Algorithms.** MIT Press.

- LEVITIN, A.  
  **Introduction to the Design and Analysis of Algorithms.** 3rd ed. Pearson.

- Materiais da disciplina PROCC0083 – Projeto e Análise de Algoritmos (UFS):  

- DEMAIN, E. D. et al.  
  **“Computational Complexity of Games and Puzzles.”**

---

## 👥 Autores

- **Wagner Silva** – https://github.com/silvawbr  
- **Wagner Lucena**

---

## 📝 Licença

Este projeto é de caráter acadêmico e está licenciado sob os termos da **MIT License**.
