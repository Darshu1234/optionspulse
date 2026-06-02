#pragma once

enum class OptionType { Call, Put };
enum class OptionStyle { European, American };
double normCDF(double x);
double normPDF(double x);
double blackScholesPricer(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle);
double delta(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle);
double gamma(double S,double K,double r, double sigma, double T, OptionStyle optionStyle);
double vega(double S, double K, double r, double sigma, double T, OptionStyle optionStyle);
double theta(double S, double K, double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle);
double rho(double S, double K,double r, double sigma, double T, OptionType optionType, OptionStyle optionStyle);
double NewtonRaphson(double S,double K, double r, double T, double price, OptionType optionType, OptionStyle optionStyle);
