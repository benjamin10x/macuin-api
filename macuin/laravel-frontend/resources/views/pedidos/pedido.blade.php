@extends('layouts.app')
@section('content')
<div class="orders-page">
    <header class="header">
        <div class="header-container">
            <div class="header-left">
                <a href="{{ route('catalogo') }}" class="back-link-header">
                    <i class="fas fa-arrow-left"></i> Volver al Catálogo
                </a>
                <a href="{{ route('catalogo') }}" class="logo">MACUIN</a>
            </div>
            <div class="header-right">
                <a href="{{ route('pedidos') }}" class="nav-link active">Mis Pedidos</a>
                <a href="{{ route('carrito') }}" class="cart-link">
                    <i class="fas fa-shopping-cart"></i>
                </a>
            </div>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            @if(session('success'))
                <div style="background:#d1fae5;color:#065f46;padding:.75rem;border-radius:.5rem;margin-bottom:1rem">
                    {{ session('success') }}
                </div>
            @endif

            <div class="page-header">
                <h1 class="page-title">Historial de Pedidos</h1>
                <p class="page-subtitle">Consulta el estado de tus pedidos</p>
            </div>

            @if(!$usuario)
                <div style="text-align:center;padding:3rem;color:#6b7280">
                    <i class="fas fa-user-lock" style="font-size:2.5rem;margin-bottom:1rem"></i>
                    <p>Debes <a href="{{ route('login') }}" style="color:#2E75B6">iniciar sesión</a>
                       o <a href="{{ route('registro') }}" style="color:#2E75B6">registrarte</a>
                       para ver tus pedidos.</p>
                </div>
            @elseif(count($pedidos) === 0)
                <div style="text-align:center;padding:3rem;color:#6b7280">
                    <i class="fas fa-box-open" style="font-size:2.5rem;margin-bottom:1rem"></i>
                    <p>Aún no tienes pedidos. <a href="{{ route('catalogo') }}" style="color:#2E75B6">Ver catálogo</a></p>
                </div>
            @else
                <div class="orders-list">
                    @foreach($pedidos as $pedido)
                    <a href="{{ route('pedido-detalle', $pedido['id']) }}" class="order-card">
                        <div class="order-icon"><i class="fas fa-cube"></i></div>
                        <div class="order-info">
                            <h3 class="order-number">ORD-{{ str_pad($pedido['id'], 4, '0', STR_PAD_LEFT) }}</h3>
                            <p class="order-date">
                                {{ \Carbon\Carbon::parse($pedido['fecha'])->format('d \d\e F \d\e Y') }}
                                • {{ count($pedido['detalles']) }} artículo(s)
                            </p>
                        </div>
                        <div class="order-right">
                            <span class="order-price">${{ number_format($pedido['total'], 2) }}</span>
                            <span class="order-status status-{{ $pedido['estado'] }}">
                                {{ ucfirst($pedido['estado']) }}
                            </span>
                        </div>
                        <i class="fas fa-chevron-right order-arrow"></i>
                    </a>
                    @endforeach
                </div>
            @endif
        </div>
    </main>
</div>
@endsection
