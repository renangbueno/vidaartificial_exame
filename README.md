# Jogo da Vida de Conway – Programação Paralela e Distribuída

**Disciplina**: Sistemas Distribuídos ES45A.2025_02.ES51  
**Aluno**: Renan Gabriel Bueno RA: 2454254  

Implementação completa das três versões exigidas usando apenas **Python padrão**.

---

## 🌟 Versões Entregues

* **Sequencial**: Implementação usando listas simples.
* **Paralela**: Implementação com **`threading`** (de 1 a 8 *threads*).
* **Distribuída**: Implementação com **sockets TCP** (1 servidor + N clientes, usando o padrão *halo exchange* para comunicação de fronteira). 

---

## 🚀 Como Executar

### Sequencial + Paralelo

Para rodar as versões sequenciais, paralelas e gerar os gráficos de desempenho:

```bash
python jogo_da_vida.py
```

### Distribuída (3 terminais)
Para executar a versão distribuída, use três terminais separados:

```bash
# Terminal 1: Servidor
python jogo_da_vida.py servidor
```

```bash
# Terminal 2 e 3: Clientes (abrir em terminais separados)
python jogo_da_vida.py cliente
```

## 📊 Resultados Obtidos
Máquina de Teste: Intel® Core™ i5-10500T @ 2.30 GHz • 8 GB RAM • Windows 11 Pro • Python 3.12

O modelo distribuído foi o único que apresentou ganho real de desempenho porque utiliza processos separados (clientes/servidor), escapando assim do GIL (Global Interpreter Lock) do Python.

## 📚 Fontes Consultadas
* Documentação oficial Python
* Wikipedia – Conway’s Game of Life
* Real Python / Stack Overflow
* Materiais USP e PUC (halo exchange)
* Grok (xAI) e ChatGPT – depuração e explicação do GIL
