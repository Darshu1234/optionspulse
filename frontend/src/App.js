import React, { useState, useEffect } from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import Plot from 'react-plotly.js';

const GREEK_COLORS = {
  delta: '#22C55E',
  gamma: '#3B82F6',
  vega: '#EAB308',
  theta: '#EF4444',
  rho: '#A855F7',
};

const TOOLTIP_STYLE = {
  contentStyle: {
    background: '#1E293B',
    border: '1px solid #334155',
    borderRadius: 8,
    fontSize: 12,
    fontFamily: 'Fira Code, monospace',
  },
  labelStyle: { color: '#94A3B8' },
};

const AXIS_TICK = { fill: '#94A3B8', fontSize: 10 };

function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [S, setS] = useState("");
  const [K, setK] = useState(330.0);
  const [r, setR] = useState(0.05);
  const [sigma, setSigma] = useState("");
  const [T, setT] = useState(1.0);
  const [OptionType, setType] = useState("Call");
  const [OptionStyle, setStyle] = useState("European");
  const [price, setPrice] = useState(null);
  const [greeks, setGreeks] = useState(null);
  const [greeksGraph, setGreeksGraph] = useState(null);
  const [pnlHeatMap, setHeatMap] = useState(null);
  const [volSmile, setVolSmile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { fetchQuote(); }, []);

  async function fetchQuote() {
    const response = await fetch("http://localhost:8000/quote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ticker }),
    });
    const data = await response.json();
    setS(data.S);
    setSigma(data.sigma);
  }

  async function fetchGraph() {
    const response = await fetch("http://localhost:8000/greekgraphs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ S, K, r, sigma, T, optionType: OptionType, optionStyle: OptionStyle }),
    });
    const data = await response.json();
    setGreeksGraph(data);
  }

  async function fetchPnl(priceValue) {
    const response = await fetch("http://localhost:8000/pnl", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ S, K, r, sigma, T, optionType: OptionType, optionStyle: OptionStyle, price: priceValue }),
    });
    const data = await response.json();
    setHeatMap(data);
  }

  async function fetchVolSmile() {
    const response = await fetch("http://localhost:8000/vol_smile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ S, r, T, optionType: OptionType, optionStyle: OptionStyle, ticker }),
    });
    const data = await response.json();
    setVolSmile(data);
  }

  async function handleSubmit() {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/price", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ S, K, r, sigma, T, optionType: OptionType, optionStyle: OptionStyle, ticker }),
      });
      const data = await response.json();
      setPrice(data);

      const response1 = await fetch("http://localhost:8000/greeks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ S, K, r, sigma, T, optionType: OptionType, optionStyle: OptionStyle, ticker }),
      });
      const data1 = await response1.json();
      setGreeks(data1);

      fetchGraph();
      fetchPnl(data);
      fetchVolSmile();
    } finally {
      setLoading(false);
    }
  }

  const smileData = volSmile
    ? volSmile.K_list.map((k, i) => ({ K: k, vol: volSmile.vol_list[i] }))
    : [];

  return (
    <div>
      <header className="header">
        <h1 className="logo">Greek<span className="logo-accent">Desk</span></h1>
      </header>

      <div className="main-layout">
        {/* Sidebar */}
        <aside className="input-panel">
          <div className="section-label">Ticker</div>
          <div className="ticker-row">
            <input
              className="input-field"
              type="text"
              value={ticker}
              onChange={e => setTicker(e.target.value)}
              placeholder="AAPL"
            />
            <button className="btn btn-ghost" onClick={fetchQuote}>Quote</button>
          </div>

          <div className="divider" />

          <div className="section-label">Parameters</div>

          <div className="input-row">
            <div className="input-group">
              <label className="input-label">Spot (S)</label>
              <input className="input-field" type="number" value={S} onChange={e => setS(e.target.value)} />
            </div>
            <div className="input-group">
              <label className="input-label">Strike (K)</label>
              <input className="input-field" type="number" value={K} onChange={e => setK(e.target.value)} />
            </div>
          </div>

          <div className="input-row">
            <div className="input-group">
              <label className="input-label">Rate (r)</label>
              <input className="input-field" type="number" value={r} onChange={e => setR(e.target.value)} />
            </div>
            <div className="input-group">
              <label className="input-label">Vol (σ)</label>
              <input className="input-field" type="number" value={sigma} onChange={e => setSigma(e.target.value)} />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Expiry (T, years)</label>
            <input className="input-field" type="number" value={T} onChange={e => setT(e.target.value)} />
          </div>

          <div className="divider" />

          <div className="section-label">Contract</div>

          <div className="input-row">
            <div className="input-group">
              <label className="input-label">Type</label>
              <select className="input-field" value={OptionType} onChange={e => setType(e.target.value)}>
                <option value="Call">Call</option>
                <option value="Put">Put</option>
              </select>
            </div>
            <div className="input-group">
              <label className="input-label">Style</label>
              <select className="input-field" value={OptionStyle} onChange={e => setStyle(e.target.value)}>
                <option value="European">European</option>
                <option value="American">American</option>
              </select>
            </div>
          </div>

          <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Calculating...' : 'Calculate'}
          </button>
        </aside>

        {/* Main output */}
        <main className="output-panel">
          {price !== null && (
            <div className="price-card">
              <div className="price-value">${Number(price).toFixed(4)}</div>
              <div className="price-meta">Theoretical Price · {OptionType} · {OptionStyle}</div>
            </div>
          )}

          {greeks !== null && (
            <div className="greeks-card">
              <div className="section-label">Greeks</div>
              <div className="greeks-grid">
                {Object.entries(greeks).map(([name, val]) => (
                  <div className="greek-item" key={name}>
                    <div className="greek-name">{name}</div>
                    <div className="greek-value" style={{ color: GREEK_COLORS[name] }}>
                      {Number(val).toFixed(4)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {greeksGraph !== null && (
            <>
              <div className="charts-section-label">Greeks vs Spot</div>
              <div className="charts-grid">
                {['delta', 'gamma', 'vega', 'theta', 'rho'].map(greek => (
                  <div className="chart-card" key={greek}>
                    <div className="chart-title" style={{ color: GREEK_COLORS[greek] }}>
                      {greek[0].toUpperCase() + greek.slice(1)}
                    </div>
                    <ResponsiveContainer width="100%" height={160}>
                      <LineChart data={greeksGraph}>
                        <XAxis dataKey="S" tick={AXIS_TICK} tickLine={false} axisLine={false} />
                        <YAxis tick={AXIS_TICK} tickLine={false} axisLine={false} width={48} />
                        <Tooltip {...TOOLTIP_STYLE} itemStyle={{ color: GREEK_COLORS[greek] }} />
                        <Line
                          type="monotone"
                          dataKey={greek}
                          stroke={GREEK_COLORS[greek]}
                          dot={false}
                          strokeWidth={2}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ))}
              </div>
            </>
          )}

          {pnlHeatMap !== null && (
            <div className="chart-card-full">
              <div className="chart-title">P&amp;L Heatmap · Spot × Volatility</div>
              <Plot
                data={[{
                  type: 'heatmap',
                  z: pnlHeatMap.pnl_grid,
                  x: pnlHeatMap.S,
                  y: pnlHeatMap.sigma,
                  colorscale: 'RdYlGn',
                }]}
                layout={{
                  paper_bgcolor: 'transparent',
                  plot_bgcolor: 'transparent',
                  font: { color: '#94A3B8', family: 'Fira Sans, sans-serif', size: 11 },
                  xaxis: { title: 'Spot (S)', gridcolor: '#334155', color: '#94A3B8', zerolinecolor: '#334155' },
                  yaxis: { title: 'σ', gridcolor: '#334155', color: '#94A3B8', zerolinecolor: '#334155' },
                  margin: { t: 10, b: 50, l: 60, r: 20 },
                  height: 320,
                }}
                style={{ width: '100%' }}
                config={{ responsive: true, displayModeBar: false }}
              />
            </div>
          )}

          {volSmile !== null && smileData.length > 0 && (
            <div className="chart-card-full">
              <div className="chart-title">Volatility Smile</div>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={smileData}>
                  <XAxis
                    dataKey="K"
                    tick={AXIS_TICK}
                    tickLine={false}
                    axisLine={false}
                    label={{ value: 'Strike (K)', position: 'insideBottom', offset: -2, fill: '#94A3B8', fontSize: 11 }}
                  />
                  <YAxis
                    tick={AXIS_TICK}
                    tickLine={false}
                    axisLine={false}
                    width={48}
                    label={{ value: 'IV', angle: -90, position: 'insideLeft', fill: '#94A3B8', fontSize: 11 }}
                  />
                  <Tooltip
                    {...TOOLTIP_STYLE}
                    itemStyle={{ color: '#22C55E' }}
                    formatter={v => [Number(v).toFixed(4), 'IV']}
                  />
                  <Line type="monotone" dataKey="vol" stroke="#22C55E" dot={false} strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
