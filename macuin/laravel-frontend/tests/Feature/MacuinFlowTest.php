<?php

namespace Tests\Feature;

use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class MacuinFlowTest extends TestCase
{
    public function test_registration_only_sends_supported_fields_to_api(): void
    {
        Http::fake([
            'http://api:8000/v1/usuarios/registro' => function (Request $request) {
                $this->assertSame([
                    'nombre' => 'Juan Perez',
                    'email' => 'juan@example.com',
                    'telefono' => '4461234567',
                    'password' => 'secreto123',
                ], $request->data());

                return Http::response([
                    'id' => 1,
                    'nombre' => 'Juan Perez',
                    'email' => 'juan@example.com',
                    'telefono' => '4461234567',
                    'rol' => 'cliente',
                ], 201);
            },
        ]);

        $response = $this->post(route('registro.post'), [
            'nombre' => 'Juan Perez',
            'email' => 'juan@example.com',
            'telefono' => '4461234567',
            'password' => 'secreto123',
            'password_confirmation' => 'secreto123',
        ]);

        $response->assertRedirect(route('catalogo'));
        $response->assertSessionHas('success');
    }

    public function test_catalog_logo_points_to_home(): void
    {
        Http::fake([
            'http://api:8000/v1/autopartes/' => Http::response([], 200),
        ]);

        $response = $this->get(route('catalogo'));

        $response->assertOk();
        $response->assertSee('href="' . route('index') . '" class="logo"', false);
    }

    public function test_cart_logo_points_to_home_and_back_link_stays_on_catalog(): void
    {
        $response = $this->get(route('carrito'));

        $response->assertOk();
        $response->assertSee('href="' . route('index') . '" class="logo"', false);
        $response->assertSee('href="' . route('catalogo') . '" class="back-link-header"', false);
    }
}
