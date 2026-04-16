<?php

namespace App\Services;

use Illuminate\Http\Client\Response;
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
            return ['success' => false, 'error' => $this->extractError($response, 'Error al registrar')];
        } catch (\Exception $e) {
            Log::error("ApiService::registrarUsuario - {$e->getMessage()}");
            return ['success' => false, 'error' => 'Error de conexión con la API'];
        }
    }

    public function iniciarSesion(array $credenciales): array
    {
        try {
            $response = Http::timeout(5)->post("{$this->baseUrl}/usuarios/login", $credenciales);
            if ($response->successful()) {
                return ['success' => true, 'data' => $response->json()];
            }
            return ['success' => false, 'error' => $this->extractError($response, 'No se pudo iniciar sesión')];
        } catch (\Exception $e) {
            Log::error("ApiService::iniciarSesion - {$e->getMessage()}");
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
            return ['success' => false, 'error' => $this->extractError($response, 'Error al crear pedido')];
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

    protected function extractError(Response $response, string $fallback): string
    {
        $detail = $response->json('detail');

        if (is_string($detail) && $detail !== '') {
            return $detail;
        }

        if (!is_array($detail)) {
            return $fallback;
        }

        $messages = [];

        foreach ($detail as $error) {
            if (is_string($error) && $error !== '') {
                $messages[] = $error;
                continue;
            }

            if (!is_array($error)) {
                continue;
            }

            $field = $this->extractFieldName($error['loc'] ?? []);
            $type = $error['type'] ?? null;
            $message = $error['msg'] ?? null;

            if ($type === 'extra_forbidden') {
                $messages[] = $field
                    ? "El campo {$field} no está permitido."
                    : 'Se enviaron datos no permitidos.';
                continue;
            }

            if (is_string($message) && $message !== '') {
                $messages[] = $field ? "{$field}: {$message}" : $message;
            }
        }

        $messages = array_values(array_unique(array_filter($messages)));

        return $messages !== [] ? implode(' ', $messages) : $fallback;
    }

    protected function extractFieldName(array $loc): ?string
    {
        $field = null;

        foreach ($loc as $segment) {
            if ($segment === 'body' || is_int($segment)) {
                continue;
            }

            $field = (string) $segment;
        }

        if (!$field) {
            return null;
        }

        return str_replace('_', ' ', $field);
    }
}
