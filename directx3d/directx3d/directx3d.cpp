// directx3d.cpp : 定义应用程序的入口点。
//
#include "stdafx.h"
#include "stdafx.h"
#include "directx3d.h"
#include "d3dutil.h"
#include "camera.h"


// Globals
IDirect3DDevice9 *gDevice = NULL;

const int gWIDTH = 640;
const int gHEIGHT = 480;

Camera camer(Camera::LANDOBJECT);
// Framework Functions

bool Setup() {
	// Setup a basic scene.  The scene will be created the
	// first time this function is called.
	xd3d::DrawBasicScene(gDevice, 0.0f);

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
		D3DXMATRIX V;
		camer.getViewMatrix(&V);
		gDevice->SetTransform(D3DTS_VIEW, &V);

		gDevice->Clear(0, 0, D3DCLEAR_TARGET | D3DCLEAR_ZBUFFER, 0, 1.0f, 0);

		gDevice->BeginScene();
		xd3d::DrawBasicScene(gDevice, 1.0f);
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






/*
#define MAX_LOADSTRING 100

// 全局变量:
HINSTANCE hInst;								// 当前实例
TCHAR szTitle[MAX_LOADSTRING];					// 标题栏文本
TCHAR szWindowClass[MAX_LOADSTRING];			// 主窗口类名

// 此代码模块中包含的函数的前向声明:
ATOM				MyRegisterClass(HINSTANCE hInstance);
BOOL				InitInstance(HINSTANCE, int);
LRESULT CALLBACK	WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK	About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY _tWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPTSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

 	// TODO: 在此放置代码。
	MSG msg;
	HACCEL hAccelTable;

	// 初始化全局字符串
	LoadString(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadString(hInstance, IDC_DIRECTX3D, szWindowClass, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	// 执行应用程序初始化:
	if (!InitInstance (hInstance, nCmdShow))
	{
		return FALSE;
	}

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_DIRECTX3D));

	// 主消息循环:
	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	return (int) msg.wParam;
}



//
//  函数: MyRegisterClass()
//
//  目的: 注册窗口类。
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASSEX wcex;

	wcex.cbSize = sizeof(WNDCLASSEX);

	wcex.style			= CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc	= WndProc;
	wcex.cbClsExtra		= 0;
	wcex.cbWndExtra		= 0;
	wcex.hInstance		= hInstance;
	wcex.hIcon			= LoadIcon(hInstance, MAKEINTRESOURCE(IDI_DIRECTX3D));
	wcex.hCursor		= LoadCursor(NULL, IDC_ARROW);
	wcex.hbrBackground	= (HBRUSH)(COLOR_WINDOW+1);
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_DIRECTX3D);
	wcex.lpszClassName	= szWindowClass;
	wcex.hIconSm		= LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return RegisterClassEx(&wcex);
}

//
//   函数: InitInstance(HINSTANCE, int)
//
//   目的: 保存实例句柄并创建主窗口
//
//   注释:
//
//        在此函数中，我们在全局变量中保存实例句柄并
//        创建和显示主程序窗口。
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   HWND hWnd;

   hInst = hInstance; // 将实例句柄存储在全局变量中

   hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

   if (!hWnd)
   {
      return FALSE;
   }

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  函数: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  目的: 处理主窗口的消息。
//
//  WM_COMMAND	- 处理应用程序菜单
//  WM_PAINT	- 绘制主窗口
//  WM_DESTROY	- 发送退出消息并返回
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	int wmId, wmEvent;
	PAINTSTRUCT ps;
	HDC hdc;

	switch (message)
	{
	case WM_COMMAND:
		wmId    = LOWORD(wParam);
		wmEvent = HIWORD(wParam);
		// 分析菜单选择:
		switch (wmId)
		{
		case IDM_ABOUT:
			DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		// TODO: 在此添加任意绘图代码...
		EndPaint(hWnd, &ps);
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}

// “关于”框的消息处理程序。
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	UNREFERENCED_PARAMETER(lParam);
	switch (message)
	{
	case WM_INITDIALOG:
		return (INT_PTR)TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			EndDialog(hDlg, LOWORD(wParam));
			return (INT_PTR)TRUE;
		}
		break;
	}
	return (INT_PTR)FALSE;
}
*/