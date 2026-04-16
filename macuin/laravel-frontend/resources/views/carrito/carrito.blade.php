@extends('layouts.app')
@section('content')
<div class="cart-page">
    <header class="header">
        <div class="header-container">
            <div class="header-left">
                <a href="{{ route('catalogo') }}" class="back-link-header">
                    <i class="fas fa-arrow-left"></i> Volver al Catálogo
                </a>
                <a href="{{ route('index') }}" class="logo">MACUIN</a>
            </div>
            <div class="header-right">
                <a href="{{ route('pedidos') }}" class="nav-link">Mis Pedidos</a>
            </div>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <div class="page-header">
                <h1 class="page-title">Crear Pedido</h1>
                <p class="page-subtitle">Revisa y confirma tu pedido</p>
            </div>

            @if(!$usuario)
                <div style="background:#fff3cd;color:#856404;padding:1rem;border-radius:.5rem;margin-bottom:1rem">
                    <i class="fas fa-info-circle"></i>
                    Debes <a href="{{ route('registro') }}">registrarte</a> o
                    <a href="{{ route('login') }}">iniciar sesión</a> para confirmar un pedido.
                </div>
            @endif

            <div class="cart-layout">
                <div class="cart-items-section" id="cart-items">
                    <p style="color:#6b7280;text-align:center;padding:2rem" id="empty-msg">
                        Tu carrito está vacío. <a href="{{ route('catalogo') }}">Ver catálogo</a>
                    </p>
                </div>

                <div class="cart-summary-section">
                    <div class="cart-summary-card">
                        <h3 class="summary-title">Resumen del Pedido</h3>
                        <div class="summary-row">
                            <span>Subtotal</span>
                            <span id="subtotal">$0.00</span>
                        </div>
                        <div class="summary-total">
                            <span>Total</span>
                            <span id="total">$0.00</span>
                        </div>

                        @if($usuario)
                        <form id="form-pedido" method="POST" action="{{ route('pedidos.crear') }}">
                            @csrf
                            <div id="hidden-inputs"></div>
                            <button type="submit" class="btn-checkout" id="btn-confirmar" disabled>
                                Confirmar Pedido
                            </button>
                        </form>
                        @else
                        <a href="{{ route('registro') }}" class="btn-checkout" style="text-align:center;display:block">
                            Regístrate para comprar
                        </a>
                        @endif
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>

<script>
let carrito = JSON.parse(localStorage.getItem('macuin_carrito') || '[]');
renderCarrito();

function renderCarrito() {
    const container  = document.getElementById('cart-items');
    const emptyMsg   = document.getElementById('empty-msg');
    const btnConfirm = document.getElementById('btn-confirmar');
    const hiddenDiv  = document.getElementById('hidden-inputs');

    if (carrito.length === 0) {
        if (emptyMsg) emptyMsg.style.display = 'block';
        if (btnConfirm) btnConfirm.disabled = true;
        return;
    }

    if (emptyMsg) emptyMsg.style.display = 'none';
    container.innerHTML = '';

    let total = 0;
    carrito.forEach((item, idx) => {
        total += item.precio * item.cantidad;
        container.insertAdjacentHTML('beforeend', `
            <div class="cart-item">
                <div class="cart-item-info">
                    <h3 class="cart-item-name">${item.nombre}</h3>
                    <span class="cart-item-price">$${item.precio.toFixed(2)}</span>
                </div>
                <div class="cart-item-controls">
                    <button class="qty-btn minus" onclick="cambiarCantidad(${idx}, -1)">
                        <i class="fas fa-minus"></i>
                    </button>
                    <span class="qty-value">${item.cantidad}</span>
                    <button class="qty-btn plus" onclick="cambiarCantidad(${idx}, 1)">
                        <i class="fas fa-plus"></i>
                    </button>
                    <span class="cart-item-total">$${(item.precio * item.cantidad).toFixed(2)}</span>
                    <button class="btn-remove" onclick="eliminarItem(${idx})">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>`);
    });

    document.getElementById('subtotal').textContent = `$${total.toFixed(2)}`;
    document.getElementById('total').textContent    = `$${total.toFixed(2)}`;

    if (btnConfirm) btnConfirm.disabled = false;

    // Llenar inputs ocultos para el POST
    if (hiddenDiv) {
        hiddenDiv.innerHTML = '';
        carrito.forEach((item, idx) => {
            hiddenDiv.insertAdjacentHTML('beforeend', `
                <input type="hidden" name="detalles[${idx}][autoparte_id]" value="${item.autoparte_id}">
                <input type="hidden" name="detalles[${idx}][cantidad]" value="${item.cantidad}">
            `);
        });
    }
}

function cambiarCantidad(idx, delta) {
    carrito[idx].cantidad = Math.max(1, carrito[idx].cantidad + delta);
    localStorage.setItem('macuin_carrito', JSON.stringify(carrito));
    renderCarrito();
}

function eliminarItem(idx) {
    carrito.splice(idx, 1);
    localStorage.setItem('macuin_carrito', JSON.stringify(carrito));
    renderCarrito();
}

// Limpiar carrito al confirmar pedido
const form = document.getElementById('form-pedido');
if (form) {
    form.addEventListener('submit', () => {
        localStorage.removeItem('macuin_carrito');
    });
}
</script>
@endsection
