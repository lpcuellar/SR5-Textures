##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR5: Textures
##  LUIS PEDRO CUÉLLAR - 18220
##

from gl import Render, color
from object import Object, Texture

title = "---    APLICAR TEXTURAS A MOBDELOS OBJ    ---\n"
main_menu = """Opciones:
        1. Cambiar color de fondo (default = negro)
        2. Aplicar textura a una cara
        3. Salir
        """

wants_to_continue = True
option = 0
r = 0
g = 0
b = 0
are_values_ok = False

render = Render(1000, 1000)

print(title)
while(wants_to_continue):
    print(main_menu)
    option = input("        Ingrese la opción que desea realizar: ")
    option = int(option)

    ##  changes the background color of the image
    if(option == 1):
        is_values_ok = False

        ## ask the values for the rgb and check that they are valid
        while(is_values_ok == False):
            r = input("Ingrese el valor r del color deseado (de 0 a 1): ")
            r = float(r)
            g = input("Ingrese el valor g del color deseado (de 0 a 1): ")
            g = float(g)
            b = input("Ingrese el valor b del color deseado (de 0 a 1): ")
            b = float(b)

            if((r < 0 or r > 1) or (g < 0 or g > 1) or (b < 0 or b > 1)):
                print("\nPor favor escoger valores entre 0 y 1\n")
            else:
                is_values_ok = True

                ##  changes the background color of the image
                render.glClearColor(r, g, b)

    ##  apply texture to a face
    elif(option == 2):
        texture = Texture('./textures/model.bmp')
        render.loadModel('./models/model.obj', (500, 500, 0), (300, 300, 300), False, texture)
        render.glFinish("face.bmp")
        # print("Termiado!")
        wants_to_continue = False

    ##  exits the program
    elif(option == 3):
        wants_to_continue = False
        print("BYEEE")

    else:
        print("Por favor escoja una opción válida!")
