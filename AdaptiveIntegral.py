def qstep(f,a,b,tol,fa,fc,fb):
    h1=b-a
    h2=h1/2
    c=(a+b)/2
    fd=f((a+c)/2)
    fe=f((c+b)/2)
    I1=h1*(fa+4*fc+fb)/6
    I2=h2*(fa+4*fd+2*fc+4*fe+fb)/6
    if abs(I2-I1)<tol:
        I=I2+(I2-I1)/15
    else:
        Ia=qstep(f,a,c,tol,fa,fd,fc)
        Ib=qstep(f,c,b,tol,fc,fe,fb)
        I=Ia+Ib
    return I

def quadadapt(f,a,b,tol=0.000001):
    c=(a+b)/2
    fa=f(a)
    fc=f(c)
    fb=f(b)
    return qstep(f,a,b,tol,fa,fc,fb)