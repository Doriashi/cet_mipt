import numpy as np
import time
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
import sys

def dense_matrix(N): # creation of dense matrix A
    A = np.zeros((N, N))
    for j in range(N):
        for i in range(N):
            if i == j:
                A[j][i] = 1
            else:
                A[j][i] = 1 / abs(i - j)
    return A

def sparse_matrix(N): # creation of sparse matrix A
    ia = []
    ja = []
    a = []
    for j in range(N):
        stroka = []
        for i in range(N):
            if i == j or (1 / abs(i - j)) >= 1.e-2:
                stroka.append(len(a))
                ja.append(i)
                if i == j:
                    a.append(1)
                else:
                    a.append(1 / abs(i - j))
        ia.append(stroka[0])
    ia.append(len(a))
    A = [ia, ja, a]
    return A

def mul(A, D): # multiplying of sparse matrix and residual
    ia = A[0]
    ja = A[1]
    a = A[2]
    n = len(D)
    res = [0] * n
    csr_row = 0
    for i in range(n):
        start, end = ia[i], ia[i + 1]
        for j in range(start, end):
            col, csr_value = ja[j], a[j]
            dense_value = D[csr_row]
            res[col] += csr_value * dense_value
        csr_row += 1
    return np.array(res)

def b_sol(A, N): # solution of equation Ax=b
    x = np.array([1] * N)
    return A.dot(x)

def conjugate_gradients_dense(A, b, N, eps): # method of conjugate gradients for dense matrix
    x = np.zeros(N)
    r = b - x.dot(A)
    p = r
    rr = np.dot(r, r)
    while True:
        alfa = - rr / np.dot(p, p.dot(A))
        x -= alfa * p
        r += alfa * A.dot(p)
        rr_next = np.dot(r, r)
        if rr_next ** (1/2) < eps:
            return x
        beta = rr_next / rr
        p = r + beta * p
        rr = rr_next

def conjugate_gradients_sparse(A, b, N, eps): # method of conjugate gradients for sparse matrix
    x = np.zeros(N)
    r = b - mul(A, x)
    p = r
    rr = np.dot(r, r)
    while True:
        alfa = - rr / np.dot(p, mul(A, p))
        x -= alfa * p
        r += alfa * mul(A, p)
        rr_next = np.dot(r, r)
        if rr_next ** (1/2) < eps:
            return x
        beta = rr_next / rr
        p = r + beta * p
        rr = rr_next

def sparse(N):  # scipy package
    A = np.zeros((N, N))
    for j in range(N):
        for i in range(N):
            if i == j:
                A[j][i] = 1
            else:
                p = 1 / abs(i - j)
                if p >= 1.e-1:
                    A[j][i] = p
                else:
                    A[j][i] = 0
    A = csr_matrix(A)
    b = b_sol(A, N)
    start_time = time.time()
    x = spsolve(A, b)
    t = time.time() - start_time

    return x, t, sys.getsizeof(A)

N = 1000  # conditions
eps = 1.e-1

A1 = dense_matrix(N)
b1 = b_sol(A1, N)

start_time = time.time()
sol1 = conjugate_gradients_dense(A1, b1, N, eps)
print('Method of conjugate gradients:')
#print(sol1)
print("Dense matrix: %s seconds" % (time.time() - start_time))
print(sys.getsizeof(A1))

'''
A2 = sparse_matrix(N)
x = np.array([1] * N)
b2 = mul(A2, x)

start_time = time.time()
sol2 = conjugate_gradients_sparse(A2, b2, N, eps)
print('Method of conjugate gradients:')
#print(sol2)
print("Sparse matrix: %s seconds" % (time.time() - start_time))
print(sys.getsizeof(A2))

x, t, m = sparse(N)
print("Scipy package: %s seconds" % t)
print(m)'''