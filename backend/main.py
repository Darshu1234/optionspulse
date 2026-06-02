import os;
os.add_dll_directory("C:/msys64/ucrt64/bin")
import optionspulse # type: ignore
from pydantic import BaseModel
from fastapi import FastAPI
from enum import Enum
import yfinance as yf
import numpy as np
from backend.models import PricingHistory, SavedPosition
from backend.database import SessionLocal
from datetime import datetime, date, timedelta
from typing import List

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


        
class OptionType(Enum):
    Call = "Call"
    Put = "Put"

class OptionStyle(Enum):
    European = "European"
    American = "American"

class PriceRequest(BaseModel):
    S: float
    K: float
    r: float
    sigma: float
    T: float
    optionType: OptionType
    optionStyle: OptionStyle
    ticker: str

class GreeksResponse(BaseModel):
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float

class QuoteRequest(BaseModel):
    ticker : str
class QuoteResponse(BaseModel):
    S: float
    sigma: float

class GraphRequest(BaseModel):
    S: float
    K: float
    r: float
    sigma: float
    T: float
    optionType: OptionType
    optionStyle: OptionStyle


class GraphResponse(BaseModel):
    S: float
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float

class pnlRequest(BaseModel):
    S: float
    K: float
    r: float
    T: float
    optionType: OptionType
    optionStyle: OptionStyle
    price: float
    sigma: float

class pnlResponse(BaseModel):
    S: List[float]
    sigma: List[float]
    pnl_grid: List[List[float]]

class volRequest(BaseModel):
    S: float
    K: float
    r: float
    T: float
    optionType: OptionType
    optionStyle: OptionStyle
    price: float

class volResponse(BaseModel):
    sigma: float

class volSmileRequest(BaseModel):
    S: float
    r: float
    T: float
    ticker: str
    optionStyle: OptionStyle
    optionType: OptionType

class volSmileResponse(BaseModel):
    vol_list: List[float]
    K_list: List[float]



@app.post("/price")
def price(request: PriceRequest):
    db = SessionLocal()
    try:
        if request.optionType == OptionType.Call:
            cpp_type = optionspulse.OptionType.Call
        else:
            cpp_type = optionspulse.OptionType.Put
        
        if request.optionStyle == OptionStyle.European:
            cpp_style = optionspulse.OptionStyle.European
        else:
            cpp_style = optionspulse.OptionStyle.American

        result = optionspulse.price(request.S,request.K,
                                    request.r,request.sigma,request.T,
                                    cpp_type,
                                    cpp_style)
        record = PricingHistory(ticker=request.ticker,s=request.S,k=request.K,
                                r=request.r,sigma=request.sigma,t=request.T, 
                                option_type=request.optionType.value,option_style=request.optionStyle.value,
                                price=result,created_at=datetime.utcnow())
        db.add(record)
        db.commit()
        return result
    finally:
        db.close()

@app.post("/greeks")
def greeks(request: PriceRequest):
    db = SessionLocal()
    try:
        if request.optionType == OptionType.Call:
            cpp_type = optionspulse.OptionType.Call
        else:
            cpp_type = optionspulse.OptionType.Put
        
        if request.optionStyle == OptionStyle.European:
            cpp_style = optionspulse.OptionStyle.European
        else:
            cpp_style = optionspulse.OptionStyle.American

        delta_res = optionspulse.delta(request.S,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style)
        gamma_res = optionspulse.gamma(request.S,request.K,request.r,request.sigma,request.T,cpp_style)
        vega_res = optionspulse.vega(request.S,request.K,request.r,request.sigma,request.T,cpp_style)
        theta_res = optionspulse.theta(request.S,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style)
        rho_res = optionspulse.rho(request.S,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style)
        
        price_res = optionspulse.price(request.S,request.K,
                                    request.r,request.sigma,request.T,
                                    cpp_type,
                                    cpp_style)
        
        record = SavedPosition(ticker=request.ticker,s=request.S,k=request.K,
                                r=request.r,sigma=request.sigma,t=request.T, 
                                option_type=request.optionType.value,option_style=request.optionStyle.value,
                                price=price_res,delta=delta_res,gamma=gamma_res,vega=vega_res,theta=theta_res,
                                rho=rho_res,created_at=datetime.utcnow())
        db.add(record)
        db.commit()
        return GreeksResponse(delta=delta_res, gamma=gamma_res, vega=vega_res, theta=theta_res, rho=rho_res)
    finally:
        db.close()

@app.post("/quote")
def quote(request: QuoteRequest):
    ticker_res = yf.Ticker(request.ticker)
    price_res = ticker_res.info["currentPrice"]
    hist = ticker_res.history(period="1y")
    close = hist["Close"]
    log_ratio = np.log(close / close.shift(1))
    sigma_res = np.std(log_ratio) * np.sqrt(252)
    return QuoteResponse(S=price_res, sigma = sigma_res)

@app.post("/greekgraphs")
def greekgraph(request: GraphRequest):

    if request.optionType == OptionType.Call:
        cpp_type = optionspulse.OptionType.Call
    else:
        cpp_type = optionspulse.OptionType.Put
    
    if request.optionStyle == OptionStyle.European:
        cpp_style = optionspulse.OptionStyle.European
    else:
        cpp_style = optionspulse.OptionStyle.American
    s_values = np.linspace(request.S-(request.S//4),request.S+(request.S//4),100)
    result = []
    for i in s_values:
        delta_res = optionspulse.delta(i,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style)
        gamma_res = optionspulse.gamma(i,request.K,request.r,request.sigma,request.T,cpp_style)
        vega_res = optionspulse.vega(i,request.K,request.r,request.sigma,request.T,cpp_style)
        theta_res = optionspulse.theta(i,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style)
        rho_res = optionspulse.rho(i,request.K,request.r,request.sigma,request.T,cpp_type,cpp_style) 
        result.append(GraphResponse(S=i,delta=delta_res,gamma=gamma_res,vega=vega_res,theta=theta_res,rho=rho_res))
    return result

@app.post("/pnl")
def pnl(request: pnlRequest):
    if request.optionType == OptionType.Call:
        cpp_type = optionspulse.OptionType.Call
    else:
        cpp_type = optionspulse.OptionType.Put
    
    if request.optionStyle == OptionStyle.European:
        cpp_style = optionspulse.OptionStyle.European
    else:
        cpp_style = optionspulse.OptionStyle.American
    s_values = np.linspace(request.S-(request.S//4),request.S+(request.S//4),100)
    sigma_values = np.linspace(request.sigma*1.5,request.sigma*0.5,20)
    result = []
    for i in sigma_values:
        row = []
        for j in s_values:
            pnl = optionspulse.price(j,request.K,
                                    request.r,i,request.T,
                                    cpp_type,
                                    cpp_style) - request.price
            row.append(pnl)
        result.append(row)
    return pnlResponse(S=list(s_values), sigma=list(sigma_values), pnl_grid=result)

@app.post("/implied_vol")
def implied_vol(request: volRequest):
    if request.optionType == OptionType.Call:
        cpp_type = optionspulse.OptionType.Call
    else:
        cpp_type = optionspulse.OptionType.Put
    
    if request.optionStyle == OptionStyle.European:
        cpp_style = optionspulse.OptionStyle.European
    else:
        cpp_style = optionspulse.OptionStyle.American
    result = optionspulse.volatility(request.S, request.K,request.r,request.T,request.price,cpp_type,cpp_style)
    return volResponse(sigma=result)

@app.post("/vol_smile")
def vol_smile(request: volSmileRequest):
    if request.optionType == OptionType.Call:
        cpp_type = optionspulse.OptionType.Call
    else:
        cpp_type = optionspulse.OptionType.Put
    if request.optionStyle == OptionStyle.European:
        cpp_style = optionspulse.OptionStyle.European
    else:
        cpp_style = optionspulse.OptionStyle.American
        
    target = date.today() + timedelta(days=int(request.T*365))
    expiries = yf.Ticker(request.ticker).options
    closest_expiry = min(expiries, key=lambda e: abs((datetime.strptime(e, "%Y-%m-%d").date()-target).days))
    T = (datetime.strptime(closest_expiry, "%Y-%m-%d").date() - date.today()).days / 365 
    chain = yf.Ticker(request.ticker).option_chain(closest_expiry)
    contracts = chain.calls if request.optionType == OptionType.Call else chain.puts
    vol_list = []
    K_list = []
    for i, row in contracts.iterrows():
        strike = row["strike"]
        lastPrice = row["lastPrice"]
        if lastPrice == 0:
            continue
        try:
            vol = optionspulse.volatility(request.S, strike,request.r,T,lastPrice,cpp_type,cpp_style)
            if vol > 5 or vol < 0:
                continue
            vol_list.append(vol)
            K_list.append(strike)
        except ValueError:
            continue
        

    return volSmileResponse(vol_list=vol_list,K_list=K_list)
