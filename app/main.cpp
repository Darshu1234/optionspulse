#include <iostream>
#include "pricer.h"
#include <cmath>
int main(){
    // Example parameters for a European call option
    double S = 100.0; // Stock price
    double K = 105.0; // Strike price
    double r = 0.05; // Risk-free rate
    double sigma = 0.2; // Volatility
    double T = 1.0; // Time to maturity

    // Calculate the price of a European call option
    // expected output: 8.021352235143176
    double callPrice = blackScholesPricer(S, K, r, sigma, T, OptionType::Call, OptionStyle::European);
    // Calculate the price of a European put option
    // expected output: 7.900445830869176
    double putPrice = blackScholesPricer(S, K, r, sigma, T, OptionType::Put, OptionStyle::European);
    std::cout << "European Call Option Price: " << callPrice << std::endl;
    std::cout << "European Put Option Price: " << putPrice << std::endl;

    double callDelta = delta(S, K, r, sigma, T, OptionType::Call, OptionStyle::European);
    double putDelta = delta(S, K, r, sigma, T, OptionType::Put, OptionStyle::European);
    std::cout << "European Call Option Delta: " << callDelta << std::endl;
    std::cout << "European Put Option Delta: " << putDelta << std::endl;
    
    double callGamma = gamma(S, K, r, sigma, T, OptionStyle::European);
    double putGamma = gamma(S, K, r, sigma, T, OptionStyle::European);
    std::cout << "European Call Option Gamma: " << callGamma << std::endl;
    std::cout << "European Put Option Gamma: " << putGamma << std::endl;
    // expected output same for both call and put gamma
    
    double callVega = vega(S,K,r,sigma,T, OptionStyle::European);
    double putVega = vega(S,K,r,sigma,T, OptionStyle::European);
    std::cout << "European Call Option Vega: " << callVega << std::endl;
    std::cout << "European Put Option Vega: " << putVega << std::endl;
    // expected output will be same for call and put vega too.
    
    double callTheta = theta(S,K,r,sigma,T,OptionType::Call,OptionStyle::European);
    double putTheta = theta(S,K,r,sigma,T,OptionType::Put, OptionStyle::European);
    std::cout << "European Call Option Theta: " << callTheta << std::endl;
    std::cout << "European Put Option Theta: " << putTheta << std::endl;

    double callRho = rho(S,K,r,sigma,T,OptionType::Call,OptionStyle::European);
    double putRho = rho(S,K,r,sigma,T,OptionType::Put,OptionStyle::European);
    std::cout << "European Call Option Rho: " << callRho << std::endl;
    std::cout << "European Put Option Rho: " << putRho << std::endl;

    double lhs = putTheta + r * S * putDelta + 0.5 * sigma * sigma * S * S * putGamma;
    double rhs = r * putPrice;
    std::cout << "LHS: " << lhs << " RHS: " << rhs << std::endl; // satisfies Black-Scholes PDE
    double lhs1 = callTheta + r * S * callDelta + 0.5 * sigma * sigma * S * S * callGamma;
    double rhs1 = r * callPrice;
    std::cout << "LHS: " << lhs1 << " RHS: " << rhs1 << std::endl; // satisfies Black-Scholes PDE

}

