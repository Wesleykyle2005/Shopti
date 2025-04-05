from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from urllib.parse import quote
from django.contrib import messages

# Vista principal del carrito que muestra productos, cantidades y total
# Se limpia el carrito de productos inválidos

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_products = []
    total_price = 0
    final_cart = {}

    for prod_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(id=prod_id_str)
            item_total = product.price * quantity
            total_price += item_total
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
            final_cart[prod_id_str] = quantity
        except Product.DoesNotExist:
            pass  # Se omite el producto si fue eliminado

    request.session['cart'] = final_cart

    return render(request, 'cart/detail.html', {
        'cart_products': cart_products,
        'total_price': total_price
    })


# Actualiza la cantidad de un producto en el carrito, respetando el stock disponible

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if prod_id_str in cart:
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.available_units:
            quantity = product.available_units
        cart[prod_id_str] = max(quantity, 1)

    request.session['cart'] = cart
    return redirect('cart_detail')


# Añade un producto al carrito vía GET; actualiza la cantidad si ya existe
# Usa AJAX para actualizar dinámicamente el contador

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get('quantity', 1))

    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)

    if prod_id_str in cart:
        new_quantity = cart[prod_id_str] + quantity
        cart[prod_id_str] = new_quantity if new_quantity <= product.available_units else product.available_units
    else:
        cart[prod_id_str] = quantity if quantity <= product.available_units else product.available_units

    product.number_of_units_added_to_carts += 1
    product.save()

    request.session['cart'] = cart

    cart_count = len(cart)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': cart_count})

    return redirect('products_all')


# Elimina un producto del carrito
# Soporta eliminación vía AJAX para actualizar contador sin recargar página

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)

    if prod_id_str in cart:
        del cart[prod_id_str]
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = len(cart)
        return JsonResponse({'cart_count': cart_count})

    return redirect('cart_detail')


# Flag para habilitar o deshabilitar generación de mensajes de WhatsApp
WHATSAPP_ENABLED = False

# Construye un mensaje preformateado de WhatsApp con los productos del carrito
# Redirige al API de WhatsApp con el mensaje codificado por URL

def build_whatsapp_message(request):
    if not WHATSAPP_ENABLED:
        messages.warning(request, "La función de envío por WhatsApp está deshabilitada en este momento.")
        return redirect('cart_detail')

    cart = request.session.get('cart', {})
    cart_products = []
    total_price = 0
    store_name = "Mi Tienda"

    for prod_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id_str)
        item_total = product.price * quantity
        total_price += item_total
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    message_body = (
        f"¡Hola {store_name}! 👋\n"
        "Quiero realizar el siguiente pedido:\n\n"
        "📋 *Detalles del pedido:*\n"
    )

    for i, item in enumerate(cart_products, 1):
        message_body += (
            f"\n{i}. *{item['product'].name}*\n"
            f"   ▸ Cantidad: {item['quantity']} "
            f"{'unidad' if item['quantity'] == 1 else 'unidades'}\n"
            f"   ▸ Precio unitario: C${item['product'].price:,.2f}\n"
            f"   ▸ Subtotal: C${item['item_total']:,.2f}\n"
        )

    message_body += (
        "\n--------------------------------\n"
        f"💵 *Total del pedido: C${total_price:,.2f}*\n\n"
        "📌 *Mis datos de contacto:*\n"
        "   ▸ Nombre: [Tu nombre completo]\n"
        "   ▸ Dirección de envío: [Dirección detallada]\n"
        "   ▸ Teléfono: [Número de contacto]\n"
        "   ▸ Método de pago preferido: [Efectivo/Tarjeta/Transferencia]\n\n"
        "Por favor confirmen disponibilidad y envíen detalles para finalizar la compra. "
        "¡Gracias! 😊\n"
        f"#PedidoOnline{store_name.replace(' ', '')}"
    )

    encoded_message = quote(message_body)
    whatsapp_url = f"https://api.whatsapp.com/send?phone=+50582529355&text={encoded_message}"

    return redirect(whatsapp_url)
