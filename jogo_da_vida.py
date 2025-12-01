# Aluno: Renan Gabriel Bueno RA: 2454254
import time
import random
import threading
import socket
import pickle
import struct

def criar_grid(t):
    return [[random.randint(0,1) for _ in range(t)] for _ in range(t)]

def vizinhos(grid, i, j, t):
    s = 0
    for di in [-1,0,1]:
        for dj in [-1,0,1]:
            if di == 0 and dj == 0:
                continue
            ni = (i + di) % t
            nj = (j + dj) % t
            s += grid[ni][nj]
    return s

def sequencial(grid):
    t = len(grid)
    nova = [[0]*t for _ in range(t)]
    for i in range(t):
        for j in range(t):
            v = vizinhos(grid, i, j, t)
            if grid[i][j]:
                nova[i][j] = 1 if v == 2 or v == 3 else 0
            else:
                nova[i][j] = 1 if v == 3 else 0
    return nova

def paralelo(grid, nt):
    t = len(grid)
    nova = [[0]*t for _ in range(t)]
    lock = threading.Lock()
    def calc(inicio, fim):
        local = []
        for i in range(inicio, fim):
            linha = []
            for j in range(t):
                v = vizinhos(grid, i, j, t)
                if grid[i][j]:
                    linha.append(1 if v == 2 or v == 3 else 0)
                else:
                    linha.append(1 if v == 3 else 0)
            local.append(linha)
        with lock:
            for idx, linha in enumerate(local):
                nova[inicio + idx] = linha
    tam = t // nt
    threads = []
    for i in range(nt):
        ini = i * tam
        fim = t if i == nt - 1 else (i + 1) * tam
        th = threading.Thread(target=calc, args=(ini, fim))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    return nova

def rodar_sequencial(tam, it):
    g = criar_grid(tam)
    ini = time.perf_counter()
    for _ in range(it):
        g = sequencial(g)
    return time.perf_counter() - ini

def rodar_paralelo(tam, it, nt):
    g = criar_grid(tam)
    ini = time.perf_counter()
    for _ in range(it):
        g = paralelo(g, nt)
    return time.perf_counter() - ini

def servidor(porta=5555, clientes=2, tam=2000, it=20):
    grid = criar_grid(tam)
    linhas_por = tam // clientes
    s = socket.socket()
    s.bind(('', porta))
    s.listen(clientes)
    conns = []
    for _ in range(clientes):
        c, _ = s.accept()
        conns.append(c)
    inicio = time.perf_counter()
    for _ in range(it):
        for i in range(clientes):
            ini = i * linhas_por
            fim = tam if i == clientes-1 else (i+1)*linhas_por
            bloco = grid[ini:fim]
            ant = grid[ini-1] if i > 0 else grid[0]
            prox = grid[fim] if i < clientes-1 else grid[tam-1]
            dados = pickle.dumps((bloco, ant, prox, tam))
            conns[i].send(struct.pack('!I', len(dados)))
            conns[i].send(dados)
        nova = [[0]*tam for _ in range(tam)]
        for i in range(clientes):
            tam_msg = struct.unpack('!I', conns[i].recv(4))[0]
            msg = b''
            while len(msg) < tam_msg:
                msg += conns[i].recv(4096)
            parte = pickle.loads(msg)
            ini = i * linhas_por
            fim = tam if i == clientes-1 else (i+1)*linhas_por
            for k in range(fim-ini):
                nova[ini+k] = parte[k]
        grid = nova
    print(f"Distribuido ({clientes} clientes) {tam}x{tam} {it} it: {time.perf_counter()-inicio:.3f}s")
    for c in conns:
        c.close()
    s.close()

def cliente(host='localhost', porta=5555):
    c = socket.socket()
    c.connect((host, porta))
    while True:
        try:
            tam_msg = struct.unpack('!I', c.recv(4))[0]
            msg = b''
            while len(msg) < tam_msg:
                msg += c.recv(4096)
            bloco, ant, prox, tam = pickle.loads(msg)
            local = [ant] + bloco + [prox]
            nova = []
            for i in range(1, len(local)-1):
                linha = []
                for j in range(tam):
                    v = 0
                    for di in [-1,0,1]:
                        for dj in [-1,0,1]:
                            if di == 0 and dj == 0:
                                continue
                            v += local[i+di][(j+dj)%tam]
                    cel = local[i][j]
                    linha.append(1 if (cel == 1 and v in (2,3)) or (cel == 0 and v == 3) else 0)
                nova.append(linha)
            resp = pickle.dumps(nova)
            c.send(struct.pack('!I', len(resp)))
            c.send(resp)
        except:
            break
    c.close()

if __name__ == '__main__':
    tam = 10
    iteracoes = 20

    print("=== TESTES DE DESEMPENHO ===\n")
    print("Sequencial")
    t = rodar_sequencial(tam, iteracoes)
    print(f"{tam}x{tam} {iteracoes} it -> {t:.3f}s\n")

    print("Paralelo")
    for th in [1,2,4,8]:
        t = rodar_paralelo(tam, iteracoes, th)
        print(f"{th} threads -> {t:.3f}s")
    print()

    # print("Distribuido")
    print()

    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "servidor":
            servidor()
        elif sys.argv[1] == "cliente":
            cliente()