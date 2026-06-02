#define _USE_MATH_DEFINES
#include "pricer.h"
#include <cmath>
#include <stdexcept>



double normCDF(double x) {
    return 0.5 * (1.0 + std::erf(x / std::sqrt(2.0)));
}

double normPDF(double x){
    return 1 / std::sqrt(2 * M_PI) * std::exp(- (x * x) / 2);
}

double blackScholesPricer(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle) {
    if (optionStyle != OptionStyle::European) {
        throw std::invalid_argument("Only European options are supported with the Black-Scholes Model.");
    }
    if (S <= 0) {
        throw std::invalid_argument("Invalid input parameters: Stock price must be positive.");
    }
    if (K <= 0) {
        throw std::invalid_argument("Invalid input parameters: Strike price must be positive.");
    }
    if (sigma <= 0) {
        throw std::invalid_argument("Invalid input parameters: Volatility must be positive.");
    }
    if (T <= 0) {
        throw std::invalid_argument("Invalid input parameters: Time to maturity must be positive.");
    }

    // Calculate d1 and d2
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);

    // Calculate the option price using the Black-Scholes formula
    if (optionType == OptionType::Call) {
        return S * normCDF(d1) - K * std::exp(-r * T) * normCDF(d2);
    } else { // Put option
        return K * std::exp(-r * T) * normCDF(-d2) - S * normCDF(-d1);
    }
}

double delta(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){ 
        throw std::invalid_argument("This is only supported for European options");
    }
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    if (optionType == OptionType::Call){
        return normCDF(d1);
    }
    else{
        return normCDF(d1) - 1;
    }
}

double gamma(double S,double K,double r, double sigma, double T, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){
        throw std::invalid_argument("This is only supported for European options");
    }
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    return normPDF(d1) / (S * sigma * std::sqrt(T));
}

double vega(double S,double K,double r, double sigma, double T, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){
        throw std::invalid_argument("This is only supported for European options");
    }
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    return S * std::sqrt(T) * normPDF(d1);
}

double theta(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){
        throw std::invalid_argument("This is only supported for European options");
    }
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);
    double x;
    if (optionType == OptionType::Call){
        x = -(S * normPDF(d1) * sigma / (2 * std::sqrt(T))) - r * K * std::exp(-r * T) * normCDF(d2);
    }
    else{

        x = -(S * normPDF(d1) * sigma / (2*std::sqrt(T))) + r * K * std::exp(- r * T) * normCDF(-d2);
    }
    return x;
}

double rho(double S, double K,double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){
        throw std::invalid_argument("This is only supported for European options");
    }
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);
    double x;
    if (optionType == OptionType::Call){
        x = K * T * std::exp(-r*T) * normCDF(d2);
    }
    else{
        x = - K * T * std::exp(-r*T) * normCDF(-d2);
    }
    return x;
}

double NewtonRaphson(double S,double K, double r, double T, double price, OptionType optionType, OptionStyle optionStyle){
    if (optionStyle != OptionStyle::European){
        throw std::invalid_argument("This is only supported for European options");
    }    
    double sigma = 0.2;
    double p = 0;
    while (!(abs(p-price) < 0.0001)){
        p = blackScholesPricer(S,K,r,sigma,T,optionType,optionStyle);
        double v = vega(S,K,r,sigma,T,optionStyle);
        if (v<1e-10) break;
        sigma = sigma - (p-price) / v;
    }
    return sigma;
}






