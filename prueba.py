import json


def limpiar_valor(value: str) -> str | int:
    value = value.strip()
    try:
        if value.isnumeric() and value[0] == "0":
            return value
        value = int(value)
    except ValueError:
        pass
    return value


def parsear_titulos(titulos: str) -> list:

    return (
        titulos[titulos.find("(") + 1 : titulos.rfind(")")]
        .replace(" ", "")
        .replace("`", "")
        .split(",")
    )


def parsear_fila(fila: str) -> list:
    estoy_en_valor: bool = False

    fila: str = fila.strip()[1:-2:]
    # print(fila)

    temp_value: str = ""
    fila_list: list = []

    # Chequeo si estoy recorriendo valor
    for char in fila:
        if char == "'":
            estoy_en_valor = not estoy_en_valor
            continue

        if (char != ",") or (char == "," and estoy_en_valor == True):
            temp_value += char
            # print(temp_value)

        elif char == "," and estoy_en_valor == False:
            temp_value = limpiar_valor(temp_value)
            fila_list.append(temp_value)

            temp_value = ""

    if temp_value != "":
        fila_list.append(limpiar_valor(temp_value))

    return fila_list


def json_creation(to_dump: dict, file_name: str) -> str:
    output_file_name: str = file_name + "_output.json"
    # print(to_dump)
    with open(output_file_name, "w", encoding="utf-8") as file_final:
        json.dump(to_dump, file_final, ensure_ascii=False, indent=4)
    return output_file_name


####


def parsear_archivo(file_name: str, output_dict_key: str) -> dict:
    with open(file_name, "r", encoding="utf-8") as file:
        output: dict = {}
        titulos: list = []
        titulos = parsear_titulos(file.readline())
        # print(titulos)
        filas_procesadas: int = 0

        for line in file:
            # chequeo que no sea linea de insert
            if line[0] != "(":
                continue

            fila_lista: list = parsear_fila(line)
            # print(fila_lista)

            assert len(titulos) == len(fila_lista), (
                "No coincide la cantidad de elementos con la cantidad de titulos, podrias perder info"
            )

            zipped_list: dict = dict(zip(titulos, fila_lista))
            output[zipped_list[output_dict_key]] = zipped_list
            # print(output)

            filas_procesadas += 1

        assert filas_procesadas == len(output), (
            "Hay claves repetidas, se pisaron usuarios"
        )
        return output


def armar_usuario_para_zonas(usuario:dict) -> dict:
    usuario_final:dict = {}
    
    usuario_final["nombre"] = usuario["nombre"]
    usuario_final["apellido"] = usuario["apellido"]
    usuario_final["email"] = usuario["email"]
    usuario_final["telefono"] = usuario["telefono"]
    
    return usuario_final

def cruzar_usuarios_x_zonas(zonas: dict, usuarios: dict) -> dict:

    output: dict = {}
    output["Zona no especificada"] = [] 
    for key, value in zonas.items():
        output[
            value["nombre"]
        ] = []  # hago esto pq nlo tengo por id en usuarios, ya q era una tabla sql


    for key_usuario, dict_usuario in usuarios.items():
        if zonas.get(dict_usuario["zona_id"]) is None:
            output["Zona no especificada"].append(armar_usuario_para_zonas(dict_usuario))
        else:
            output[zonas[dict_usuario["zona_id"]]["nombre"]].append(armar_usuario_para_zonas(dict_usuario))
            
 
    # print(output)lñopppppppppppppppppppppppppppppooo
    #$
    return output


zonas_parseado: dict = parsear_archivo("zonas.sql", "id")
# print(zonas_parseado)
usuarios_parseado: dict = parsear_archivo("usuarios.sql", "email")
# print(usuarios_parseado)

usuarios_x_zonas: dict = cruzar_usuarios_x_zonas(zonas_parseado, usuarios_parseado)
print(usuarios_x_zonas)

created_file: str = json_creation(usuarios_x_zonas, "usuarios por zonas")
