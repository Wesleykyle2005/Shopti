# Shopti

Shopti ofrece a los usuarios la posibilidad de buscar tiendas de pulperías a través de un mapa interactivo, lo que facilita la localización de establecimientos cercanos. Además, permite consultar el inventario disponible en cada tienda, ayudando a los consumidores a conocer la oferta de productos antes de realizar un pedido. Esta funcionalidad enriquece la experiencia del usuario al combinar la búsqueda geográfica con el acceso directo a la información actualizada del stock.

Por otro lado, Shopti permite a los pulperos administrar de forma integral sus pedidos e inventario, facilitando el registro detallado de transacciones y la gestión del stock. Además, incorpora herramientas de análisis que identifican los productos más vendidos, lo que ayuda a tomar decisiones informadas para optimizar las operaciones y aumentar la rentabilidad del negocio.

---

## Descripción del proyecto

El repositorio contiene una aplicación web de Django que permite:

- Mostrar y gestionar tiendas y sus ubicaciones en un mapa.
- Administrar productos y categorías, incluyendo filtrado y paginación.
- Gestionar un carrito de compras con funciones para agregar, actualizar y eliminar productos.
- Simular pedidos y generar mensajes para confirmar la orden de compra.

La aplicación está organizada en varios módulos que manejan diferentes aspectos del sistema.

---

## Estructura general

- **`Shopty/`**  
  Configuración base del proyecto Django (incluye `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).

- **`kernel/`**  
  Módulo principal que maneja la vista de inicio, la autenticación de usuarios y el layout general del sitio.

- **`stores/`**  
  Módulo para la gestión de tiendas. Incluye el modelo de tienda, integración con mapas (Leaflet.js) y la visualización de las ubicaciones.

- **`products/`**  
  Módulo para administrar productos y categorías. Permite listar productos, filtrar por tienda y categoría, y organizar la información con paginación.

- **`cart/`**  
  Módulo que gestiona el carrito de compras mediante la sesión. Permite agregar, actualizar y eliminar productos, y genera un mensaje para confirmar pedidos (por ejemplo, para envío a través de WhatsApp).

- **`db.sqlite3`**  
  Base de datos SQLite con la información generada por las migraciones.

---

## Detalle de módulos

### kernel

- **models.py**: Define el modelo de usuario extendiendo `AbstractUser`.
- **views.py**: Contiene la vista `home` que muestra la lista de tiendas.
- **static/kernel/js/script.js**: Gestiona la lógica del frontend, incluyendo el filtrado de productos y la visualización de detalles.
- **templates/kernel/layout.html**: Plantilla base que define la estructura principal del sitio.

### stores

- **models.py**: Define el modelo `Store` con atributos como nombre, descripción y ubicación.
- **static/stores/js/maps.js**: Configura un mapa usando Leaflet para mostrar las tiendas.
- **templates/stores/index.html**: Visualiza el listado de tiendas junto con el mapa.

### products

- **models.py**: Define los modelos `Product` y `Category`, relacionándolos con las tiendas.
- **views.py**:  
  - `products`: Lista los productos con paginación.  
  - `filter_products`: Aplica filtros por tienda y/o categoría.
- **templates/products/**:  
  - `products.html`: Página principal que muestra los productos.  
  - `product_list.html`: Subplantilla para la presentación de cada producto.

### cart

- **views.py**:  
  - `cart_detail`: Muestra el contenido del carrito.  
  - `cart_add`: Añade productos al carrito mediante AJAX o URL.  
  - `update_cart`: Actualiza la cantidad de productos.  
  - `cart_remove`: Elimina productos del carrito.  
  - `build_whatsapp_message`: Genera un mensaje de pedido.
- **templates/cart/detail.html**: Muestra los productos en el carrito y el botón para generar el pedido.

---

## Script adicional

- **fetch_insert.py**: Script para poblar la base de datos automáticamente desde una API externa, creando registros de tiendas y productos.

---

## Cómo ejecutar el proyecto

1. **Clonar o descargar** este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/shopti.git
   cd shopti
   ```

2. **Instalar dependencias**:
   ```bash
   pip install django requests
   ```

3. **Aplicar migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

---