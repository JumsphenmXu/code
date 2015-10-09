#include <iostream>


/*
 * REMEMBER WHAT:
 * Default parameters and function overloads are resolved by its static TYPE.
 * And function in the Derived class can HIDEs their Base class counter-part(competitors) 
 */


using std::cout;
using std::endl;


/* for overload resolution */
/* dummy struct */
class DataType {
public:
	DataType(int i) : d_(i) { }
	DataType(double d) : d_(d) { }

	const double get() const {
		return d_;
	}

	void set(double d) {
		d_ = d;
	}

	void set(int i) {
		d_ = i;
	}

private:
	double d_;
};


class Base {
public:
	virtual void func(int) {
		cout << "Base::func(int)" << endl;
	}

	virtual void func(double) {
		cout << "Base::func(double)" << endl;
	}

	virtual void gunc(int i = 10) {
		cout << "Base::gunc(int i = 10), i = " << i << endl;
	}
};


class Derived : public Base {
public:
	// using Base::func;
	void func(DataType dt) {
		cout << "Derived::func(DataType dt), " << dt.get() << endl;
	}

	void gunc(int i = 20) {
		cout << "Derived::gunc(int i = 20), i = " << i << endl;
	}
};


int main() {
	Base b;
	Derived d;
	Base *pd = new Derived();

	b.func(1.0);	// print "Base::func(double)"

	/*
	 * Explanation for d.func(1.0);
	 * Here OVERLOAD resolution happened here, so static TYPE do the job.
	 * why this happens is because that Derived::func(DataType dt) HIDEs Base::func(double)
	 * and <double> can be implicitly convert to <DataType>
	 ********************************************************
	 ********************************************************
	 * if you want print out "Derived::func(double)", you can
	 * explicitly bring their definition by using command, namely
	 * using Base::func();
	 */
	d.func(1.0);	// print "Derived::func(DataType dt), 1"


	/*
	 * Explanation for pd->func(1.0);
	 * OVERLOAD is resolved by its static TYPE, here namely Base.
	 * (Base *pd = new Derived()) 
	 */
	pd->func(1.0);	// print "Base::func(double)"


	b.gunc();		// print "Base::gunc(int i = 10), i = 10"
	d.gunc();		// print "Derived::gunc(int i = 20), i = 20"

	/* 
	 * Explanation for pd->gunc();
	 * gunc(int i = 10) is virtually defined int Base class, so
	 * Derived::gunc(int i = 20) OVERRIDEs Base::gunc(int i = 10),
	 * while default parameters, the same as overload, is resolved according to
	 * the static TYPE, here pd's static is Base class, so the PARAMETER i equals to 10
	 */
	pd->gunc();		// print "Derived::gunc(int i = 20), i = 10"

	/*
	 * REMEMBER WHAT:
	 * Default parameters and function overloads are resolved by its static TYPE.
	 * And function in the Derived class can HIDEs their Base class counter-part(competitors) 
	 */

	return 0;
}