import numpy,itertools,numbers
import sys
import time
import math
from drawchar import charimage,puton
screenX=512 
screenY=288
#data=[n,t]
data=numpy.array([list(range(1,201,4)),list(range(50,100))])
data=numpy.array([[  3,   7,  13,  19,  24,  30,  35,  40,  46,  51,  56,  62,  67,
         73,  79,  84,  89,  93,  97, 101, 106, 110, 114, 119, 123],
       [  2,   6,  11,  16,  20,  24,  29,  34,  38,  44,  48,  52,  57,
         61,  65,  70,  75,  80,  86,  90,  96, 101, 106, 111, 117],
       [  3,   9,  13,  18,  23,  29,  35,  39,  43,  49,  54,  58,  63,
         69,  74,  78,  82,  87,  93,  97, 103, 108, 112, 116, 120]])
from math import sin,pi,log,sqrt
data=numpy.array([[10*i for i in range(10,1000)],
                  [10*i+5*sin(i*pi/6) for i in range(10,1000)],
                  [10*i+10*sin((i+3)*pi/6) for i in range(10,1000)]
                ])

data=numpy.array([[n for n in numpy.arange(0,10.01,0.01)],
                  [n*log(2+log(n+2)) for n in numpy.arange(0,10.01,0.01)],
                  [n*log(n+2) for n in numpy.arange(0,10.01,0.01)],
                  [n**(5/4) for n in numpy.arange(0,10.01,0.01)],
                  [n*sqrt(n) for n in numpy.arange(0,10.01,0.01)],
                  [n*sqrt(n)*log(n+2) for n in numpy.arange(0,10.01,0.01)],
                  [n*n/3 for n in numpy.arange(0,10.01,0.01)]
                ])



colors=numpy.array([[255,20,200],[50,255,0],[20,50,255],[200,0,0],[0,200,0],[0,200,200],[76,37,196]],"u1")
names="""n
nlog(2+log(n+2))
nlog(n+2)
n^(5/4)
nsqrtn
n*sqrtn*log(n+2)
n^2/3""".splitlines()
screen=numpy.ones([screenY,screenX,3],"u1")*255#[Y,X,rgb]
emptyscreen=numpy.ones([screenY,screenX,3],"u1")*255
import imageio
emptyscreen=imageio.imread("image_20.png")[:,:,(0,1,2)]

upY=10

intY=50
vY=2
barYth=30

leftX=10
rightX=10


bars=[]
def init():
    bars.clear()
    for index in range(data.shape[0]):
        bars.append({"Y":upY+index*intY,"index":index,"color":colors[index],"name":charimage(names[index])})
def main():
    init()
    import subprocess
    try:
        if 1:
            x=subprocess.Popen([#"ffmpeg",
                                "ffplay",
                                #"-y","-r","1",
                                "-f","rawvideo","-s",f"{screenX}x{screenY}","-pix_fmt","rgb24","-i","-"
                                #, "-pix_fmt" ,"yuv420p","out.mp4"
                                ],stdin=subprocess.PIPE
                               #,stderr=open("log.txt","wb",buffering=0)
                               )
        else:
            x=subprocess.Popen(["ffmpeg",
                                #"ffplay",
                                "-y",#"-r","1",
                                "-f","rawvideo","-s",f"{screenX}x{screenY}","-pix_fmt","rgb24","-i","-"
                                , "-pix_fmt" ,"yuv420p","out.mp4"
                                ],stdin=subprocess.PIPE
                               #,stderr=open("log.txt","wb",buffering=0)
                               )
        for t in range(data.shape[1]):
            #time.sleep(0.4)
            draw(t,x.stdin.write)
            x.stdin.flush()
    except:
        raise
    finally:
        x.stdin.close()


def draw(t,w):

    print(t)

    for bar in bars:
        bar["value"]=data[bar["index"],t]
    if 1:#bars not sorted:
        bars.sort(key=lambda x:x["value"],reverse=True)

    maxXstand=max(bars[0]["value"]*1.2,1)



    screen[:]=emptyscreen

        

    screenX_leftX_rightX=(screenX-leftX-rightX)/maxXstand
    _unit=10**math.floor(math.log10(maxXstand)-0.4 )
    #unit=int(_unit*screenX_leftX_rightX)
    
    
    #screen[:,list(range(leftX,screenX-rightX+1,unit))]=[200,200,200]
    for i in numpy.arange(0,maxXstand+0.01,_unit):
        ___X=leftX+int(i*screenX_leftX_rightX)
        screen[:,___X]=(200,200,200)
        if i.is_integer():
            i=int(i)
            text=charimage(str(i))
        else:
            text=charimage(f"{i:.4}")
        puton(text,___X-text.shape[1]//2,140,screen)

        
    
    for bar,targetY in zip(bars,itertools.count(upY,intY)):
        if t:
            diff=bar["Y"]-targetY
            if diff>0:
                bar["Y"]-=min(vY,diff)
            elif diff<0:
                bar["Y"]-=max(-vY,diff)
        else:
            bar["Y"]=targetY
        barX=int(bar["value"]*screenX_leftX_rightX)
        screen[bar["Y"]:bar["Y"]+barYth,leftX:barX+leftX]=bar["color"]
        text=bar["name"]
        puton(text,barX+leftX-text.shape[1],bar["Y"],screen)
        val=(bar["value"])
        text=charimage(str(val) if isinstance(val,numbers.Integral) else f'{val:.4}')
        puton(text,barX+leftX,bar["Y"],screen)
    w(screen)
main()
    
