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
                <h2 class="auth-title">Crear Cuenta</h2>
                <p class="auth-subtitle">Registro de nuevo cliente</p>
            </div>

            @if($errors->any())
                <div style="background:#fee2e2;color:#991b1b;padding:.75rem;border-radius:.5rem;margin-bottom:1rem;font-size:.875rem">
                    {{ $errors->first() }}
                </div>
            @endif

            <form class="auth-form" method="POST" action="{{ route('registro.post') }}">
                @csrf
                <div class="form-group">
                    <label class="form-label">Nombre Completo</label>
                    <div class="input-wrapper">
                        <i class="fas fa-user input-icon"></i>
                        <input type="text" name="nombre" class="form-input"
                               placeholder="Juan Pérez" value="{{ old('nombre') }}" required>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Correo Electrónico</label>
                    <div class="input-wrapper">
                        <i class="fas fa-envelope input-icon"></i>
                        <input type="email" name="email" class="form-input"
                               placeholder="tu@email.com" value="{{ old('email') }}" required>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Teléfono (opcional)</label>
                    <div class="input-wrapper">
                        <i class="fas fa-phone input-icon"></i>
                        <input type="tel" name="telefono" class="form-input"
                               placeholder="4461234567" value="{{ old('telefono') }}">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Contraseña</label>
                    <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" name="password" class="form-input"
                               placeholder="Mínimo 6 caracteres" required>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Confirmar Contraseña</label>
                    <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" name="password_confirmation" class="form-input"
                               placeholder="Repite tu contraseña" required>
                    </div>
                </div>
                <button type="submit" class="btn-auth">Registrarse</button>
            </form>

            <div class="auth-footer">
                <p>¿Ya tienes cuenta? <a href="{{ route('login') }}" class="auth-link">Inicia sesión</a></p>
            </div>
        </div>
    </div>
</div>
@endsection
