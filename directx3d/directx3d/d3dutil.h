#ifndef __d3dUtility_H__
#define __d3dUtility_H__

#include "stdafx.h"
#include <d3d9.h>
#include <d3dx9.h>
#include <string>

namespace xd3d {
	bool InitD3D(HINSTANCE hInstance, int width, int height,
		bool windowed, D3DDEVTYPE deviceType, IDirect3DDevice9 **device);

	int EnterMsgLoop(bool (*lpfnDisplay)(float timeDelta));

	LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

	template<typename T>
	void Release(T t) {
		if (t) {
			t->Release();
			t = 0;
		}
	}

	template<typename T>
	void Delete(T t) {
		if (t) {
			delete t;
			t = 0;
		}
	}

	// Colors
	const D3DXCOLOR      WHITE( D3DCOLOR_XRGB(255, 255, 255) );
	const D3DXCOLOR      BLACK( D3DCOLOR_XRGB(  0,   0,   0) );
	const D3DXCOLOR        RED( D3DCOLOR_XRGB(255,   0,   0) );
	const D3DXCOLOR      GREEN( D3DCOLOR_XRGB(  0, 255,   0) );
	const D3DXCOLOR       BLUE( D3DCOLOR_XRGB(  0,   0, 255) );
	const D3DXCOLOR     YELLOW( D3DCOLOR_XRGB(255, 255,   0) );
	const D3DXCOLOR       CYAN( D3DCOLOR_XRGB(  0, 255, 255) );
	const D3DXCOLOR    MAGENTA( D3DCOLOR_XRGB(255,   0, 255) );

	// Lights
	D3DLIGHT9 InitDirectionalLight(D3DXVECTOR3* direction, D3DXCOLOR* color);
	D3DLIGHT9 InitPointLight(D3DXVECTOR3* position, D3DXCOLOR* color);
	D3DLIGHT9 InitSpotLight(D3DXVECTOR3* position, D3DXVECTOR3* direction, D3DXCOLOR* color);

	// Materials
	D3DMATERIAL9 InitMtrl(D3DXCOLOR a, D3DXCOLOR d, D3DXCOLOR s, D3DXCOLOR e, float p);

	const D3DMATERIAL9 WHITE_MTRL  = InitMtrl(WHITE, WHITE, WHITE, BLACK, 2.0f);
	const D3DMATERIAL9 RED_MTRL    = InitMtrl(RED, RED, RED, BLACK, 2.0f);
	const D3DMATERIAL9 GREEN_MTRL  = InitMtrl(GREEN, GREEN, GREEN, BLACK, 2.0f);
	const D3DMATERIAL9 BLUE_MTRL   = InitMtrl(BLUE, BLUE, BLUE, BLACK, 2.0f);
	const D3DMATERIAL9 YELLOW_MTRL = InitMtrl(YELLOW, YELLOW, YELLOW, BLACK, 2.0f);

	// Bounding Objects
	struct BoundingBox {
		BoundingBox();
		bool isPointInside(D3DXVECTOR3& p);

		D3DXVECTOR3 _min;
		D3DXVECTOR3 _max;
	};

	struct BoundingSphere {
		BoundingSphere();

		D3DXVECTOR3 _center;
		float       _radius;
	};


	// Constants
	const float INFINITY = FLT_MAX;
	const float EPSILON  = 0.001f;

	// Drawing
	// Function references "desert.bmp" internally.  This file must
	// be in the working directory.
	bool DrawBasicScene(
		IDirect3DDevice9* device,// Pass in 0 for cleanup.
		float scale);            // uniform scale 


	void PreRender(IDirect3DDevice9* device);
	// void Render();
	// void PostRender();

	// Vertex Structures
	struct Vertex {
		Vertex() {}
		Vertex(float x, float y, float z, 
			float nx, float ny, float nz,
			float u, float v) {
			_x  = x;  _y  = y;  _z  = z;
			_nx = nx; _ny = ny; _nz = nz;
			_u  = u;  _v  = v;
		}

		float _x, _y, _z;
		float _nx, _ny, _nz;
		float _u, _v;

		static const DWORD FVF;
	};
}

#endif