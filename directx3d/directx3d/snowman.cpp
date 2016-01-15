#include "stdafx.h"
#include "snowman.h"


xd3d::Snowman::Snowman(IDirect3DDevice9 *device) {
	_device = device;
	_length = 42;
	_angle = 0.0f;
	_vertices = new xd3d::Vertex[_length];

	_vertices[0] = Vertex( - 2.0f,  + 2.0f,  + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
	_vertices[1] = Vertex( + 2.0f,  + 2.0f,  + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
	_vertices[2] = Vertex( + 2.0f,  + 2.0f,  + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

	_vertices[3] = Vertex( - 2.0f,  + 2.0f,  + 4.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
	_vertices[4] = Vertex( + 2.0f,  + 2.0f,  + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);
	_vertices[5] = Vertex( - 2.0f,  + 2.0f,  + 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f);

	// the left face
	_vertices[6] = Vertex( - 2.0f,  - 2.0f,  + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
	_vertices[7] = Vertex( - 2.0f,  + 2.0f,  + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
	_vertices[8] = Vertex( - 2.0f,  + 2.0f,  + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);

	_vertices[9] = Vertex( - 2.0f,  - 2.0f,  + 4.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
	_vertices[10] = Vertex( -2.0f,  + 2.0f,  + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);
	_vertices[11] = Vertex( -2.0f,  - 2.0f,  + 0.0f, -1.0f, 0.0f, 0.0f, 1.0f, 0.0f);

	// the right face
	_vertices[12] = Vertex( + 2.0f,  + 2.0f,  + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
	_vertices[13] = Vertex( + 2.0f,  - 2.0f,  + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
	_vertices[14] = Vertex( + 2.0f,  - 2.0f,  + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

	_vertices[15] = Vertex( + 2.0f,  + 2.0f,  + 4.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
	_vertices[16] = Vertex( + 2.0f,  - 2.0f,  + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);
	_vertices[17] = Vertex( + 2.0f,  + 2.0f,  + 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f);

	// the back face
	_vertices[18] = Vertex( + 2.0f,  - 2.0f,  + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
	_vertices[19] = Vertex( - 2.0f,  - 2.0f,  + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
	_vertices[20] = Vertex( - 2.0f,  - 2.0f,  + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

	_vertices[21] = Vertex( + 2.0f,  - 2.0f,  + 4.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
	_vertices[22] = Vertex( - 2.0f,  - 2.0f,  + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);
	_vertices[23] = Vertex( + 2.0f,  - 2.0f,  + 0.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f);

	// the down face 
	_vertices[24] = Vertex( - 2.0f,  + 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
	_vertices[25] = Vertex( + 2.0f,  + 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
	_vertices[26] = Vertex( + 2.0f,  - 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

	_vertices[27] = Vertex( - 2.0f,  + 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
	_vertices[28] = Vertex( + 2.0f,  - 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);
	_vertices[29] = Vertex( - 2.0f,  - 2.0f,  + 0.0f, 0.0f, 0.0f, -1.0f, 0.0f, 0.0f);

	// the left _verticeslope face 
	_vertices[30] = Vertex( + 0.0f,  + 0.0f,  + 6.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
	_vertices[31] = Vertex( - 2.0f,  + 2.0f,  + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);
	_vertices[32] = Vertex( - 2.0f,  - 2.0f,  + 4.0f, -1.0f, 0.0f, 1.0f, 1.0f, 1.0f);

	// the front _verticeslope face 
	_vertices[33] = Vertex( + 0.0f,  + 0.0f,  + 6.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
	_vertices[34] = Vertex( + 2.0f,  + 2.0f,  + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);
	_vertices[35] = Vertex( - 2.0f,  + 2.0f,  + 4.0f, 0.0f, 1.0f, 1.0f, 0.0f, 1.0f);

	// the right _verticeslope face 
	_vertices[36] = Vertex( + 0.0f,  + 0.0f,  + 6.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
	_vertices[37] = Vertex( + 2.0f,  - 2.0f,  + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);
	_vertices[38] = Vertex( + 2.0f,  + 2.0f,  + 4.0f, 1.0f, 0.0f, 1.0f, 1.0f, 0.0f);

	// the back _verticeslope face
	_vertices[39] = Vertex( + 0.0f,  + 0.0f,  + 6.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
	_vertices[40] = Vertex( - 2.0f,  - 2.0f,  + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);
	_vertices[41] = Vertex( + 2.0f,  - 2.0f,  + 4.0f, 0.0f, -1.0f, 1.0f, 0.0f, 1.0f);

	const float MXOFFSET = 15.0f;
	const float MYOFFSET = 0.0f;
	const float MZOFFSET = -4.0f;
	xd3d::Snowman::Update(MXOFFSET, MYOFFSET, MZOFFSET);
}


xd3d::Snowman::Snowman(IDirect3DDevice9* device, xd3d::Vertex *vertices, int length) {
	_device = device;
	_length = length;

	for (int i = 0; i < _length; ++i) {
		_vertices[i] = vertices[i];
	}
}


xd3d::Snowman::~Snowman() {

}


xd3d::Vertex* xd3d::Snowman::GetVertices(xd3d::Vertex* vertices) {
	vertices = _vertices;
	return vertices;
}


int xd3d::Snowman::GetLength() {
	return _length;
}


void xd3d::Snowman::Update(enum xd3d::SnowmanRotation sr) {
	if (!_vertices || _length < 1) {
		return;
	}

	if (_angle > 2 * D3DX_PI) {
		_angle = 0.0f;
	}

	D3DXMATRIX R;
	if (sr == xd3d::SnowmanRotation::SR_X) {
		D3DXMatrixRotationX(&R, _angle);
	} else if (sr == xd3d::SnowmanRotation::SR_Y) {
		D3DXMatrixRotationY(&R, _angle);
	} else if (sr == xd3d::SnowmanRotation::SR_Z) {
		D3DXMatrixRotationZ(&R, _angle);
	}

	for (int i = 0; i < _length; ++i) {
		float x = _vertices[i]._x;
		float y = _vertices[i]._y;
		float z = _vertices[i]._z;
		_vertices[i]._x = x * R(0, 0)+ y * R(0, 1) + z * R(0, 2);
		_vertices[i]._y = x * R(1, 0)+ y * R(1, 1) + z * R(1, 2);
		_vertices[i]._z = x * R(2, 0)+ y * R(2, 1) + z * R(2, 2);
	}

	_angle += 0.05 * D3DX_PI;
}


void xd3d::Snowman::Update(const float xoffset, const float yoffset, const float zoffset) {
	if (!_vertices) {
		return;
	}

	for (int i = 0; i < _length; ++i) {
		_vertices[i]._x += xoffset;
		_vertices[i]._y += yoffset;
		_vertices[i]._z += zoffset;
	}
}


void xd3d::Snowman::PreRender() {
	_device->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_LINEAR);
	_device->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_LINEAR);
	_device->SetSamplerState(0, D3DSAMP_MIPFILTER, D3DTEXF_POINT);

	D3DXVECTOR3 dir(0.707f, -0.707f, 0.707f);
	D3DXCOLOR col(1.0f, 1.0f, 1.0f, 1.0f);
	D3DLIGHT9 light = xd3d::InitDirectionalLight(&dir, &col);

	_device->SetLight(0, &light);
	_device->LightEnable(0, true);
	_device->SetRenderState(D3DRS_NORMALIZENORMALS, true);
	_device->SetRenderState(D3DRS_SPECULARENABLE, true);
}


void xd3d::Snowman::Render() {
	xd3d::Snowman::PreRender();

	HRESULT hr = 0;
	hr = _device->CreateVertexBuffer(_length * sizeof(xd3d::Vertex), 0, xd3d::Vertex::FVF,
		D3DPOOL_MANAGED, &_verticesbuf, 0);

	if (FAILED(hr)) {
		::MessageBox(0, _T("Failed to create vertex buffer for Snowman"), 0, 0);
		return;
	}

	xd3d::Vertex *v = NULL;
	_verticesbuf->Lock(0, 0, (void**)&v, 0);
	for (int i = 0; i < _length; ++i) {
		v[i] = _vertices[i];
	}
	_verticesbuf->Unlock();


	D3DXMATRIX ssmatrix, ssscale, R;
	D3DXMatrixRotationX(&R, -D3DX_PI * 0.5f);
	D3DXMatrixScaling(&ssscale, 0.4f, 0.3f, 0.2f);
	D3DXMatrixIdentity(&ssmatrix);
	ssmatrix = ssmatrix * R * ssscale;
	_device->SetTransform(D3DTS_WORLD, &ssmatrix);
	_device->SetMaterial(&xd3d::RED_MTRL);
	_device->SetStreamSource(0, _verticesbuf, 0, sizeof(Vertex));
	_device->SetFVF(Vertex::FVF);
	_device->DrawPrimitive(D3DPT_TRIANGLELIST, 0, _length);
	Sleep(100);
}