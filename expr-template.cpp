#include <iostream>

using namespace std;


// add/substract/multiply/division object functors
// <+,-,*,/> object functors
struct ExprAdd {
    static double apply(double lhs, double rhs) {
        return lhs + rhs;
    }
};

struct ExprSub {
    static double apply(double lhs, double rhs) {
        return lhs - rhs;
    }
};

struct ExprMul {
    static double apply(double lhs, double rhs) {
        return lhs * rhs;
    }
};

struct ExprDiv {
    static double apply(double lhs, double rhs) {
        return lhs / rhs;
    }
};


// Expression template
template <typename E>
struct Expr {
    Expr(E e) : _e(e) { }

    double operator() (double d) {
        return _e(d);
    }

    E _e;
};


// Variable definition
struct Var {
    double operator() (double d) {
        return d;
    }
};


// Constant definition
struct Constant {
    Constant(double d) : _d(d) { }
    Constant(int d) : _d(d) { }

    double operator() (double) {
        return _d;
    }

    const double _d;
};


// complex expression composited by Var/Constant/ComplexExpr
template <typename E1, typename E2, typename Op>
struct ComplexExpr {
    ComplexExpr(E1 lhs, E2 rhs) : _lhs(lhs), _rhs(rhs) {}

    double operator() (double d) {
        return Op::apply(_lhs(d), _rhs(d));
    } 

    E1 _lhs;
    E2 _rhs;
};


// operator overload for complex expression
// for add
template<typename E1, typename E2>
Expr<ComplexExpr<Expr<E1>, Expr<E2>, ExprAdd> > operator+ (E1 lhs, E2 rhs) {
    typedef ComplexExpr<Expr<E1>, Expr<E2>, ExprAdd> ExprType;
    return Expr<ExprType>( ExprType(Expr<E1>(lhs), Expr<E2>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprAdd> > operator+ (E lhs, int rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprAdd> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprAdd> > operator+ (int lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprAdd> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprAdd> > operator+ (E lhs, double rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprAdd> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprAdd> > operator+ (double lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprAdd> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


// for sub
template<typename E1, typename E2>
Expr<ComplexExpr<Expr<E1>, Expr<E2>, ExprSub> > operator- (E1 lhs, E2 rhs) {
    typedef ComplexExpr<Expr<E1>, Expr<E2>, ExprSub> ExprType;
    return Expr<ExprType>( ExprType(Expr<E1>(lhs), Expr<E2>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprSub> > operator- (E lhs, int rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprSub> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprSub> > operator- (int lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprSub> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprSub> > operator- (E lhs, double rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprSub> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprSub> > operator- (double lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprSub> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


// for mul
template<typename E1, typename E2>
Expr<ComplexExpr<Expr<E1>, Expr<E2>, ExprMul> > operator* (E1 lhs, E2 rhs) {
    typedef ComplexExpr<Expr<E1>, Expr<E2>, ExprMul> ExprType;
    return Expr<ExprType>( ExprType(Expr<E1>(lhs), Expr<E2>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprMul> > operator* (E lhs, int rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprMul> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprMul> > operator* (int lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprMul> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprMul> > operator* (E lhs, double rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprMul> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprMul> > operator* (double lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprMul> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


// for div
template<typename E1, typename E2>
Expr<ComplexExpr<Expr<E1>, Expr<E2>, ExprDiv> > operator/ (E1 lhs, E2 rhs) {
    typedef ComplexExpr<Expr<E1>, Expr<E2>, ExprDiv> ExprType;
    return Expr<ExprType>( ExprType(Expr<E1>(lhs), Expr<E2>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprDiv> > operator/ (E lhs, int rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprDiv> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprDiv> > operator/ (int lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprDiv> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


template<typename E>
Expr<ComplexExpr<Expr<E>, Expr<Constant>, ExprDiv> > operator/ (E lhs, double rhs) {
    typedef ComplexExpr<Expr<E>, Expr<Constant>, ExprDiv> ExprType;
    return Expr<ExprType>( ExprType(Expr<E>(lhs), Expr<Constant>(Constant(rhs))) );
}


template<typename E>
Expr<ComplexExpr<Expr<Constant>, Expr<E>, ExprDiv> > operator/ (double lhs, E rhs) {
    typedef ComplexExpr<Expr<Constant>, Expr<E>, ExprDiv> ExprType;
    return Expr<ExprType>( ExprType(Expr<Constant>(Constant(lhs)), Expr<E>(rhs)) );
}


int main() {
    Var x;
    cout << (x * x * x)(2) << endl;
    cout << (x * x + 2.0)(2) << endl;
    return 0;
}
