# Botiga API

Botiga API es un servicio web basado en FastAPI diseñado para gestionar productos en una tienda online. Este proyecto proporciona una serie de endpoints para crear, leer, actualizar y eliminar productos, así como para cargar productos desde un archivo CSV a la base de datos.

## Características

![all_endpoints](/images/all_endpoints.png)

### Leer Todos los Productos - Get /product/
Devuelve una lista de todos los productos disponibles en la base de datos. Este endpoint facilita la recuperación de información detallada de cada producto almacenado.

![get_products](/images/get_products.png)

### Leer un Producto por ID - Get /product/{id}
Devuelve los detalles de un producto específico utilizando su ID. Este endpoint es útil para obtener información detallada de un producto particular.

![get_product_id](/images/get_product_id.png)

### Crear un Producto Individual - Post /create/ 
Permite la creación de un nuevo producto en la base de datos. Los detalles necesarios incluyen:
**Nombre**
**Descripción**
**Compañía**
**Precio**
**Unidades**
**ID de la subcategoría**

![create_product](/images/create_product.png)

### Crear Múltiples Productos - Post /creates/
Permite la creación de varios productos de una sola vez mediante el envío de una lista de productos. Cada producto debe contener los mismos detalles que se requieren para la creación individual.

![create_products](/images/create_products.png)

### Actualizar el Nombre de un Producto - Put /product/{id}
Permite actualizar el nombre de un producto existente en la base de datos utilizando su ID. Este endpoint facilita mantener actualizada la información del producto.

![modify_product](/images/modify_product.png)

### Eliminar un Producto por ID - Delete /product/{id}
Permite eliminar un producto específico de la base de datos utilizando su ID. Es útil para gestionar el inventario y remover productos que ya no están disponibles.

![delete_product](/images/delete_product.png)

### Obtener Productos con Detalles Específicos - Get /productAll/
Devuelve una lista de productos con detalles adicionales incluyendo:
**Nombre de la categoría**
**Nombre de la subcategoría**
**Nombre del producto**
**Marca del producto**
**Precio**

![get_products_details](/images/get_products_details.png)

### Cargar Productos desde un Archivo CSV - Post /loadProducts/
Permite la carga masiva de productos desde un archivo CSV. Este proceso implica:
1. **Leer el archivo CSV**: Se lee el contenido del archivo CSV proporcionado.
2. **Procesar los datos**: Se procesan los datos del CSV, que incluyen categorías, subcategorías y productos.
3. **Insertar/Actualizar en la base de datos**: Los datos procesados se insertan o actualizan en la base de datos según corresponda.

![load_products](/images/load_products.png)

## ¿Cómo Funciona?

### Conexión a la Base de Datos
El proyecto utiliza un manejador de base de datos (botiga_db) que se encarga de establecer la conexión con la base de datos MySQL utilizando los parámetros de configuración proporcionados en un archivo config.json.

### Endpoints CRUD
Los endpoints CRUD (Crear, Leer, Actualizar, Eliminar) interactúan con la base de datos a través del manejador botiga_db. Cada operación realiza consultas SQL específicas para manipular los datos de los productos.

### Carga de CSV
El manejador botiga_db también incluye funcionalidades para cargar datos desde un archivo CSV. Este proceso implica leer el archivo, procesar cada registro y actualizar o insertar los datos correspondientes en las tablas de categorías, subcategorías y productos.

### Manejo de Excepciones
Cada endpoint maneja posibles excepciones y errores, retornando mensajes claros sobre el estado de las operaciones (éxito o error), lo que facilita la depuración y el uso de la API.