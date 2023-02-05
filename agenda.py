import re

# Excepciones


class NumeroTelefonicoException(Exception):

    def __init__(self):
        super().__init__("Numero telefonico no valido")


class EsUnicoException(Exception):

    def __init__(self):
        super().__init__("Este valor no es unico")


class Contacto:

    def __init__(self, nombre, telefonos, id=0):
        self.id = id
        self.nombre = nombre
        self.telefonos = telefonos


class Agenda:

    actualID = 1
    contactos: list[Contacto] = []
    locacionesTelefonos = ["NumCelular", "NumCasa", "NumTrabajo"]

    def __init__(self):
        pass

    def buscarContacto(self, nombre):
        contactosObjetivo = list(
            filter(lambda contacto: nombre in contacto.nombre, self.contactos))
        return contactosObjetivo

    def mostrarContacto(self, contacto: Contacto):
        print("=="*20)
        print("| Nombre:\t", contacto.nombre)
        for key, telefono in dict.items(contacto.telefonos):
            print(f"| {key}: {telefono}")
        print("=="*20)

    def mostrarAgenda(self, contactos=[]):
        if len(self.contactos) > 0 or len(contactos) > 0:
            print("CONTACTOS")
            if len(contactos) > 0:
                for contacto in contactos:
                    print(f"| [ {contacto.id} ] ", contacto.nombre)
            else:
                for contacto in self.contactos:
                    print(f"| [ {contacto.id} ] ", contacto.nombre)
            print(f"| [ 0 ] SALIR")
            self.sub_menu()
        else:
            print("No hay contactos")

    # CRUD

    def sub_menu(self):
        if len(self.contactos) == 0:
            print("No hay contactos")
            return

        print("Escribe el nombre completo del contacto o el numero entre [ ]")
        opcion = input(">").strip()

        if opcion == "0" or opcion == "SALIR":
            return

        if opcion.isnumeric():
            contacto = [x for x in self.contactos if x.id == int(opcion)][0]
            self.consultarContacto(contacto)
        else:
            contactos = list(
                filter(lambda contactoTemp: opcion.lower() in contactoTemp.nombre.lower(), self.contactos))
            if len(contactos) > 1:
                print("Resultados de busqueda...")
                self.mostrarAgenda(contactos)
            elif len(contactos) == 1:
                self.consultarContacto(contactos[0])
            else:
                print("Ningun contacto encontrado")
                self.mostrarAgenda()

    def consultarContacto(self, contacto):
        self.mostrarContacto(contacto)
        print("| [ 1 ] Editar")
        print("| [ 2 ] Eliminar")
        print("| [ 3 ] Regresar")
        print("| [ 4 ] Volver a Menu")
        opcion = input(">")
        if opcion == "1":
            self.actualizarContacto(
                contacto.id, contacto.nombre, contacto.telefonos)
        elif opcion == "2":
            self.eliminarContacto(contacto)
        elif opcion == "3":
            self.mostrarAgenda()
        elif opcion == "4":
            return
        else:
            print("Opcion no valida...")
            self.consultarContacto(contacto)

    def eliminarContacto(self, contacto: Contacto):
        try:
            index = self.contactos.index(contacto)
            self.contactos.pop(index)
        except IndexError:
            print("Error en index")
        except ValueError:
            print("No se pudo encontrar el contacto")
            self.mostrarAgenda()

    def actualizarContacto(self, id, nombre, telefonos):
        try:
            nombreTemp = input(
                "Nombre contacto (Dejar vacio para no actualizar):").strip()
            nombre = nombreTemp if len(nombreTemp) > 0 else nombre

            if not self._check_nombre(nombre):
                raise ValueError
            print("Deja el numero vacio si no quieres actualizar")
            i = 0
            while i < len(self.locacionesTelefonos):
                locacion = self.locacionesTelefonos[i]
                # Sirve para en caso de repetir no se vuelva a capturar el telefono
                telefonoTemp = input(f"{locacion}> ").strip()

                # Checa el telefono en caso de que sea correcto lo agrega al dict de telefonos.
                if telefonoTemp == "":
                    i += 1
                elif self._check_telefono(telefonoTemp):
                    telefonos[locacion] = telefonoTemp
                    i += 1
                else:
                    raise NumeroTelefonicoException
            contacto = Contacto(nombre, telefonos, id)
            contactoAntiguo = list(
                filter(lambda contactoTemp: contacto.id == contactoTemp.id, self.contactos))[0]
            self.contactos[self.contactos.index(contactoAntiguo)] = contacto
        except ValueError as error:
            print(error)
            self.actualizarContacto(id, nombre, telefonos)
        except NumeroTelefonicoException as error:
            print("Formato de telefono no valido")
            self.actualizarContacto(id, nombre, telefonos)
        except Exception as error:
            print("Error al registrar, vuelvalo a intentar")
            self.actualizarContacto(id, nombre, telefonos)
        else:
            print("Actualizacion exitosa!")

    def crearContacto(self, nombre="", telefonos={}):
        try:
            if nombre == "":
                nombre = input("Nombre contacto:").strip()
                if not self._check_nombre(nombre):
                    raise ValueError
            print(
                "Puede dejar el numero telefonico vacio pero almenos debe de solicitar uno")
            i = 0
            while i < len(self.locacionesTelefonos):
                locacion = self.locacionesTelefonos[i]
                # Sirve para en caso de repetir no se vuelva a capturar el telefono
                if locacion in telefonos:
                    if self._check_telefono(telefonos[locacion]):
                        i += 1
                        continue

                telefonoTemp = input(f"{locacion}> ").strip()
                # Checa el telefono en caso de que sea correcto lo agrega al dict de telefonos.
                if telefonoTemp == "":
                    i += 1
                elif self._check_telefono(telefonoTemp):
                    telefonos[locacion] = telefonoTemp
                    i += 1
                else:
                    raise NumeroTelefonicoException

        except ValueError as error:
            print(error)
            self.crearContacto(nombre, telefonos)
        except NumeroTelefonicoException as error:
            print("Formato de telefono no valido")
            self.crearContacto(nombre, telefonos)
        except Exception as error:
            print("Error al registrar, vuelvalo a intentar")
            self.crearContacto(nombre, telefonos)
        else:
            contacto = Contacto(nombre, telefonos, self.actualID)
            self.actualID += 1
            self.contactos.append(contacto)

    def _check_telefono(self, telefono):
        try:
            # Esta expresion checa que el telefono contenga numeros de incio a fin y que solo contenga 10 digitos
            esCorrecto = re.search("^[0-9]{10}$", telefono)
            return esCorrecto
        except Exception as error:
            print(error)

    def _check_nombre(self, nombre):
        try:
            esCorrecto = len(nombre) > 0
            # checa si el nombre es correcto en su formato
            return esCorrecto
        except Exception as error:
            print(error)

    def _check_contacto(self, contactoNuevo: Contacto):
        try:
            # Checa en la lista de contactos si es que existe el nombre y sus telefonos
            for contacto in self.contactos:
                if contacto.nombre == contactoNuevo.nombre:
                    raise EsUnicoException
                # Checa cada uno de los telefonos si existen, en caso de que existan se manda una excepcion aunque no deberia ser necesario y solo ignorar
                for telefono_de in dict.keys(contacto.telefonos):
                    if contacto[telefono_de] == contactoNuevo[telefono_de]:
                        raise EsUnicoException
        except Exception as error:
            # Aqui deberia preguntar si intenta añadir el usuario actualizarlo para no volver a cargar los datos.
            print(error)


# PROGRAMA
agenda = Agenda()
opcion = 0
while True:
    print("1. Registrar contacto")
    print("2. Lista de Contactos")
    print("3. Buscar contacto")
    print("4. Salir")
    opcion = input(">")
    if opcion == "1":
        agenda.crearContacto("", {})
    elif opcion == "2":
        agenda.mostrarAgenda()
        pass
    elif opcion == "3":
        agenda.sub_menu()
        pass
    elif opcion == "4":
        break
    else:
        print("Opcion no valida")
