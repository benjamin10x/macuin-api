@extends('layouts.app')

@section('content')
<header class="header">
    <div class="header-container">
        <a href="{{ route('catalogo') }}" class="logo">MACUIN</a>
        <div class="header-right">
            <a href="{{ route('pedidos') }}" class="nav-link">Mis Pedidos</a>
            <a href="{{ route('carrito') }}" class="cart-link">
                
                <i class="fas fa-shopping-cart"></i>
                <span class="cart-count" id="cart-count">0</span>
            </a>
            @if(session('usuario'))
                <span style="color:#fff;font-size:.9rem">{{ session('usuario')['nombre'] }}</span>
                <form method="POST" action="{{ route('logout') }}" style="display:inline">
                    @csrf
                    <button type="submit" class="user-link" style="background:none;border:none;cursor:pointer">
                        <i class="fas fa-sign-out-alt"></i>
                    </button>
                </form>
            @else
                <a href="{{ route('login') }}" class="user-link">
                    <i class="fas fa-user-circle"></i>
                </a>
            @endif
        </div>
    </div>
</header>

<main class="main-content">
    <div class="container">
        @if(session('success'))
            <div class="alert-success-bar">{{ session('success') }}</div>
        @endif
        @if(session('error'))
            <div class="alert-error-bar">{{ session('error') }}</div>
        @endif

        <h1 class="page-title">Catálogo de Autopartes</h1>

        <div class="filters-container">
            <div class="filter-group">
                <label for="categoria-select">Categoría:</label>
                <select id="categoria-select" onchange="filtrarProductos()">
                    <option value="">Todas las categorías</option>
                    @php
                        $categorias = collect($autopartes)->pluck('categoria')->unique()->sort();
                    @endphp
                    @foreach($categorias as $categoria)
                        <option value="{{ strtolower($categoria) }}">{{ $categoria }}</option>
                    @endforeach
                </select>
            </div>
            <div class="filter-group">
                <label for="precio-min">Precio mínimo:</label>
                <input type="number" id="precio-min" placeholder="0" oninput="filtrarProductos()">
            </div>
            <div class="filter-group">
                <label for="precio-max">Precio máximo:</label>
                <input type="number" id="precio-max" placeholder="999999" oninput="filtrarProductos()">
            </div>
        </div>

        <div class="search-container">
            <i class="fas fa-search search-icon"></i>
            <input type="text" class="search-input" id="buscador"
                   placeholder="Buscar autopartes..." oninput="filtrarProductos()">
        </div>

        <div class="products-grid" id="products-grid">
            @forelse($autopartes as $autoparte)
            <div class="product-card" data-nombre="{{ strtolower($autoparte['nombre']) }}"
                 data-categoria="{{ strtolower($autoparte['categoria']) }}"
                 data-precio="{{ $autoparte['precio'] }}">
                <div class="product-image">
                    <i class="fas fa-cog"></i>
                </div>
                <div class="product-info">
                    <span class="product-category">{{ $autoparte['categoria'] }}</span>
                    <h3 class="product-name">{{ $autoparte['nombre'] }}</h3>
                    @if($autoparte['descripcion'])
                        <p style="font-size:.8rem;color:#6b7280;margin:.25rem 0">{{ $autoparte['descripcion'] }}</p>
                    @endif
                    <div class="product-footer">
                        <span class="product-price">${{ number_format($autoparte['precio'], 2) }}</span>
                        @if($autoparte['stock'] > 0)
                            <span class="product-stock available">
                                <i class="fas fa-check-circle"></i> {{ $autoparte['stock'] }} disponibles
                            </span>
                        @else
                            <span class="product-stock" style="color:#dc2626">
                                <i class="fas fa-times-circle"></i> Sin stock
                            </span>
                        @endif
                    </div>
                    @if($autoparte['stock'] > 0)
                        <button class="btn-add-cart"
                                onclick="agregarAlCarrito({{ $autoparte['id'] }}, '{{ $autoparte['nombre'] }}', {{ $autoparte['precio'] }})">
                            Agregar al Carrito
                        </button>
                    @else
                        <button class="btn-add-cart" disabled style="opacity:.5;cursor:not-allowed">
                            Sin stock
                        </button>
                    @endif
                </div>
            </div>
            @empty
            <div style="grid-column:1/-1;text-align:center;padding:3rem;color:#6b7280">
                <i class="fas fa-box-open" style="font-size:2rem;margin-bottom:1rem"></i>
                <p>No hay productos disponibles en este momento.</p>
            </div>
            @endforelse
        </div>
    </div>
</main>

<style>
.alert-success-bar{background:#d1fae5;color:#065f46;padding:.75rem 1rem;border-radius:.5rem;margin-bottom:1rem;}
.alert-error-bar{background:#fee2e2;color:#991b1b;padding:.75rem 1rem;border-radius:.5rem;margin-bottom:1rem;}
.filters-container { display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }
.filter-group { display: flex; flex-direction: column; }
.filter-group label { font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem; color: #374151; }
.filter-group select, .filter-group input { padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem; }
</style>

<script>
let carrito = JSON.parse(localStorage.getItem('macuin_carrito') || '[]');
actualizarContador();

function agregarAlCarrito(id, nombre, precio) {
    const idx = carrito.findIndex(i => i.autoparte_id === id);
    if (idx >= 0) {
        carrito[idx].cantidad++;
    } else {
        carrito.push({ autoparte_id: id, nombre, precio, cantidad: 1 });
    }
    localStorage.setItem('macuin_carrito', JSON.stringify(carrito));
    actualizarContador();
    mostrarToast(`"${nombre}" agregado al carrito`);
}

function actualizarContador() {
    const total = carrito.reduce((s, i) => s + i.cantidad, 0);
    document.getElementById('cart-count').textContent = total;
}

function filtrarProductos() {
    const q = document.getElementById('buscador').value.toLowerCase();
    const categoria = document.getElementById('categoria-select').value.toLowerCase();
    const precioMin = parseFloat(document.getElementById('precio-min').value) || 0;
    const precioMax = parseFloat(document.getElementById('precio-max').value) || Infinity;

    document.querySelectorAll('.product-card').forEach(card => {
        const nombre = card.dataset.nombre || '';
        const cat = card.dataset.categoria || '';
        const precio = parseFloat(card.dataset.precio) || 0;

        const matchesSearch = nombre.includes(q) || cat.includes(q);
        const matchesCategoria = !categoria || cat === categoria;
        const matchesPrecio = precio >= precioMin && precio <= precioMax;

        card.style.display = (matchesSearch && matchesCategoria && matchesPrecio) ? '' : 'none';
    });
}

function mostrarToast(msg) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;background:#1A1A2A;color:#fff;padding:.75rem 1.25rem;border-radius:.5rem;font-size:.875rem;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,.2)';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2500);
}
</script>
@endsection
