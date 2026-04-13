<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\CatalogoController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PedidoController;

Route::get('/', function () {
    return view('home.index');
})->name('index');

Route::get('/catalogo', [CatalogoController::class, 'index'])->name('catalogo');

Route::get('/registro',  [AuthController::class, 'showRegistro'])->name('registro');
Route::post('/registro', [AuthController::class, 'registro'])->name('registro.post');

Route::get('/login',  [AuthController::class, 'showLogin'])->name('login');
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

Route::get('/pedidos',     [PedidoController::class, 'index'])->name('pedidos');
Route::post('/pedidos',    [PedidoController::class, 'crear'])->name('pedidos.crear');
Route::get('/pedidos/{id}',[PedidoController::class, 'detalle'])->name('pedido-detalle');

Route::get('/carrito', function () {
    $usuario = session('usuario');
    return view('carrito.carrito', compact('usuario'));
})->name('carrito');
