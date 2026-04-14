    
@extends('layouts.app')

@section('content')
<div class="auth-page">
    <a href="{{ route('catalogo') }}" class="back-link">
        <i class="fas fa-arrow-left"></i> Volver
    </a>

    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1 class="auth-logo">MACUIN</h1>
                <h2 class="auth-title">Iniciar Sesión</h2>
                <p class="auth-subtitle">Portal de Clientes</p>
            </div>

            @if($errors->any())
                <div style="background:#fee2e2;color:#991b1b;padding:.75rem;border-radius:.5rem;margin-bottom:1rem;font-size:.875rem">
                    {{ $errors->first() }}
                </div>
            @endif

            <form class="auth-form" method="POST" action="{{ route('login.post') }}">
                @csrf
                <div class="form-group">
                    <label class="form-label">Correo Electrónico</label>
                    <div class="input-wrapper">
                        <i class="fas fa-envelope input-icon"></i>
                        <input type="email" name="email" class="form-input"
                               placeholder="tu@email.com" value="{{ old('email') }}" required>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Contraseña</label>
                    <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" name="password" class="form-input"
                               placeholder="********" required>
                    </div>
                </div>

                <div class="form-options">
                    <a href="#" class="forgot-password">¿Olvidaste tu contraseña?</a>
                </div>

                <button type="submit" class="btn-auth">Iniciar Sesión</button>
            </form>

            <div class="auth-footer">
                <p>¿No tienes cuenta? <a href="{{ route('registro') }}" class="auth-link">Regístrate</a></p>
            </div>
        </div>
    </div>
</div>
@endsection
