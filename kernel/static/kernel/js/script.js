// Ejecuta al cargar el DOM por completo
document.addEventListener('DOMContentLoaded', function() {
    var categorySelect = document.getElementById('category-select');

    // Si existe el selector de categorías, lo vincula al envío automático del formulario
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            document.getElementById('filter-form').submit();
        });
    }

    // Adjunta eventos a botones "ver más"
    attachViewMoreEvents();
});

// Función para vincular eventos al botón "ver más"
function attachViewMoreEvents() {
    document.querySelectorAll('.view-more').forEach(function(button) {
        button.addEventListener('click', function() {
            // Extrae atributos de datos del botón seleccionado
            var productId = this.getAttribute('data-id');
            var productName = this.getAttribute('data-name');
            var productDescription = this.getAttribute('data-description');
            var productPrice = this.getAttribute('data-price');
            var productImage = this.getAttribute('data-image');
            var available_units = this.getAttribute('data-available-units');

            // Llena el contenido del modal con los datos del producto
            document.getElementById('productModalLabel').innerText = productName;
            document.getElementById('productModalDescription').innerText = productDescription;
            document.getElementById('productModalPrice').innerText = productPrice;
            document.getElementById('productModalImage').src = productImage;
            document.getElementById('productModalImage').alt = productName;
            document.getElementById('modalProductId').value = productId;
            document.getElementById('modalProductQuantity').value = 1; 
            document.getElementById('modalProductQuantity').max = available_units;
            document.getElementById('available_units').innerText = available_units;
        });
    });

    // Agrega producto al carrito desde el modal
    document.getElementById('modalAddToCartButton').addEventListener('click', function() {
        var productId = document.getElementById('modalProductId').value;
        var quantity = parseInt(document.getElementById('modalProductQuantity').value, 10);
        var max = parseInt(document.getElementById('modalProductQuantity').max, 10);

        // Validación: cantidad debe ser un entero positivo
        if (!Number.isInteger(quantity) || quantity <= 0) {
            showAlert('La cantidad debe ser un número entero positivo', 'warning');
            return;
        }

        // Validación: no exceder unidades disponibles
        if (quantity > max) {
            showAlert('La cantidad debe ser menor o igual a ' + max, 'warning');
            return;
        }

        // Solicitud AJAX para agregar producto
        var url = '/cart/add/' + productId + '?quantity=' + encodeURIComponent(quantity);
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                document.getElementById('cart-count').innerText = response.cart_count;
                showAlert('Producto añadido al carrito. <a href="' + cartDetailUrl + '">Ver carrito</a>', 'success');
            }
        };
        xhr.send();
    });
}

// Muestra alertas personalizadas en pantalla
function showAlert(message, type) {
    let iconId = "#info-fill";
    if (type === 'warning' || type === 'danger') {
        iconId = "#exclamation-triangle-fill";
    }

    var alertContainer = document.getElementById('alert-container');

    // Crea y configura estructura de la alerta
    var alert = document.createElement('div');
    alert.className = `alert alert-dark alert-${type} alert-dismissible fade show d-flex align-items-center`;
    alert.role = 'alert';
    alert.innerHTML = `
        <svg class="bi flex-shrink-0 me-2 alert-icon" role="img" aria-label="${type}"><use xlink:href="${iconId}"/></svg>
        <div>${message}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alert);

    // Cierra automáticamente la alerta luego de 1.5 segundos
    setTimeout(function() {
        var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
        alertInstance.close();
    }, 1500);
}
