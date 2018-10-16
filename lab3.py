"""
lab3

В этом модуле определены функции, которые позволяют работать с питоновскими строками
как с матрицами, определены характерные матричные операции. В плане быстродействия
превосходит numpy в некоторых случаях.

Есть проблемы с рангом (ранг считает правильно, но изменяет исходную матрицу(список),
не смотря на все мои старания).
+надо поработать над функцией наблюдаемости и управляемости.
""" 

def isvector(v):
    """
    Вернет 1 если v-вектор строка,
    в противном случае вернет 0.
    """
    try:
        len(v[0])
        return 0
    except TypeError:
        return 1
    
def vol(m,i):
    """
    Функция, выделяющая из матрицы m[n*k] i-ый столбец
    и возвращающая его в виде вектора строки.
    """
    if isvector(m):
        return m
    else:
        res=[]
        n=len(m)
        for j in range(0,n):
            res.append(m[j][i])
        return res

def nulvector(v):
    """
    Тест на нулевой вектор, заданный в виде вектора строки.
    Вернет 1 если все элемента вектора нули,
    0 в противном случае.
    """
    l=len(v)
    c=v.count(0)
    if l==c:
        return 1
    else:
        return 0

def delcol(m,i):
    """
    Удаление из матрицы m i-ого столбца.
    Ничего не возвращает, а сразу меняет m.
    """
    l=len(m)
    for j in range(0,l):
        m[j].pop(i)

def delnul(m):
    """
    Удаление нулевых строк и столбцов матрицы m[l*k],
    где l-кол-во строк матрицы, а k-кол-во столбцов
    матрицы. Возвращает матрицу с удаленными нулевыми векторами,
    но не изменяет исходную матрицу.
    """
    res=m.copy()
    l=len(res)
    k=len(res[0])
    i=0
    j=0
    count=[]
    while i<l:
        if nulvector(res[i]):
            res.pop(i)
            l=l-1
            continue
        if i==0:
            while j<k:
                if nulvector(vol(res,j)):
                    delcol(res,j)
                    k=k-1
                    continue
                j=j+1
        i=i+1
    return res
                        
def ktest(v1,v2):
    """
    Проверка линейной зависимости двух векторов,k-коэффициент пропорциональности их координат.
    Функция ktest вернет либо 0, если отсутствует линейная зависимость векторов,
    либо значение коэффициента пропорциональности их координат, то есть k.
    Вектора задаются в виде вектора строки (список без подсписков).
    Предполагается что вектора одного размера.
    """
    l=len(v1)
    res=[]
    count=0
    if (v1[0]==0 and v2[0]==0):
        for i in range(1,l):
            if (v1[i]!=0 and v2[i]!=0):
                k=v2[i]/v1[i]
                count=i
                break
    for i in range(count,l):
        if (v1[i]!=0 and v2[i]!=0):
            k=v2[i]/v1[i]
            if i==count:
                klast=k
            if klast!=k:
                k=0
                break
            klast=k
        elif ((v1[i]==0 and v2[i]!=0) or (v1[i]!=0 and v2[i]==0)):
            k=0
            break
    return k

def strlintest(m):
    """
    Удаление линейно зависимых строк матрицы m.
    m-прямоугольная вещественная матрица.
    """
    l=len(m)
    j=0
    i=1
    while j<l-1:
        while i<l:
            res=ktest(m[j],m[i])
            if res!=0:
                m.pop(i)
                l=l-1
                continue
            i=i+1
        j=j+1

def vollintest(m):
    """
    Удаление линейно зависимых столбцов матрицы m.
    """
    k=len(m[0])
    j=0
    i=1
    while j<k-1:
        while i<k:
            res=ktest(vol(m,j),vol(m,i))
            if res!=0:
                delcol(m,i)
                k=k-1
                continue
            i=i+1
        j=j+1
def rank(m):
    """
    Вычисление ранга матрицы m[n*m]-вещественная прямоугольная матрица.
    ранг матрицы вычисляется как наименьший размер матрицы m у которой все строки
    и столбцы линейно независимые и ненулевые.
    """
    r=delnul(m)
    strlintest(r)
    vollintest(r)
    n=len(r)
    k=len(r[0])
    if n>=k:
        return k
    else:
        return n

def zero(n,k):
    """
    Создание нулевой матрицы с размером n*k
    или нулевого вектора столбца.
    Если n=1 о будет возвращена вектор строка.
    """
    res=[]
    if n==1:
        res=[0 for i in range(0,k)]
    else:
        for i in range(0,n):
            s1=[0 for i in range(0,k)]
            res.append(s1)
    return res

def scalarmult(v1,v2):
    """
    Вычисление скалярного произведения векторов v1 и v2,
    заданных в виде вектора строки.
    """
    l=len(v1)
    res=0
    for i in range(0,l):
        res=res+v1[i]*v2[i]
    return res

def strtocol(v):
    """
    Перевод вектора строки в вектор столбец.
    Возвращает вектор столбец.
    """
    res=[]
    n=len(v)
    for i in range(0,n):
        res.append([v[i]])
    return res

def mult(m1,m2):
    """
    Перемножение сцепленных матриц m1,m2,причем в порядке m1*m2,
    где m2 может быть в частности вектором, заданным
    в виде вектора строки пользователем, или m1 может
    быть вектором, заданным
    в виде вектора строки пользователем.
    Если второй аргумент является вектором, то возвратит
    результат в виде вектора столбца.
    Если первый аргумент является вектором,
    заданным в виде вектора строки, то возвратит
    результат в виде вектора столбца.
    """
    if isvector(m1):
        n=1
    else:
        n=len(m1)
    if isvector(m2):
        strtocol(m2)
        k=1
    else:
        k=len(m2[0])
    res=zero(n,k)
    for i in range(0,n):
        for j in range(0,k):
            el=scalarmult(m1[i],vol(m2,j))
            if n==1:
                res[j]=el
            else:
                res[i][j]=el

def ones(n):
    """
    Генерация единичной матрицы размерностью n.
    """
    res=zero(n,n)
    for i in range(0,n):
        res[i][i]=1
    return res

def mpow(m, n):
    """
    Возведение матрицы m в целую положительную степень n.
    """
    k=len(m)
    if n==0:
        return ones(k)
    elif n==1:
        return m
    else:
        res=mult(m,m)
        if n==2:
            return res
        else:
            for i in range(0,n-2):
                res=mult(res,m)
            return res

def observe(a,c):
    """
    Тест наблюдаемости системы (a[n*n], c[k*n]).
    Если с-вектор, то он задан в виде вектора строки.
    """
    n=len(a)
    q=c.copy()
    for i in range(1,n):
        current=mult(c,mpow(a,i))
        if isvector(c):
            q.append(current)
        else:
            q.extend(current)
    if rank(q)==n:
        print("Линейная система полностью наблюдаема")
        return True
    else:
        print("Линейная система ненаблюдаема")
        return False

def horizontalconcat(m1,m2):
    """
    Горизонтальная конкатенация матриц m1,m2,
    или двух векторов, заданных в виде векторов строк,
    или матрицы и вектора столбца,
    заданного как вектор строка.
    """
    n=len(m1)
    if isvector(m2):
        strtocol(m1)
        strtocol(m2)
    for i in range(0,n):
        m1[i].extend(m2[i])
    return m1

def control(a,b):
    """
    Проверка управляемости системы (a[n*n],b[n*m]),
    если b-вектор столбец,
    то он задается как вектор строка.
    Матрица a не может иметь размерность 1*1.
    """
    n=len(a)
    u=b.copy()
    if isvector(b):
        u=strtocol(u)
    for i in range(1,n):
        current=mult(mpow(a,i),b)
        u=horizontalconcat(u,current)
    if rank(u)==n:
        print("Линейная система полностью управляема")
        return True
    else:
        print("Линейная система неуправляема")
        return False
                
        
        
        
            
            
            
