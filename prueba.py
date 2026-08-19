import json

output: dict = {}


def limpiar_valor(value: str):
    value = value.strip()
    try:
        value = int(value)
    except ValueError:
        pass
    return value


def parsear_titulos(titulos: str):
    return titulos.replace(" ", "").replace("(", "").replace("`", "")[:-3:].split(",")


def parsear_fila(fila: str):
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


def json_creation(to_dump: dict):
    with open("output.json", "w") as file_final:
        json.dump(to_dump, file_final)


with open("zonas.sql", "r") as file:
    output: dict = {}
    titulos: list = []
    titulos = parsear_titulos(file.readline())
    # print(titulos)
    for line in file:
        fila_lista: list = parsear_fila(line)
        # print(fila_lista)

        assert len(titulos) == len(fila_lista), (
            "No coincide la cantidad de elementos con la cantidad de titulos, podrias perder info"
        )

        zipped_list: dict = dict(zip(titulos, fila_lista))
        output[fila_lista[0]] = zipped_list
        # print(output)

    json_creation(output)
