<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ApiService
{
    protected string $baseUrl;

    public function __construct()
    {
        $this->baseUrl = env('API_URL', 'http://api:8000/v1');
    }

    // ── Autopartes ─────────────────────────────────────────────
    public function getAutopartes(): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/autopartes/");
            return $response->successful() ? $response->json() : [];
        } catch (\Exception $e) {
            Log::error("ApiService::getAutopartes - {$e->getMessage()}");
            return [];
        }
    }

    public function getAutoparte(int $id): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/autopartes/{$id}");
            return $response->successful() ? $response->json() : [];
        } catch (\Exception $e) {
            Log::error("ApiService::getAutoparte - {$e->getMessage()}");
            return [];
        }
    }

    // ── Usuarios ───────────────────────────────────────────────
    public function registrarUsuario(array $datos): array
    {
        try {
            $response = Http::timeout(5)->post("{$this->baseUrl}/usuarios/registro", $datos);
            if ($response->successful()) {
                return ['success' => true, 'data' => $response->json()];
            }
            $detalle = $response->json()['detail'] ?? 'Error al registrar';
            return ['success' => false, 'error' => $detalle];
        } catch (\Exception $e) {
            Log::error("ApiService::registrarUsuario - {$e->getMessage()}");
            return ['success' => false, 'error' => 'Error de conexión con la API'];
        }
    }

    public function getUsuario(int $id): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/usuarios/{$id}");
            return $response->successful() ? $response->json() : [];
        } catch (\Exception $e) {
            Log::error("ApiService::getUsuario - {$e->getMessage()}");
            return [];
        }
    }

    // ── Pedidos ────────────────────────────────────────────────
    public function crearPedido(array $datos): array
    {
        try {
            $response = Http::timeout(10)->post("{$this->baseUrl}/pedidos/", $datos);
            if ($response->successful()) {
                return ['success' => true, 'data' => $response->json()];
            }
            $detalle = $response->json()['detail'] ?? 'Error al crear pedido';
            return ['success' => false, 'error' => $detalle];
        } catch (\Exception $e) {
            Log::error("ApiService::crearPedido - {$e->getMessage()}");
            return ['success' => false, 'error' => 'Error de conexión con la API'];
        }
    }

    public function getPedidosUsuario(int $usuarioId): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/pedidos/usuario/{$usuarioId}");
            return $response->successful() ? $response->json() : [];
        } catch (\Exception $e) {
            Log::error("ApiService::getPedidosUsuario - {$e->getMessage()}");
            return [];
        }
    }

    public function getPedido(int $id): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/pedidos/{$id}");
            return $response->successful() ? $response->json() : [];
        } catch (\Exception $e) {
            Log::error("ApiService::getPedido - {$e->getMessage()}");
            return [];
        }
    }
}
