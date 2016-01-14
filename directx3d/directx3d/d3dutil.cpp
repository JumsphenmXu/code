#include "stdafx.h"
#include "d3dutil.h"
#include <Mmsystem.h>

const DWORD xd3d::Vertex::FVF = D3DFVF_XYZ | D3DFVF_NORMAL | D3DFVF_TEX1;

bool xd3d::InitD3D(HINSTANCE hInstance, int width, int height,
				   bool windowed, D3DDEVTYPE deviceType, IDirect3DDevice9 **device) {
	// Create main window
	WNDCLASS wndcls;
	::ZeroMemory(&wndcls, sizeof(WNDCLASS));
	wndcls.style = CS_HREDRAW | CS_VREDRAW;
	wndcls.lpfnWndProc = xd3d::WndProc;
	wndcls.cbClsExtra = 0;
	wndcls.cbClsExtra = 0;
	wndcls.hInstance = hInstance;
	wndcls.hIcon = LoadIcon(0, IDI_APPLICATION);
	wndcls.hCursor = LoadCursor(0, IDC_ARROW);
	wndcls.hbrBackground = (HBRUSH) GetStockObject(WHITE_BRUSH);
	wndcls.lpszMenuName = 0;
	wndcls.lpszClassName = L"D3d";

	if (!RegisterClass(&wndcls)) {
		::MessageBox(0, L"Register window class FAILED !!!", 0, 0);
		return false;
	}

	HWND hwnd = 0;
	hwnd = ::CreateWindow(L"D3d", L"D3d",
			WS_EX_TOPMOST, 0, 0, width, height, 0, 0, hInstance, 0);

	if (!hwnd) {
		::MessageBox(0, L"Create window FAILED !!!", 0, 0);
		return false;
	}

	::ShowWindow(hwnd, SW_SHOW);
	::UpdateWindow(hwnd);

	// Initialize Direct3D
	HRESULT hr = 0;

	// Step 1: Create the IDirect3D9 object
	IDirect3D9 *d3dObject = NULL;
	d3dObject = Direct3DCreate9(D3D_SDK_VERSION);

	if (!d3dObject) {
		::MessageBox(0, L"Create IDirect3D9 FAILED !!!", 0, 0);
		return false;
	}

	// Step 2: Check for hardware vertex processing
	D3DCAPS9 caps;
	d3dObject->GetDeviceCaps(D3DADAPTER_DEFAULT, deviceType, &caps);

	int vp = 0;
	if (caps.DevCaps & D3DDEVCAPS_HWTRANSFORMANDLIGHT) {
		vp = D3DCREATE_HARDWARE_VERTEXPROCESSING;
	} else {
		vp = D3DCREATE_SOFTWARE_VERTEXPROCESSING;
	}

	// Step 3: Fill out the D3DPRESENT_PARAMETERS structure
	D3DPRESENT_PARAMETERS d3dParam;
	::ZeroMemory(&d3dParam, sizeof(D3DPRESENT_PARAMETERS));

	d3dParam.BackBufferWidth = width;
	d3dParam.BackBufferHeight = height;
	d3dParam.BackBufferFormat = D3DFMT_X8R8G8B8;
	d3dParam.BackBufferCount = 1;
	d3dParam.MultiSampleType = D3DMULTISAMPLE_NONE;
	d3dParam.MultiSampleQuality = 0;
	d3dParam.SwapEffect = D3DSWAPEFFECT_DISCARD;
	d3dParam.hDeviceWindow = hwnd;
	d3dParam.Windowed = windowed;
	d3dParam.EnableAutoDepthStencil = true;
	d3dParam.AutoDepthStencilFormat = D3DFMT_D24S8;
	d3dParam.Flags = 0;
	d3dParam.FullScreen_RefreshRateInHz = D3DPRESENT_RATE_DEFAULT;
	d3dParam.PresentationInterval = D3DPRESENT_INTERVAL_IMMEDIATE;

	// Step 4: Create the device
	hr = d3dObject->CreateDevice(D3DADAPTER_DEFAULT, deviceType, hwnd, vp, &d3dParam, device);
	if (FAILED(hr)) {
		d3dParam.AutoDepthStencilFormat = D3DFMT_D16;
		hr = d3dObject->CreateDevice(D3DADAPTER_DEFAULT, deviceType, hwnd, vp, &d3dParam, device);

		if (FAILED(hr)) {
			d3dObject->Release();
			::MessageBox(0, L"Create Device FAILED !!!", 0, 0);
			return false;
		}
	}

	d3dObject->Release();
	return true;
}

int xd3d::EnterMsgLoop(bool (*lpfnDisplay)(float timeDelta)) {
	MSG msg;
	::ZeroMemory(&msg, sizeof(MSG));

	static float lastTime = (float) timeGetTime();
	while (msg.message != WM_QUIT) {
		if (::PeekMessage(&msg, 0, 0, 0, PM_REMOVE)) {
			::TranslateMessage(&msg);
			::DispatchMessage(&msg);
		} else {
			float curTime = (float) timeGetTime();
			float timeDelta = (curTime - lastTime) * 0.001f;
			lpfnDisplay(timeDelta);
			lastTime = curTime;
		}
	}

	return msg.wParam;
}


D3DLIGHT9 xd3d::InitDirectionalLight(D3DXVECTOR3* direction, D3DXCOLOR* color) {
	D3DLIGHT9 light;
	::ZeroMemory(&light, sizeof(light));

	light.Type      = D3DLIGHT_DIRECTIONAL;
	light.Ambient   = *color * 0.4f;
	light.Diffuse   = *color;
	light.Specular  = *color * 0.6f;
	light.Direction = *direction;

	return light;
}


D3DLIGHT9 xd3d::InitPointLight(D3DXVECTOR3* position, D3DXCOLOR* color) {
	D3DLIGHT9 light;
	::ZeroMemory(&light, sizeof(light));

	light.Type      = D3DLIGHT_POINT;
	light.Ambient   = *color * 0.4f;
	light.Diffuse   = *color;
	light.Specular  = *color * 0.6f;
	light.Position  = *position;
	light.Range        = 1000.0f;
	light.Falloff      = 1.0f;
	light.Attenuation0 = 1.0f;
	light.Attenuation1 = 0.0f;
	light.Attenuation2 = 0.0f;

	return light;
}


D3DLIGHT9 xd3d::InitSpotLight(D3DXVECTOR3* position, D3DXVECTOR3* direction, D3DXCOLOR* color) {
	D3DLIGHT9 light;
	::ZeroMemory(&light, sizeof(light));

	light.Type      = D3DLIGHT_SPOT;
	light.Ambient   = *color * 0.4f;
	light.Diffuse   = *color;
	light.Specular  = *color * 0.6f;
	light.Position  = *position;
	light.Direction = *direction;
	light.Range        = 1000.0f;
	light.Falloff      = 1.0f;
	light.Attenuation0 = 1.0f;
	light.Attenuation1 = 0.0f;
	light.Attenuation2 = 0.0f;
	light.Theta        = 0.5f;
	light.Phi          = 0.7f;

	return light;
}


D3DMATERIAL9 xd3d::InitMtrl(D3DXCOLOR a, D3DXCOLOR d, D3DXCOLOR s, D3DXCOLOR e, float p) {
	D3DMATERIAL9 mtrl;
	mtrl.Ambient  = a;
	mtrl.Diffuse  = d;
	mtrl.Specular = s;
	mtrl.Emissive = e;
	mtrl.Power    = p;
	return mtrl;
}

xd3d::BoundingBox::BoundingBox() {
	// infinite small 
	_min.x = xd3d::INFINITY;
	_min.y = xd3d::INFINITY;
	_min.z = xd3d::INFINITY;

	_max.x = -xd3d::INFINITY;
	_max.y = -xd3d::INFINITY;
	_max.z = -xd3d::INFINITY;
}

bool xd3d::BoundingBox::isPointInside(D3DXVECTOR3& p) {
	if( p.x >= _min.x && p.y >= _min.y && p.z >= _min.z &&
		p.x <= _max.x && p.y <= _max.y && p.z <= _max.z ) {
		return true;
	} else {
		return false;
	}
}

xd3d::BoundingSphere::BoundingSphere() {
	_radius = 0.0f;
}

bool xd3d::DrawBasicScene(IDirect3DDevice9* device, float scale) {
	static IDirect3DVertexBuffer9* floor  = 0;
	static IDirect3DTexture9*      tex    = 0;
	static ID3DXMesh*              pillar = 0;

	////////////////////////////////////////////////////////
	// By Xinhui
	// construct the snow man vertices
	static IDirect3DVertexBuffer9* StillSnowman = 0;
	static IDirect3DVertexBuffer9* MovingSnowman = 0;
	////////////////////////////////////////////////////////

	HRESULT hr = 0;

	if( device == 0 ) {
		if( floor && tex && pillar ) {
			// they already exist, destroy them
			xd3d::Release<IDirect3DVertexBuffer9*>(floor);
			xd3d::Release<IDirect3DTexture9*>(tex);
			xd3d::Release<ID3DXMesh*>(pillar);
			xd3d::Release<IDirect3DVertexBuffer9*>(StillSnowman);
			xd3d::Release<IDirect3DVertexBuffer9*>(MovingSnowman);
		}
	} else if( !floor && !tex && !pillar ) {
		// they don't exist, create them
		device->CreateVertexBuffer(
			6 * sizeof(xd3d::Vertex),
			0, 
			xd3d::Vertex::FVF,
			D3DPOOL_MANAGED,
			&floor,
			0);

		Vertex* v = 0;
		floor->Lock(0, 0, (void**)&v, 0);

		v[0] = Vertex(-20.0f, -2.5f, -20.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		v[1] = Vertex(-20.0f, -2.5f,  20.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f);
		v[2] = Vertex( 20.0f, -2.5f,  20.0f, 0.0f, 1.0f, 0.0f, 1.0f, 0.0f);

		v[3] = Vertex(-20.0f, -2.5f, -20.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		v[4] = Vertex( 20.0f, -2.5f,  20.0f, 0.0f, 1.0f, 0.0f, 1.0f, 0.0f);
		v[5] = Vertex( 20.0f, -2.5f, -20.0f, 0.0f, 1.0f, 0.0f, 1.0f, 1.0f);

		floor->Unlock();

		//////////////////////////////////////////////////////////////
		// By Xinhui
		// Initialize the snow man
		// #1: The snowman which is still
		device->CreateVertexBuffer(42 * sizeof(xd3d::Vertex), 0,
			xd3d::Vertex::FVF, D3DPOOL_MANAGED, &StillSnowman, 0);
	
		Vertex *s = NULL;
		StillSnowman->Lock(0, 0, (void **)&s, 0);
		const float SXOFFSET = -15.0f;
		const float SYOFFSET = 0.0f;
		const float SZOFFSET = -4.0f;
		// the front face
		s[0] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		s[1] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		s[2] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

		s[3] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		s[4] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		s[5] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

		// the left face
		s[6] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		s[7] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		s[8] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);

		s[9] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		s[10] = Vertex(SXOFFSET -2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		s[11] = Vertex(SXOFFSET -2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		
		// the right face
		s[12] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		s[13] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		s[14] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

		s[15] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		s[16] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		s[17] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

		// the back face
		s[18] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		s[19] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		s[20] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

		s[21] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		s[22] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		s[23] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

		// the down face 
		s[24] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		s[25] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		s[26] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

		s[27] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		s[28] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		s[29] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

		// the left slope face 
		s[30] = Vertex(SXOFFSET + 0.0f, SYOFFSET + 0.0f, SZOFFSET + 6.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
		s[31] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
		s[32] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);

		// the front slope face 
		s[33] = Vertex(SXOFFSET + 0.0f, SYOFFSET + 0.0f, SZOFFSET + 6.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
		s[34] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
		s[35] = Vertex(SXOFFSET - 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);

		// the right slope face 
		s[36] = Vertex(SXOFFSET + 0.0f, SYOFFSET + 0.0f, SZOFFSET + 6.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
		s[37] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
		s[38] = Vertex(SXOFFSET + 2.0f, SYOFFSET + 2.0f, SZOFFSET + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);

		// the back slope face
		s[39] = Vertex(SXOFFSET + 0.0f, SYOFFSET + 0.0f, SZOFFSET + 6.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
		s[40] = Vertex(SXOFFSET - 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
		s[41] = Vertex(SXOFFSET + 2.0f, SYOFFSET - 2.0f, SZOFFSET + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
	
		StillSnowman->Unlock();

		// #2: The snowman which is moving arround
		device->CreateVertexBuffer(42 * sizeof(xd3d::Vertex), 0,
			xd3d::Vertex::FVF, D3DPOOL_MANAGED, &MovingSnowman, 0);
		
		Vertex *m = NULL;
		MovingSnowman->Lock(0, 0, (void **)&m, 0);
		const float MXOFFSET = 15.0f;
		const float MYOFFSET = 0.0f;
		const float MZOFFSET = -4.0f;

		// the front face
		m[0] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		m[1] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		m[2] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

		m[3] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		m[4] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
		m[5] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

		// the left face
		m[6] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		m[7] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		m[8] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);

		m[9] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		m[10] = Vertex(MXOFFSET -2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		m[11] = Vertex(MXOFFSET -2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
		
		// the right face
		m[12] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		m[13] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		m[14] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

		m[15] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		m[16] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
		m[17] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

		// the back face
		m[18] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		m[19] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		m[20] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

		m[21] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		m[22] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
		m[23] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

		// the down faceMZOFFSET + 
		m[24] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		m[25] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		m[26] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

		m[27] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		m[28] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
		m[29] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

		// the left slope faceMZOFFSET + 
		m[30] = Vertex(MXOFFSET + 0.0f, MYOFFSET + 0.0f, MZOFFSET + 6.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
		m[31] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
		m[32] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);

		// the front slope faceMZOFFSET + 
		m[33] = Vertex(MXOFFSET + 0.0f, MYOFFSET + 0.0f, MZOFFSET + 6.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
		m[34] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
		m[35] = Vertex(MXOFFSET - 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);

		// the right slope faceMZOFFSET + 
		m[36] = Vertex(MXOFFSET + 0.0f, MYOFFSET + 0.0f, MZOFFSET + 6.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
		m[37] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
		m[38] = Vertex(MXOFFSET + 2.0f, MYOFFSET + 2.0f, MZOFFSET + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);

		// the back slope faceMZOFFSET + 
		m[39] = Vertex(MXOFFSET + 0.0f, MYOFFSET + 0.0f, MZOFFSET + 6.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
		m[40] = Vertex(MXOFFSET - 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
		m[41] = Vertex(MXOFFSET + 2.0f, MYOFFSET - 2.0f, MZOFFSET + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);

		MovingSnowman->Unlock();

		///////////////////////////////////////////////////////////////

		D3DXCreateCylinder(device, 0.5f, 0.5f, 5.0f, 4, 10, &pillar, 0);

		D3DXCreateTextureFromFile(device, _T("desert.bmp"), &tex);
	} else {
		// Pre-Render Setup
		device->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_LINEAR);
		device->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_LINEAR);
		device->SetSamplerState(0, D3DSAMP_MIPFILTER, D3DTEXF_POINT);

		D3DXVECTOR3 dir(0.707f, -0.707f, 0.707f);
		D3DXCOLOR col(1.0f, 1.0f, 1.0f, 1.0f);
		D3DLIGHT9 light = xd3d::InitDirectionalLight(&dir, &col);

		device->SetLight(0, &light);
		device->LightEnable(0, true);
		device->SetRenderState(D3DRS_NORMALIZENORMALS, true);
		device->SetRenderState(D3DRS_SPECULARENABLE, true);

		// Render

		D3DXMATRIX T, R, P, S;
		D3DXMatrixScaling(&S, scale, scale, scale);

		// used to rotate cylinders to be parallel with world's y-axis
		D3DXMatrixRotationX(&R, -D3DX_PI * 0.5f);

		// draw floor
		D3DXMatrixIdentity(&T);
		T = T * S;
		device->SetTransform(D3DTS_WORLD, &T);
		device->SetMaterial(&xd3d::WHITE_MTRL);
		device->SetTexture(0, tex);
		device->SetStreamSource(0, floor, 0, sizeof(Vertex));
		device->SetFVF(Vertex::FVF);
		device->DrawPrimitive(D3DPT_TRIANGLELIST, 0, 2);
		
		// draw StillSnowman
		
		D3DXMATRIX ssmatrix, ssscale;
		D3DXMatrixScaling(&ssscale, 0.4f, 0.3f, 0.6f);
		D3DXMatrixIdentity(&ssmatrix);
		ssmatrix = ssmatrix * R * ssscale;
		device->SetTransform(D3DTS_WORLD, &ssmatrix);
		device->SetMaterial(&xd3d::BLUE_MTRL);
		device->SetStreamSource(0, StillSnowman, 0, sizeof(Vertex));
		device->SetFVF(Vertex::FVF);
		device->DrawPrimitive(D3DPT_TRIANGLELIST, 0, 14);

		// draw MovingSnowman

		D3DXMATRIX msmatrix, msscale;
		D3DXMatrixScaling(&msscale, 0.4f, 0.3f, 0.6f);
		D3DXMatrixIdentity(&msmatrix);
		msmatrix = msmatrix * R * msscale;
		device->SetTransform(D3DTS_WORLD, &msmatrix);
		device->SetMaterial(&xd3d::RED_MTRL);
		device->SetStreamSource(0, MovingSnowman, 0, sizeof(Vertex));
		device->DrawPrimitive(D3DPT_TRIANGLELIST, 0, 14);

		// draw pillars
		device->SetMaterial(&xd3d::BLUE_MTRL);
		device->SetTexture(0, 0);

		/*
		for(int i = 0; i < 5; i++) {
			D3DXMatrixTranslation(&T, -5.0f, 0.0f, -15.0f + (i * 7.5f));
			P = R * T * S;
			device->SetTransform(D3DTS_WORLD, &P);
			pillar->DrawSubset(0);

			D3DXMatrixTranslation(&T, 5.0f, 0.0f, -15.0f + (i * 7.5f));
			P = R * T * S;
			device->SetTransform(D3DTS_WORLD, &P);
			pillar->DrawSubset(0);
		} */

		D3DXMatrixTranslation(&T, 0.0f, 0.0f, 8.0f);
		P = R * T * S;
		device->SetTransform(D3DTS_WORLD, &P);
		pillar->DrawSubset(0);
		/*
		device->BeginScene();
		StillSnowman->DrawSubset(0);
		MovingSnowman->DrawSubset(0);
		device->EndScene();
		device->Present(0, 0, 0, 0);
		*/
	}
	return true;
}