@extends('layouts.app')
@section('content')
<div class="orders-page">
    <header class="header">
        <div class="header-container">
            <div class="header-left">
                <a href="{{ route('pedidos') }}" class="back-link-header">
                    <i class="fas fa-arrow-left"></i> Mis Pedidos
                </a>
                <a href="{{ route('catalogo') }}" class="logo">MACUIN</a>
            </div>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            @if(!$pedido)
                <p>Pedido no encontrado.</p>
            @else
                <div class="page-header">
                    <h1 class="page-title">
                        Pedido #{{ str_pad($pedido['id'], 4, '0', STR_PAD_LEFT) }}
                    </h1>
                    <span class="order-status status-{{ $pedido['estado'] }}">
                        {{ ucfirst($pedido['estado']) }}
                    </span>
                </div>

                <div style="background:#fff;border:1px solid #e5e7eb;border-radius:.75rem;padding:1.5rem;margin-bottom:1.5rem">
                    <h3 style="margin-bottom:1rem;font-size:1rem;color:#374151">Productos</h3>
                    @foreach($pedido['detalles'] as $detalle)
                    <div style="display:flex;justify-content:space-between;padding:.6rem 0;border-bottom:1px solid #f3f4f6">
                        <span>{{ $detalle['autoparte']['nombre'] ?? 'Autoparte #'.$detalle['autoparte_id'] }}</span>
                        <span>
                            {{ $detalle['cantidad'] }} × ${{ number_format($detalle['precio_unit'], 2) }}
                            = <strong>${{ number_format($detalle['subtotal'], 2) }}</strong>
                        </span>
                    </div>
                    @endforeach
                    <div style="display:flex;justify-content:flex-end;margin-top:1rem;font-size:1.1rem;font-weight:700">
                        Total: ${{ number_format($pedido['total'], 2) }}
                    </div>
                </div>

                <div style="color:#6b7280;font-size:.875rem">
                    Fecha: {{ \Carbon\Carbon::parse($pedido['fecha'])->format('d/m/Y H:i') }}
                </div>
            @endif
        </div>
    </main>
</div>
@endsection
