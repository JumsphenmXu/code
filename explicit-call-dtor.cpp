#include <iostream>


class ExplicitDtor {
public:
	~ExplicitDtor() {
		std::cout << "Destructor can be called explicitly !!!" << std::endl;
	}
};


int main() {
	/*
	 *	Only in the way when 
	 *	::operator new(size_t size) + placement new + ::operator delete(void *)
	 *	called, then dtor can be explicitly called by programmers.
	 *	Substituting ::operator new(size_t) by malloc(size_t) and accordingly
	 *	::operator delete(void *) by free(void *) is also applicable.
	 */

	// ::operator new(size_t size) allocate the raw memory
	ExplicitDtor *ped = static_cast<ExplicitDtor *>(::operator new(sizeof(ExplicitDtor)));
	// ExplicitDtor *ped = static_cast<ExplicitDtor *>(malloc(sizeof(ExplicitDtor)));

	// placement new to construct the ExplicitDtor object
	new (ped) ExplicitDtor();

	// explicitly call the ExplicitDtor dtor
	ped->~ExplicitDtor();

	// deallocate the raw memory which was allocated by ::operator new(size_t size)
	::operator delete(ped);
	// free(ped);


	return 0;
}