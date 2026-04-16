<?php

namespace App\Http\Controllers;

use App\Services\ApiService;
use Illuminate\Http\Request;

class AuthController extends Controller
{
    protected ApiService $api;

    public function __construct(ApiService $api)
    {
        $this->api = $api;
    }

    public function showRegistro()
    {
        return view('auth.registro');
    }

    public function registro(Request $request)
    {
        $request->validate([
            'nombre'   => 'required|min:3|max:100',
            'email'    => 'required|email',
            'telefono' => 'nullable|max:20',
            'password' => 'required|min:6|confirmed',
        ], [
            'nombre.required'    => 'El nombre es obligatorio',
            'email.required'     => 'El correo es obligatorio',
            'email.email'        => 'El correo no es válido',
            'password.required'  => 'La contraseña es obligatoria',
            'password.min'       => 'La contraseña debe tener al menos 6 caracteres',
            'password.confirmed' => 'Las contraseñas no coinciden',
        ]);

        $resultado = $this->api->registrarUsuario([
            'nombre'   => $request->nombre,
            'email'    => $request->email,
            'telefono' => $request->telefono,
            'password' => $request->password,
        ]);

        if ($resultado['success']) {
            // Guardar usuario en sesión (sin JWT por ahora)
            session(['usuario' => $resultado['data']]);
            return redirect()->route('catalogo')
                ->with('success', '¡Cuenta creada correctamente! Bienvenido a MACUIN.');
        }

        return back()->withErrors(['email' => $resultado['error']])->withInput();
    }

    public function showLogin()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required|min:6',
        ], [
            'email.required' => 'El correo es obligatorio',
            'email.email' => 'El correo no es válido',
            'password.required' => 'La contraseña es obligatoria',
            'password.min' => 'La contraseña debe tener al menos 6 caracteres',
        ]);

        $resultado = $this->api->iniciarSesion([
            'email' => $request->email,
            'password' => $request->password,
        ]);

        if ($resultado['success']) {
            $request->session()->regenerate();
            session(['usuario' => $resultado['data']]);

            return redirect()->route('catalogo')
                ->with('success', '¡Bienvenido de nuevo a MACUIN!');
        }

        return back()
            ->withErrors(['login' => $resultado['error']])
            ->withInput($request->only('email'));
    }

    public function logout(Request $request)
    {
        $request->session()->forget('usuario');
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect()->route('index');
    }
}
