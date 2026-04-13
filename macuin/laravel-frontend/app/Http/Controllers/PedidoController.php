<?php

namespace App\Http\Controllers;

use App\Services\ApiService;
use Illuminate\Http\Request;

class PedidoController extends Controller
{
    protected ApiService $api;

    public function __construct(ApiService $api)
    {
        $this->api = $api;
    }

    public function index()
    {
        $usuario = session('usuario');
        $pedidos = [];

        if ($usuario) {
            $pedidos = $this->api->getPedidosUsuario($usuario['id']);
        }

        return view('pedidos.pedido', compact('pedidos', 'usuario'));
    }

    public function detalle(int $id)
    {
        $pedido = $this->api->getPedido($id);
        return view('pedidos.pedido-detalle', compact('pedido'));
    }

    public function crear(Request $request)
    {
        $usuario = session('usuario');
        if (!$usuario) {
            return redirect()->route('login')
                ->with('error', 'Debes iniciar sesión para hacer un pedido');
        }

        $request->validate([
            'detalles'              => 'required|array|min:1',
            'detalles.*.autoparte_id' => 'required|integer',
            'detalles.*.cantidad'   => 'required|integer|min:1',
        ]);

        $resultado = $this->api->crearPedido([
            'usuario_id' => $usuario['id'],
            'detalles'   => $request->detalles,
        ]);

        if ($resultado['success']) {
            return redirect()->route('pedidos')
                ->with('success', 'Pedido creado correctamente. Folio: #' . $resultado['data']['id']);
        }

        return back()->with('error', $resultado['error']);
    }
}
