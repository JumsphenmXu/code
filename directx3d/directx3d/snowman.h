#ifndef __SNOWMAN_H__
#define __SNOWMAN_H__

#include "stdafx.h"
#include "d3dutil.h"

namespace xd3d {
	enum SnowmanRotation {
		SR_X = 1,
		SR_Y = 2,
		SR_Z = 4
	};

	const float XEPSILON = 0.001f;

	class Snowman {
	public:
		Snowman(IDirect3DDevice9* device);
		Snowman(IDirect3DDevice9* device, xd3d::Vertex* vertices, int length);

		void Update(enum SnowmanRotation sr = SnowmanRotation::SR_Y);
		void Update(const float xoffset, const float yoffset, const float zoffset);
		xd3d::Vertex* GetVertices(xd3d::Vertex* vertices);
		int GetLength();

		void PreRender();
		void Render();

		~Snowman();
	private:
		IDirect3DDevice9* _device;
		IDirect3DVertexBuffer9* _verticesbuf;
		xd3d::Vertex* _vertices;
		int _length;
		float _angle;
	};
}


#endif