##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR5: Textures
##  LUIS PEDRO CUÉLLAR - 18220
##


import struct
from object import Object


##  char --> 1 byte
def char(var):
    return struct.pack('=c', var.encode('ascii'))

##  word --> 2 bytes
def word(var):
    return struct.pack('=h', var)

##  dword --> 4 bytes
def dword(var):
    return struct.pack('=l', var)

##  function that puts the rgb value of a color into bytes
def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

##  this function does the cross of two arrays
def cross(a, b):
    length = len(a)
    c = []

    if length == 2 :
        c.append((a[0] * b[1]) - (a[1] * b[0]))

    elif length == 3 :
        c.append((a[1] * b[2]) - (a[2] * b[1]))
        c.append(-((a[0] * b[2]) - (a[2] * b[0])))
        c.append((a[0] * b[1]) - (a[1] * b[0]))

    return c

## this function does the difference between two arrays
def subtract(a, b):
    length = len(a)
    c = []

    if length == 2 :
        c.append(a[0] - b[0])
        c.append(a[1] - b[1])

    elif length == 3 :
        c.append(a[0] - b[0])
        c.append(a[1] - b[1])
        c.append(a[2] - b[2])

    return c

##  this fucntion does the norm of a vector
def norm(a):
    length = len(a)
    c = 0

    if length == 2 :
        c = (a[0] ** 2) + (a[1] ** 2)
        c = c ** 0.5


    elif length == 3 :
        c = (a[0] ** 2) + (a[1] ** 2) + (a[2] ** 2)
        c = c ** 0.5

    return c

##  this function does the dot product between two arrays or numbers
def dot(a, b):
    is_a_Array = isinstance(a, list)
    is_b_Array = isinstance(b, list)
    c = 0

    if (is_a_Array == True) and (is_b_Array == True) :
        length = len(a)

        if length == 2:
            c = (a[0] * b[0]) + (a[1] * b[1])

        else :
            c = (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])

    else:
        c = a * b

    return c

##  this function calculates the barycentric coordinates
def barycentric_coords(a, b, c, p):
    ##  u => a
    ##  v => b
    ##  w => c
    try:
        u = (((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) /
              ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

        v = (((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) /
              ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

class Render(object):
    def __init__(self, width, height, background = None):
        self.glInit(width, height, background)
        self.current_color = color(1, 1, 1)

    ##  initiates the image with the width, height and background color
    def glInit(self, width, height, background):
        background = color(0, 0, 0) if background == None else background

        self.bg_color = background

        self.glCreateWindow(width, height)

    ##  creates the window with the given
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear(self.bg_color)

    ##  colors the image with the background color
    def glClear(self, bg_color):
        self.bg_color = bg_color
        self.pixels = [ [ self.bg_color for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

    ##  defines an area inside the window in which it can be drawn points and lines
    def glViewPort(self, x, y, width, height):
         self.vp_x = x
         self.vp_y = y
         self.vp_width = width
         self.vp_height = height

    ##   changes de background color of the image
    def glClearColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

        self.bg_color = color(self.r, self.g, self.b)

        self.glClear(self.bg_color)

    ##  draws a point in the image with the given NDC coordinates
    def glVertex(self, x, y):
        ver_x = int(((x + 1) * (self.vp_width / 2)) + self.vp_x)
        ver_y = int(((y + 1) * (self.vp_height / 2)) + self.vp_y)
        self.pixels[round(ver_y)][round(ver_x)] = self.current_color

    ##  draws a pint in the image with pixel coordinates
    def glVertex_coordinates(self, x, y):
        self.pixels[y][x] = self.current_color

    ##  changes the color of the points that can be drawn
    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    ##  draws a straight line from (x0, y0) to (x1, y1)
    def glLine(self, x0, y0, x1, y1):
        x0 = round(( x0 + 1) * (self.vp_width  / 2 ) + self.vp_x)
        x1 = round(( x1 + 1) * (self.vp_width  / 2 ) + self.vp_x)
        y0 = round(( y0 + 1) * (self.vp_height / 2 ) + self.vp_y)
        y1 = round(( y1 + 1) * (self.vp_height / 2 ) + self.vp_y)

        dx = x1 - x0
        dy = y1 - y0

        steep = abs(dy) > abs(dx)

        if steep :
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1 :
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep :
                self.glVertex_coordinates(y, x)
            else :
                self.glVertex_coordinates(x, y)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    ##  this function draws a line in between to pixel coordinates. Starts in (x0, y0) and ends in (x1, y1)
    def glLine_coordinates(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep :
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1 :
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        try :
            m = dy/dx
        except ZeroDivisionError:
            pass
        else :
            y = y0

            for x in range(x0, x1 + 1) :
                if steep :
                    self.glVertex_coordinates(y, x)
                else :
                    self.glVertex_coordinates(x, y)

                offset += m
                if offset >= limit :
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def transform(self, vertex, scale = [1, 1, 1], translate = [0, 0, 0]) :
        transformed =[  round(vertex[0] * scale[0] + translate[0]),
                        round(vertex[1] * scale[1] + translate[1]),
                        round(vertex[2] * scale[2] + translate[2])  ]
        return transformed

    ##  this function loads the model for it to be drawn
    def loadModel(self, filename, translate, scale, is_wireframe, texture = None):
        model = Object(filename)

        for face in model.faces :
            count_vertices = len(face)

            if is_wireframe:
                for vertex in range(count_vertices) :
                    v0 = model.vertices[face[vertex][0] - 1]
                    v1 = model.vertices[face[(vertex + 1) % count_vertices][0] - 1]

                    x0 = round(v0[0] * scale[0] + translate[0])
                    y0 = round(v0[1] * scale[1] + translate[1])

                    x1 = round(v1[0] * scale[0] + translate[0])
                    y1 = round(v1[1] * scale[1] + translate[1])

                    self.glLine_coordinates(x0, y0, x1, y1)
            else:
                light = [0, 0, 1]

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]

                v0 = self.transform(v0, scale, translate)
                v1 = self.transform(v1, scale, translate)
                v2 = self.transform(v2, scale, translate)

                if count_vertices > 3 :
                    v3 = model.vertices[face[3][0] - 1]
                    v3 = self.transform(v3, scale, translate)

                if texture :
                    vt0 = model.texture_coords[face[0][1] - 1]
                    vt1 = model.texture_coords[face[1][1] - 1]
                    vt2 = model.texture_coords[face[2][1] - 1]

                    if count_vertices > 3 :
                        vt3 = model.texture_coords[face[3][1] - 1]

                else :
                    vt0 = [0, 0]
                    vt1 = [0, 0]
                    vt2 = [0, 0]
                    vt3 = [0, 0]

                normal = cross(subtract(v1, v0), subtract(v2, v0))
                norm_normal = norm(normal)

                try:
                    for i in range(len(normal)) :
                        normal[i] = normal[i] / norm_normal
                except ZeroDivisionError:
                    pass

                intensity = dot(normal, light)

                if intensity >= 0 :
                    self.triangle_barycentric_coordinates(v0, v1, v2, intensity, texture = texture, texture_coords = (vt0, vt1, vt2))

                    if count_vertices > 3 :
                        self.triangle_barycentric_coordinates(v0, v2, v3, intensity, texture = texture, texture_coords = (vt0, vt2, vt3))


    ##  this fucntion draws a polygon with the given coordinates
    def glDrawPolygon(self, poly):
        length = len(poly)

        for i in range(length) :
            p0 = poly[i]
            p1 = poly[(i + 1) % length]

            self.glLine_coordinates(p0[0], p0[1], p1[0], p1[1])

            for x in range(self.width) :
                for y in range(self.height) :
                    if self.evenOdd(poly, x, y) :
                        self.glVertex_coordinates(x, y)

    ##  this function checks if a point is inside the polygon
    ##  code used in this function is in https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule#Implementation
    def evenOdd(self, poly, x, y):
        length = len(poly)
        i = 0
        j = 0
        j = length - 1
        c = False

        for i in range(length) :
            if ((poly[i][1] > y) != (poly[j][1] > y)) and (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1])) :
                c = not c
            j = i
        return c

    ##  this function draws triangles with barycentric coordinates
    def triangle_barycentric_coordinates(self, A, B, C, intensity = 1, texture = None, texture_coords = ()):
        ## definding box limits
        minX = min(A[0], B[0], C[0])
        maxX = max(A[0], B[0], C[0])

        minY = min(A[1], B[1], C[1])
        maxY = max(A[1], B[1], C[1])

        for x in range(minX, maxX + 1) :
            for y in range(minY, maxY + 1) :
                if (x >= self.width) or (x < 0) or (y >= self.height) or (y < 0):
                    continue

                point = [x, y]
                u, v, w = barycentric_coords(A, B, C, point)

                if (u >= 0) and (v >= 0) and (w >=0) :
                    z = A[2] * u + B[2] * v + C[2] * w

                    if z > self.zbuffer[y][x] :
                        b, g , r = color(1, 1, 1)
                        b /= 255
                        g /= 255
                        r /= 255

                        b *= intensity
                        g *= intensity
                        r *= intensity


                        if texture :
                            ta, tb, tc = texture_coords
                            tx = ta[0] * u + tb[0] * v + tc[0] * w
                            ty = ta[1] * u + tb[1] * v + tc[1] * w

                            texColor = texture.getColor(tx, ty)
                            b *= texColor[0] / 255
                            g *= texColor[1] / 255
                            r *= texColor[2] / 255

                        self.current_color = color(r, g, b)
                        self.glVertex_coordinates(x, y)
                        self.zbuffer[y][x] = z

    ##  this function is used to write the image into the file, and saves it
    def glFinish(self, filename):
        file = open(filename, 'wb')

        ##  file header --> 14 bytes
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))

        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        ##  image header --> 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        ##  pixels --> 3 bytes each

        for x in range(self.height) :
            for y in range(self.width) :
                file.write(self.pixels[x][y])

        file.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth, depth, depth))

        archivo.close()
