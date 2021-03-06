// directx3d.cpp : 定义应用程序的入口点。
//
#include "stdafx.h"
#include "stdafx.h"
#include "directx3d.h"
#include "d3dutil.h"
#include "camera.h"
#include "snowman.h"

// Globals
IDirect3DDevice9* gDevice = NULL;
xd3d::Snowman* gSnowman = NULL;

const int gWIDTH = 640;
const int gHEIGHT = 480;

Camera camer(Camera::LANDOBJECT);
// Framework Functions

bool Setup() {
	// Setup a basic scene.  The scene will be created the
	// first time this function is called.
	xd3d::DrawBasicScene(gDevice, 0.0f);
	gSnowman = new xd3d::Snowman(gDevice);

	// Set projection matrix.
	D3DXMATRIX projMat;
	D3DXMatrixPerspectiveFovLH(&projMat, D3DX_PI*0.25f, (float)gWIDTH/(float)gHEIGHT, 1.0f, 1000.0f);
	gDevice->SetTransform(D3DTS_PROJECTION, &projMat);

	return true;
}


void cleanUp() {
	xd3d::DrawBasicScene(NULL, 0.0f);
}


bool Display(float timeDelta) {
	if (gDevice) {
		// Update the camera

		if (::GetAsyncKeyState('W') & 0x8000f) {
			camer.walk(4.0f * timeDelta);
		}

		if (::GetAsyncKeyState('S') & 0x8000f) {
			camer.walk(-4.0f * timeDelta);
		}

		if (::GetAsyncKeyState('A') & 0x8000f) {
			camer.strafe(-4.0f * timeDelta);
		}

		if (::GetAsyncKeyState('D') & 0x8000f) {
			camer.strafe(4.0f * timeDelta);
		}

		if (::GetAsyncKeyState('R') & 0x8000f) {
			camer.fly(4.0f * timeDelta);
		}

		if (::GetAsyncKeyState('F') & 0x8000f) {
			camer.fly(-4.0f * timeDelta);
		}

		if (::GetAsyncKeyState(VK_UP) & 0x8000f) {
			camer.pitch(1.0f * timeDelta);
		}

		if(::GetAsyncKeyState(VK_DOWN) & 0x8000f) {
			camer.pitch(-1.0f * timeDelta);
		}

		if (::GetAsyncKeyState(VK_LEFT) & 0x8000f) {
			camer.yaw(-1.0f * timeDelta);
		}
			
		if (::GetAsyncKeyState(VK_RIGHT) & 0x8000f) {
			camer.yaw(1.0f * timeDelta);
		}

		if (::GetAsyncKeyState('N') & 0x8000f) {
			camer.roll(1.0f * timeDelta);
		}

		if (::GetAsyncKeyState('M') & 0x8000f) {
			camer.roll(-1.0f * timeDelta);
		}

		// Update the view matrix representing the cameras 
        // new position/orientation.
		gSnowman->Update(xd3d::SnowmanRotation::SR_Z);

		D3DXMATRIX V;
		camer.getViewMatrix(&V);
		gDevice->SetTransform(D3DTS_VIEW, &V);

		gDevice->Clear(0, 0, D3DCLEAR_TARGET | D3DCLEAR_ZBUFFER, 0, 1.0f, 0);

		gDevice->BeginScene();

		xd3d::DrawBasicScene(gDevice, 1.0f);
		gDevice->SetTransform(D3DTS_VIEW, &V);
		gSnowman->Render();

		gDevice->EndScene();

		gDevice->Present(0, 0, 0, 0);
	}

	return true;
}


LRESULT CALLBACK xd3d::WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
	switch (msg) {
	case WM_DESTROY:
		::PostQuitMessage(0);
		break;
	case WM_KEYDOWN:
		if (wParam == VK_ESCAPE) {
			::DestroyWindow(hwnd);
		}
		break;
	}

	return ::DefWindowProc(hwnd, msg, wParam, lParam);
}


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE prevInstance, PSTR cmdline, int showCmd) {
	if (!xd3d::InitD3D(hInstance, 640, 480, true, D3DDEVTYPE_HAL, &gDevice)) {
		::MessageBox(0, L"InitD3D FAILED !!!", 0, 0);
		return 0;
	}

	if (!Setup()) {
		::MessageBox(0, L"Setup FAILED !!!", 0, 0);
		return 0;
	}

	xd3d::EnterMsgLoop(Display);
	cleanUp();
	gDevice->Release();

	return 0;
}