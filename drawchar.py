import pygame.font,numpy
pygame.font.init()

import functools
@functools.lru_cache(maxsize=128, typed=False)
def charimage(str_):

    font=pygame.font.SysFont(
        #"Segoe UI",
        None,
        16)
    x=font.render(str_,1,(0,0,0))

    return numpy.frombuffer(x.get_buffer(),("u1",(x.get_width(),4)))[:,:,(3,3,3)]
def puton(string,x,y,targ):
    #global targ_,string_
    if x<0:
        string=string[:,-x:]
        x=0
    if y<0:
        string=string[-y:,:]
        y=0
        
    #string=string[-y:,-x:]
    #x=max(0,x)
    #y=max(0,y)

    #print(string)
    targ=targ[y:,x:]
    Y,X,*_=targ.shape
    string=string[:Y,:X]
    #print(string)
    Y,X,*_=string.shape
    #targ_=targ
    #string_=string
    #print(targ[:Y,:X],y,x,Y,X)
    targ[:Y,:X]=numpy.floor((1-string/255)*targ[:Y,:X])


#_a=numpy.array([[1]])
#_b=numpy.array([[1,2],[3,4]])
#_c=numpy.array([[10,20],[30,40]])
