@extends('layouts.app')

@section('content')
<div class="home-page">
    <!-- Header -->
    <header class="header header-transparent">
        <div class="header-container">
            <a href="{{ route('index') }}" class="logo">MACUIN</a>
            <div class="header-right">
                <a href="{{ route('pedidos') }}" class="nav-link">Mis Pedidos</a>
                <a href="{{ route('carrito') }}" class="cart-link">
                    <i class="fas fa-shopping-cart"></i>
                    <span class="cart-count">2</span>
                </a>
                <a href="{{ route('login') }}" class="btn-header-login">Iniciar Sesión</a>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <span class="hero-badge">
                <i class="fas fa-truck"></i> Envío gratis en compras mayores a $1,000
            </span>
            <h1 class="hero-title">Autopartes de calidad<br>para tu vehículo</h1>
            <p class="hero-subtitle">Encuentra todo lo que necesitas para mantener tu auto en perfectas condiciones. Más de 5,000 productos disponibles con entrega rápida.</p>
            <div class="hero-buttons">
                <a href="{{ route('catalogo') }}" class="btn-primary">
                    <i class="fas fa-search"></i> Explorar Catálogo
                </a>
                <a href="{{ route('registro') }}" class="btn-secondary">
                    Crear Cuenta
                </a>
            </div>
            <div class="hero-stats">
                <div class="stat-item">
                    <span class="stat-number">5,000+</span>
                    <span class="stat-label">Productos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">10,000+</span>
                    <span class="stat-label">Clientes</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">24h</span>
                    <span class="stat-label">Entrega</span>
                </div>
            </div>
        </div>
        <div class="hero-visual">
            <div class="hero-icon">
                <i class="fas fa-car"></i>
            </div>
            <div class="floating-card card-1">
                <i class="fas fa-check-circle"></i>
                <span>Garantía de calidad</span>
            </div>
            <div class="floating-card card-2">
                <i class="fas fa-shield-alt"></i>
                <span>Pagos seguros</span>
            </div>
        </div>
    </section>

    <!-- Categories Section -->
    <section class="categories-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Categorías Populares</h2>
                <p class="section-subtitle">Encuentra las mejores autopartes organizadas por categoría</p>
            </div>
            <div class="categories-grid">
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-filter"></i>
                    </div>
                    <h3 class="category-name">Filtros</h3>
                    <p class="category-count">120 productos</p>
                </a>
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-circle"></i>
                    </div>
                    <h3 class="category-name">Frenos</h3>
                    <p class="category-count">85 productos</p>
                </a>
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3 class="category-name">Eléctrico</h3>
                    <p class="category-count">200 productos</p>
                </a>
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-oil-can"></i>
                    </div>
                    <h3 class="category-name">Lubricantes</h3>
                    <p class="category-count">45 productos</p>
                </a>
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-compress-arrows-alt"></i>
                    </div>
                    <h3 class="category-name">Suspensión</h3>
                    <p class="category-count">90 productos</p>
                </a>
                <a href="{{ route('catalogo') }}" class="category-card">
                    <div class="category-icon">
                        <i class="fas fa-fire"></i>
                    </div>
                    <h3 class="category-name">Encendido</h3>
                    <p class="category-count">65 productos</p>
                </a>
            </div>
        </div>
    </section>

    <!-- Featured Products Section -->
    <section class="featured-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Productos Destacados</h2>
                <a href="{{ route('catalogo') }}" class="section-link">Ver todos <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="featured-grid">
                <div class="featured-card">
                    <div class="featured-badge">Más Vendido</div>
                    <div class="featured-image">
                        <i class="fas fa-cube"></i>
                    </div>
                    <div class="featured-info">
                        <span class="featured-category">Filtros</span>
                        <h3 class="featured-name">Filtro de Aceite Premium</h3>
                        <div class="featured-footer">
                            <span class="featured-price">$15</span>
                            <a href="{{ route('catalogo') }}" class="btn-view">Ver Producto</a>
                        </div>
                    </div>
                </div>
                <div class="featured-card">
                    <div class="featured-badge">Oferta</div>
                    <div class="featured-image">
                        <i class="fas fa-cube"></i>
                    </div>
                    <div class="featured-info">
                        <span class="featured-category">Frenos</span>
                        <h3 class="featured-name">Pastillas de Freno Cerámicas</h3>
                        <div class="featured-footer">
                            <span class="featured-price">$89</span>
                            <a href="{{ route('catalogo') }}" class="btn-view">Ver Producto</a>
                        </div>
                    </div>
                </div>
                <div class="featured-card">
                    <div class="featured-image">
                        <i class="fas fa-cube"></i>
                    </div>
                    <div class="featured-info">
                        <span class="featured-category">Eléctrico</span>
                        <h3 class="featured-name">Batería 12V 75Ah</h3>
                        <div class="featured-footer">
                            <span class="featured-price">$1,299</span>
                            <a href="{{ route('catalogo') }}" class="btn-view">Ver Producto</a>
                        </div>
                    </div>
                </div>
                <div class="featured-card">
                    <div class="featured-image">
                        <i class="fas fa-cube"></i>
                    </div>
                    <div class="featured-info">
                        <span class="featured-category">Lubricantes</span>
                        <h3 class="featured-name">Aceite Sintético 5W-30</h3>
                        <div class="featured-footer">
                            <span class="featured-price">$45</span>
                            <a href="{{ route('catalogo') }}" class="btn-view">Ver Producto</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section">
        <div class="container">
            <div class="benefits-grid">
                <div class="benefit-item">
                    <div class="benefit-icon">
                        <i class="fas fa-shipping-fast"></i>
                    </div>
                    <h3 class="benefit-title">Envío Rápido</h3>
                    <p class="benefit-text">Entrega en 24-48 horas en toda la ciudad</p>
                </div>
                <div class="benefit-item">
                    <div class="benefit-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3 class="benefit-title">Garantía Total</h3>
                    <p class="benefit-text">Todos nuestros productos tienen garantía</p>
                </div>
                <div class="benefit-item">
                    <div class="benefit-icon">
                        <i class="fas fa-headset"></i>
                    </div>
                    <h3 class="benefit-title">Soporte 24/7</h3>
                    <p class="benefit-text">Atención al cliente todo el día</p>
                </div>
                <div class="benefit-item">
                    <div class="benefit-icon">
                        <i class="fas fa-undo"></i>
                    </div>
                    <h3 class="benefit-title">Devoluciones</h3>
                    <p class="benefit-text">30 días para devolver tu compra</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="cta-content">
            <h2 class="cta-title">¿Listo para encontrar lo que necesitas?</h2>
            <p class="cta-subtitle">Regístrate ahora y obtén un 10% de descuento en tu primera compra</p>
            <a href="registro.html" class="btn-cta">Crear Cuenta Gratis</a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="{{ route('index') }}" class="footer-logo">MACUIN</a>
                    <p class="footer-text">Tu tienda de confianza para autopartes. Calidad garantizada y entrega rápida.</p>
                    <div class="footer-social">
                        <a href="#"><i class="fab fa-facebook"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                    </div>
                </div>
                <div class="footer-links">
                    <h4 class="footer-title">Enlaces Rápidos</h4>
                    <ul>
                        <li><a href="{{ route('catalogo') }}">Catálogo</a></li>
                        <li><a href="{{ route('pedidos') }}">Mis Pedidos</a></li>
                        <li><a href="{{ route('login') }}">Iniciar Sesión</a></li>
                        <li><a href="{{ route('registro') }}">Crear Cuenta</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4 class="footer-title">Categorías</h4>
                    <ul>
                        <li><a href="{{ route('catalogo') }}">Filtros</a></li>
                        <li><a href="{{ route('catalogo') }}">Frenos</a></li>
                        <li><a href="{{ route('catalogo') }}">Eléctrico</a></li>
                        <li><a href="{{ route('catalogo') }}">Lubricantes</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4 class="footer-title">Contacto</h4>
                    <p><i class="fas fa-envelope"></i> macuin@macuin.com</p>
                    <p><i class="fas fa-phone"></i> (555) 123-4567</p>
                    <p><i class="fas fa-map-marker-alt"></i> Ciudad de México</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 MACUIN. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
</div>
@endsection