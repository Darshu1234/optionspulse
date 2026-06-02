#include <pybind11/pybind11.h>
#include "pricer.h"

namespace py = pybind11;

PYBIND11_MODULE(optionspulse,m){
    // python has no concept of enum, so we do this to
    // permit python writers to use optionspulse.OptionType.Call 
    // instead of a raw number
    py::enum_<OptionType>(m, "OptionType")
    .value("Call", OptionType::Call) // maps a C++ enum value to a python name
    .value("Put", OptionType::Put) 
    .export_values();
   // similarly for option style
    py::enum_<OptionStyle>(m, "OptionStyle")
    .value("European", OptionStyle::European)
    .value("American", OptionStyle::American)
    .export_values();
    // m is the module object
    // expose functions from pricer.cpp to python
    m.def("price",&blackScholesPricer, "Price a European option using Black-Scholes");
    m.def("delta",&delta,"Calculate delta for a European option");
    m.def("gamma",&gamma,"Calculate gamma for a European option");
    m.def("vega",&vega,"Calculate vega for a European option");
    m.def("theta",&theta,"Calculate theta for a European option");
    m.def("rho",&rho,"Calculate rho for a European option");
    m.def("volatility", &NewtonRaphson, "Calculate implied volatility for a European option");
}
