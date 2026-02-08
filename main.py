import pygame 
import numpy as np
import sys

def cam(vector):
    angle = np.pi/3.
    f = 50
    n = 1
    vector = np.append(vector,1)
    trans = np.array(
        [
            [np.tan(angle),0,0,0],
            [0,np.tan(angle),0,0],
            [0,0,(f+n)/(f-n),-(2*n*f)/(f-n)],
            [0,0,1,0]
        ]
    )

    trans2 = np.array(
        [
            [1/np.tan(angle),0,0,0],
            [0,1/np.tan(angle),0,0],
            [0,0,(2*f)/(f-n),1],
            [0,0,-(f*n)/(2*f-n),0]
        ]
    )
    camPos = [0,0,5]
    phi = np.pi/4.
    x = np.cos(phi)
    z = np.sin(phi)
    #x = 1
    #print(x)
    cam = np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,2],
        [0,0,0,1]
    ])
    camInv = np.linalg.inv(cam)
    
    vector = camInv @ vector

    vector = trans @ vector
    last_element = vector.item(-1)
    
    return vector/last_element
    

def cam2(points,xxx):
    points = np.insert(points,3,1,axis=1)

    angle = np.pi/3.
    f = 50
    n = 1
    
    trans = np.array(
        [
            [np.tan(angle),0,0,0],
            [0,np.tan(angle),0,0],
            [0,0,(f+n)/(f-n),(2*n*f)/(f-n)],
            [0,0,-1,0]
        ]
    )
    trans2 = np.array(
        [
            [1/np.tan(angle),0,0,0],
            [0,1/np.tan(angle),0,0],
            [0,0,(2*f)/(f-n),(f*n)/(2*f-n)],
            [0,0,-1,0]
        ]
    )
    camera = xxx.final
    
    points = np.linalg.inv(camera) @ np.rot90(points,-1)
    points =  trans @ points
    points = np.rot90(points,1)

    last_element = (points[:,3]).reshape(-1,1)
    points[:,:3] = points[:,:3] / last_element
   
    return points
class Camera:
    def __init__(self,position):
        self.position = position
        self.vectorXYZ = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1]
        ])
        self.vectorXZ = np.array([
            [1,0],
            [0,0],
            [0,1]
        ])
        self.final = np.full((4,4),0.)
        self.final[:3,3] = position
        self.final[3,3] = 1.
        self.rotateY(0)

    def rotateY(self,angle):
        Ry = np.array([
            [np.cos(angle),0,-np.sin(angle)],
            [0,1,0],
            [np.sin(angle),0,np.cos(angle)]
            ])
            
        self.vectorXYZ = Ry @ self.vectorXYZ
        self.vectoeXZ = Ry @ self.vectorXZ
        

        self.final[:3,0] = self.vectorXYZ[:,0]
        self.final[:3,1] = self.vectorXYZ[:,1]
        self.final[:3,2] = self.vectorXYZ[:,2]
    def rotateX(self,angle):
        Ry = np.array([
            [1,0,0],
            [0,np.cos(angle),-np.sin(angle)],
            [0,np.sin(angle),np.cos(angle)]
            ])
            
        self.vectorXYZ = Ry @ self.vectorXYZ
        self.final[:3,0] = self.vectorXYZ[:,0]
        self.final[:3,1] = self.vectorXYZ[:,1]
        self.final[:3,2] = self.vectorXYZ[:,2]
        
    def left(self):
        vel = .1
        amount = self.vectorXYZ[:,0] * vel
        self.position -= amount 
        self.final[:3,3] = self.position
        

    def right(self):
        vel = .1
        amount = self.vectorXYZ[:,0] * vel
        self.position += amount
        self.final[:3,3] = self.position
        
    def forward(self):
        #print(self.final)
        vel = .1
        amount = self.vectorXYZ[:,2] * vel
        self.position -= amount
        self.final[:3,3] = self.position
        
    def back(self):
        vel = .1
        amount = self.vectorXYZ[:,2] * vel
        self.position += amount
        self.final[:3,3] = self.position
        
    def up(self):
        vel = .1
        amount = np.array([0,vel,0])
        self.position -= amount
        self.final[:3,3] = self.position
        
    def down(self):
        vel = .1
        amount = np.array([0,vel,0])
        self.position += amount
        self.final[:3,3] = self.position
        
        
def render(cube,camera):
    #print("asddsdasdsas",cube.vertices)
    cube.verticesT = cam2(cube.vertices,camera)
    cube.Draw()


class Cube:
    def __init__(self,pos):
        self.size = 1
        self.pos = np.array(pos)
        self.vertices = [0 for i in range(8)]
        self.verticesT = []
        self.indexBuffer = [[0,2,1],[1,2,3],[3,2,4],[3,4,5],[5,4,6],[5,6,7],[7,6,1],[1,6,0],[1,3,7],[3,5,7],[0,6,2],[2,6,4]]
        self.setVertex()
    def setVertex(self):
        r = self.size
        p = self.pos
        
        self.vertices[0] = p
        self.vertices[1] = p + [0,-r,0]
        self.vertices[2] = p + [r,0,0]
        self.vertices[3] = p + [r,-r,0]

        self.vertices[4] = p + [r,0,-r]
        self.vertices[5] = p + [r,-r,-r]
        self.vertices[6] = p + [0,0,-r]
        self.vertices[7] = p + [0,-r,-r]
        self.vertices = np.array(self.vertices)

    def RotateX(self,angle):
        Rx = np.array([
            [1,0,0],
            [0,np.cos(angle),-np.sin(angle)],
            [0,np.sin(angle),np.cos(angle)]
        ])
        self.vertices = self.vertices @ Rx
    def Draw(self):
        scale = 50
        translate = (250,250)
        index = self.indexBuffer
 
        vertices = self.verticesT[:,:3]
        a = vertices[1]-vertices[0]
        b = vertices[2]-vertices[0]
       
        #pygame.draw.circle(screen,"red",vertices[1][:2]*scale+translate,3)

        for vertice in index:

            A = self.verticesT[vertice[0]]
            B = self.verticesT[vertice[1]]
            C = self.verticesT[vertice[2]]

            """
            pygame.draw.circle(screen,"red",C[:2]*scale+translate,3)
            pygame.draw.circle(screen,"magenta",A[:2]*scale+translate,3)
            pygame.draw.circle(screen,"green",B[:2]*scale+translate,3)
            """
            norm = normalV(A,B,C)
            
            #pygame.draw.line(screen,"black",C[:2]*scale+translate,norm[:2]*scale+translate,3)
            if(norm[2] < 0):
                #vertices = 0
                triangle = []
                outside = []
                for j in vertice:
                    triangle.append(vertices[j])

                for afuera in triangle:
                    outside.append(afuera[:2]*scale+translate)
                pygame.draw.lines(screen,"red",True,outside)

                if inOut(triangle) == 0:
                    for j,val in enumerate(triangle):
                        triangle[j] = val[:2]*scale+translate
                    pygame.draw.polygon(screen,"white",triangle)
                    #print(triangle[0])
                    pygame.draw.lines(screen,"black",True,triangle)
                elif inOut(triangle) == 1:
                    continue
                else:
                    
                    triangulos = clipping(inOut(triangle))
                    #print(triangulos)
                    for i in triangulos:
                        triangulo = []
                        for j in i:
                            triangulo.append(j[:2]*scale+translate)
                        pygame.draw.polygon(screen,"white",triangulo)
                        pygame.draw.lines(screen,"black",True,triangulo)
                        
                    

                

def normalV(origin,B,C):
    Bvec = origin - B  
    Cvec = origin - C 
    normal = np.cross(Bvec[:3],Cvec[:3])
    return normal#/ np.linalg.norm(normal)   
def inOut(vertices):
    inside = []
    outside = []
    
    for i in vertices:
        if i[1] < -1:
            outside.append([i,"t"])
            
        elif i[0] > 1:
            outside.append([i,"r"])
        elif i[1] > 1:
            outside.append([i,"b"])
        elif i[0] < -1:
            outside.append([i,"l"])
        else:
            
            inside.append(i)
    # Dibijar los triangulos actuales
    if outside == []:
        return 0
    elif inside == []:
        return 1
    else:
        return [inside,outside]
def clipping(vertex):
    inside,outside = vertex
    #print("asdsadsda",inside)
    triangles = []
    a = 0
    b = 0
    c = 0
    if len(inside) == 1:
        a = inside[0]
        b = intersection(a,outside[0][0],outside[0][1])
        c = intersection(a,outside[1][0],outside[1][1])
        triangles.append([a,b,c])
    else:
        #Triangulo 1
        a = inside[0]
        b = inside[1]
        c = intersection(a,outside[0][0],outside[0][1])
        triangles.append([a,b,c])
        #Triangulo 2
        a = b
        b = intersection(a,outside[0][0],outside[0][1])
        triangles.append([a,b,c])
    return triangles
        
        

def intersection(PIn,POut,side):
    #print("fadsfdsaf\n",PIn)
    a = PIn[0]
    b = PIn[1]
    c = PIn[2]
    u = POut[0]
    v = POut[1]
    w = POut[2]
    deno = 2*(-v+b)
    deno2 = 2*(a-u)
    num1 = -(b*u-u+a-b+v-a*v)
    lamda,alpha,= (0,0)
    # Vertical
    if side == "b":
        lamda = num1/deno
        alpha = (c*v-v+b-c-b*w+w)/deno

    #Horizontal
    elif side == "r":
        lamda = num1/deno2
        alpha = (c*u-u+a+c-w-a*w)/deno2
    elif side =="l":
        lamda=-(-b*u+u-a-b+v+a*v)/(2*(u-a))
        alpha = (-c*u+u-a-c+w+a*w)/(2*(u-a))
    elif side == "t":
        lamda = -(-b*u-u+a+b-v+a*v)/(2*(v-b))
        alpha = (-c*v+v-b+c+b*v-c)/(2*(v-b))
        pass   
    vertice = 0
    if side == "t":
        vertice = np.array([1-2*lamda,-1,1-2*alpha])
    # Correcto
    elif side == "r":
        vertice = np.array([1,1+2*lamda,1-2*alpha])
    # Correcto
    elif side == "b":
        vertice = np.array([1-2*lamda,1,1-2*alpha])
    elif side == "l":
        vertice = np.array([-1,1+2*lamda,1-2*alpha])
    
    return vertice



WHITE = (255, 255, 255)

pygame.init()
height = 500
width = 500   
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

cubo = Cube([0,0,0])
camera = Camera([0,0,3])
#archivo_obj = Wavefront('C:/Users/carlo/Documents/Python/graphix/mountains.obj')
#vertices = np.array(archivo_obj.)

vertices = cubo.vertices


running = True
angle = 0
phi = 0
horizontal,vertical,front = (0,0,2)
# Creamos un objeto Clock
def tex(text,pos):
    font = pygame.font.Font(None, 20)
    fps_text = font.render(text, 1, WHITE)
    screen.blit(fps_text, pos)
    

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            #running = False

    screen.fill("blue")
    pygame.draw.polygon(screen,"black",[(200,300),(300,300),(300,200),(200,200)],1)
    verticesT = cam2(vertices,camera)

    #for i in verticesT:
        #pygame.draw.circle(screen,"white",i[:2]*50+(250,250),1)
    cubo.RotateX(.02)
    render(cubo,camera)
    mov = pygame.mouse.get_rel()
    evento = pygame.event.get()
    #tex(str(evento),(0,100))   


    if mov[0] != 0 or mov[1] != 0:
        camera.rotateY(mov[0]/500)
        #camera.rotateX(mov[1]/500)

    

    # Mostramos los FPS en la pantalla
    fps = str(int(clock.get_fps()))
    tex(fps,(10,10))

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        camera.left()
        
        #print("Has presionado la letra 'a'")
    elif teclas[pygame.K_d]:
        camera.right()
        
    elif teclas[pygame.K_w]:
        camera.forward()
        
    elif teclas[pygame.K_s]:
        camera.back()
        
    elif teclas[pygame.K_SPACE]:
        camera.up()
        
    elif teclas[pygame.K_LSHIFT]:
        camera.down()
        
    #print(teclas)
    if event.type == pygame.KEYDOWN:
        
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    #break
    pygame.display.flip()
    clock.tick(60)

