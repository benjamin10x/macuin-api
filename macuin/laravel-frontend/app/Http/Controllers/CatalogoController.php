<?php

namespace App\Http\Controllers;

use App\Services\ApiService;

class CatalogoController extends Controller
{
    protected ApiService $api;

    public function __construct(ApiService $api)
    {
        $this->api = $api;
    }

    public function index()
    {
        $autopartes = $this->api->getAutopartes();
        return view('catalogos.catalogo', compact('autopartes'));
    }
}
