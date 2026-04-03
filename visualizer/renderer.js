/**
 * Canvas renderer for state space trajectories.
 * Supports H-M, H-E, time series, and phase portrait views.
 */

class Renderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.view = 'hm'; // 'hm', 'he', 'time', 'phase'
    this.dpr = window.devicePixelRatio || 1;
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width * this.dpr;
    this.canvas.height = rect.height * this.dpr;
    this.canvas.style.width = rect.width + 'px';
    this.canvas.style.height = rect.height + 'px';
    this.w = rect.width;
    this.h = rect.height;
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
  }

  setView(view) {
    this.view = view;
  }

  render(history, events, currentIdx, params, heatmaps) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.w, this.h);
    this._heatmaps = heatmaps || null;

    switch (this.view) {
      case 'hm': this.renderStateSpace(history, events, currentIdx, 'H', 'M', params); break;
      case 'he': this.renderStateSpace(history, events, currentIdx, 'H', 'E', params); break;
      case 'time': this.renderTimeSeries(history, events, currentIdx); break;
      case 'hc': this.renderHCPhasePortrait(history, events, currentIdx, params); break;
      case 'phase': this.renderPhasePortrait(history, events, currentIdx, params); break;
    }
  }

  renderStateSpace(history, events, currentIdx, xKey, yKey, params) {
    const ctx = this.ctx;
    const pad = { left: 60, right: 30, top: 30, bottom: 50 };
    const pw = this.w - pad.left - pad.right;
    const ph = this.h - pad.top - pad.bottom;

    // Axis ranges
    const xRange = xKey === 'H' ? [0, 1] : [-2, 3];
    const yRange = yKey === 'M' ? [0, 4] : yKey === 'E' ? [-3, 4] : [0, 1];

    const toX = v => pad.left + (v - xRange[0]) / (xRange[1] - xRange[0]) * pw;
    const toY = v => pad.top + ph - (v - yRange[0]) / (yRange[1] - yRange[0]) * ph;

    // Heatmap underlay (before grid so grid draws on top)
    if (this._heatmaps && this._heatmaps.loaded && this._heatmaps.activeMetric !== 'none') {
      this._heatmaps.renderUnderlay(ctx, xKey, yKey, toX, toY, pw, ph, pad.left, pad.top);
      this._heatmaps.drawLegend(ctx, pad.left + pw - 120, pad.top + 6, 100, 8);
    }

    // Background grid
    ctx.strokeStyle = '#151520';
    ctx.lineWidth = 1;
    for (let x = xRange[0]; x <= xRange[1]; x += (xRange[1] - xRange[0]) / 10) {
      ctx.beginPath(); ctx.moveTo(toX(x), pad.top); ctx.lineTo(toX(x), pad.top + ph); ctx.stroke();
    }
    for (let y = yRange[0]; y <= yRange[1]; y += (yRange[1] - yRange[0]) / 8) {
      ctx.beginPath(); ctx.moveTo(pad.left, toY(y)); ctx.lineTo(pad.left + pw, toY(y)); ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#2a2a3a';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + ph); ctx.lineTo(pad.left + pw, pad.top + ph); ctx.stroke();

    // Axis labels
    ctx.fillStyle = '#556';
    ctx.font = '11px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(xKey, pad.left + pw / 2, this.h - 8);
    ctx.save();
    ctx.translate(14, pad.top + ph / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(yKey, 0, 0);
    ctx.restore();

    // Tick labels
    ctx.font = '9px monospace';
    ctx.fillStyle = '#445';
    ctx.textAlign = 'center';
    for (let x = xRange[0]; x <= xRange[1]; x += (xRange[1] - xRange[0]) / 5) {
      ctx.fillText(x.toFixed(1), toX(x), pad.top + ph + 14);
    }
    ctx.textAlign = 'right';
    for (let y = yRange[0]; y <= yRange[1]; y += (yRange[1] - yRange[0]) / 4) {
      ctx.fillText(y.toFixed(1), pad.left - 6, toY(y) + 3);
    }

    // Draw behavioral threshold line (theta = C * (1 - H)) if showing H-M
    if (xKey === 'H' && yKey === 'M' && params) {
      ctx.strokeStyle = '#333344';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (let h = 0; h <= 1; h += 0.01) {
        const th = params.C * (1 - h);
        const px = toX(h);
        const py = toY(th);
        if (h === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.setLineDash([]);
      // Label
      ctx.fillStyle = '#445';
      ctx.font = '9px system-ui';
      ctx.fillText('threshold theta', toX(0.5), toY(params.C * 0.5) - 6);
    }

    // Draw trajectory
    if (history.length < 2) return;

    const n = Math.min(history.length, currentIdx + 1);

    // Trail with fade
    for (let i = 1; i < n; i++) {
      const alpha = Math.max(0.05, (i / n) * 0.8);
      const x0 = toX(history[i-1][xKey]);
      const y0 = toY(history[i-1][yKey]);
      const x1 = toX(history[i][xKey]);
      const y1 = toY(history[i][yKey]);

      // Color by B value
      const b = history[i].B;
      const r = Math.round(80 + (1 - b) * 150);
      const g = Math.round(80 + b * 150);
      ctx.strokeStyle = `rgba(${r}, ${g}, 120, ${alpha})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
    }

    // Event markers
    for (const ev of events) {
      const idx = Math.round(ev.time / 0.1);
      if (idx < n && idx < history.length) {
        const px = toX(history[idx][xKey]);
        const py = toY(history[idx][yKey]);
        ctx.fillStyle = '#cc8844';
        ctx.beginPath();
        ctx.arc(px, py, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#cc8844';
        ctx.font = '9px system-ui';
        ctx.textAlign = 'left';
        ctx.fillText(ev.label, px + 8, py - 4);
      }
    }

    // Current position
    if (currentIdx < history.length) {
      const cur = history[currentIdx];
      const px = toX(cur[xKey]);
      const py = toY(cur[yKey]);

      // Glow
      const grad = ctx.createRadialGradient(px, py, 0, px, py, 15);
      grad.addColorStop(0, 'rgba(100, 200, 255, 0.4)');
      grad.addColorStop(1, 'rgba(100, 200, 255, 0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(px, py, 15, 0, Math.PI * 2);
      ctx.fill();

      // Dot
      ctx.fillStyle = '#88ddff';
      ctx.beginPath();
      ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // Start marker
    if (history.length > 0) {
      const start = history[0];
      ctx.strokeStyle = '#668';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(toX(start[xKey]), toY(start[yKey]), 6, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = '#668';
      ctx.font = '9px system-ui';
      ctx.fillText('start', toX(start[xKey]) + 10, toY(start[yKey]) + 3);
    }
  }

  renderTimeSeries(history, events, currentIdx) {
    const ctx = this.ctx;
    const pad = { left: 50, right: 20, top: 20, bottom: 40 };
    const pw = this.w - pad.left - pad.right;
    const ph = this.h - pad.top - pad.bottom;
    const n = history.length;
    if (n < 2) return;

    const maxT = history[n - 1].t;
    const toX = t => pad.left + (t / maxT) * pw;

    const variables = [
      { key: 'H', color: '#44cc88', range: [0, 1] },
      { key: 'M', color: '#ff8844', range: [0, 4] },
      { key: 'E', color: '#cc4488', range: [-3, 4] },
      { key: 'I', color: '#8844cc', range: [0, 1] },
      { key: 'C', color: '#aacc44', range: [0, 1] },
      { key: 'B', color: '#44aacc', range: [0, 1] },
    ];

    // Background
    ctx.strokeStyle = '#151520';
    ctx.lineWidth = 1;
    for (let t = 0; t <= maxT; t += maxT / 10) {
      ctx.beginPath(); ctx.moveTo(toX(t), pad.top); ctx.lineTo(toX(t), pad.top + ph); ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#2a2a3a';
    ctx.beginPath(); ctx.moveTo(pad.left, pad.top + ph); ctx.lineTo(pad.left + pw, pad.top + ph); ctx.stroke();

    // Time label
    ctx.fillStyle = '#556';
    ctx.font = '11px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Days', pad.left + pw / 2, this.h - 8);

    // Ticks
    ctx.font = '9px monospace';
    ctx.fillStyle = '#445';
    for (let t = 0; t <= maxT; t += Math.max(1, Math.round(maxT / 8))) {
      ctx.fillText(Math.round(t) + '', toX(t), pad.top + ph + 14);
    }

    // Draw each variable
    for (const v of variables) {
      const toY = val => pad.top + ph - ((val - v.range[0]) / (v.range[1] - v.range[0])) * ph;

      ctx.strokeStyle = v.color;
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = 0.8;
      ctx.beginPath();
      for (let i = 0; i < Math.min(n, currentIdx + 1); i++) {
        const px = toX(history[i].t);
        const py = Math.max(pad.top, Math.min(pad.top + ph, toY(history[i][v.key])));
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.globalAlpha = 1;
    }

    // Event markers
    for (const ev of events) {
      const px = toX(ev.time);
      if (px >= pad.left && px <= pad.left + pw) {
        ctx.strokeStyle = 'rgba(200, 140, 60, 0.5)';
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(px, pad.top); ctx.lineTo(px, pad.top + ph); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#cc8844';
        ctx.font = '8px system-ui';
        ctx.save();
        ctx.translate(px + 3, pad.top + 10);
        ctx.rotate(-Math.PI / 6);
        ctx.fillText(ev.label, 0, 0);
        ctx.restore();
      }
    }

    // Current time marker
    if (currentIdx < n) {
      const px = toX(history[currentIdx].t);
      ctx.strokeStyle = 'rgba(140, 200, 255, 0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(px, pad.top); ctx.lineTo(px, pad.top + ph); ctx.stroke();
    }
  }

  renderHCPhasePortrait(history, events, currentIdx, params) {
   try {
    const ctx = this.ctx;
    const pad = { left: 60, right: 30, top: 30, bottom: 50 };
    const pw = this.w - pad.left - pad.right;
    const ph = this.h - pad.top - pad.bottom;
    if (pw <= 0 || ph <= 0) return;

    const toX = h => pad.left + h * pw;
    const toY = c => pad.top + ph - c * ph;

    // Heatmap underlay (if active, replaces region shading)
    if (this._heatmaps && this._heatmaps.loaded && this._heatmaps.activeMetric !== 'none') {
      this._heatmaps.renderUnderlay(ctx, 'H', 'C', toX, toY, pw, ph, pad.left, pad.top);
      this._heatmaps.drawLegend(ctx, pad.left + pw - 120, pad.top + 6, 100, 8);
    } else {
    // --- Region shading (drawn first, behind everything) ---
    // Stable habit region: lower-right triangle
    ctx.fillStyle = 'rgba(40, 120, 70, 0.08)';
    ctx.beginPath();
    ctx.moveTo(toX(0.4), toY(0)); ctx.lineTo(toX(1), toY(0));
    ctx.lineTo(toX(1), toY(0.6)); ctx.lineTo(toX(0.4), toY(0));
    ctx.fill();

    // Complexity trap region: upper-left
    ctx.fillStyle = 'rgba(140, 40, 60, 0.08)';
    ctx.beginPath();
    ctx.moveTo(toX(0), toY(0.55)); ctx.lineTo(toX(0), toY(1));
    ctx.lineTo(toX(0.35), toY(1)); ctx.lineTo(toX(0), toY(0.55));
    ctx.fill();

    // Sedentary region: lower-left
    ctx.fillStyle = 'rgba(100, 40, 40, 0.06)';
    ctx.beginPath();
    ctx.moveTo(toX(0), toY(0)); ctx.lineTo(toX(0.3), toY(0));
    ctx.lineTo(toX(0), toY(0.45)); ctx.lineTo(toX(0), toY(0));
    ctx.fill();

    // Progressive overload zone: band along the C-equilibrium curve
    ctx.fillStyle = 'rgba(60, 90, 130, 0.06)';
    ctx.beginPath();
    for (let h = 0.3; h <= 1; h += 0.01) {
      const ceq = 0.1 + 0.85 * h * 0.7;
      ctx.lineTo(toX(h), toY(Math.min(1, ceq + 0.1)));
    }
    for (let h = 1; h >= 0.3; h -= 0.01) {
      const ceq = 0.1 + 0.85 * h * 0.7;
      ctx.lineTo(toX(h), toY(Math.max(0, ceq - 0.1)));
    }
    ctx.closePath();
    ctx.fill();
    } // end else (no heatmap)

    // Grid
    ctx.strokeStyle = '#1a1a2a';
    ctx.lineWidth = 1;
    for (let x = 0; x <= 1; x += 0.1) {
      ctx.beginPath(); ctx.moveTo(toX(x), pad.top); ctx.lineTo(toX(x), pad.top + ph); ctx.stroke();
    }
    for (let y = 0; y <= 1; y += 0.1) {
      ctx.beginPath(); ctx.moveTo(pad.left, toY(y)); ctx.lineTo(pad.left + pw, toY(y)); ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#2a2a3a';
    ctx.beginPath(); ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + ph); ctx.lineTo(pad.left + pw, pad.top + ph); ctx.stroke();
    ctx.fillStyle = '#778'; ctx.font = '11px system-ui'; ctx.textAlign = 'center';
    ctx.fillText('H (Habit Strength)', pad.left + pw / 2, this.h - 8);
    ctx.save(); ctx.translate(14, pad.top + ph / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('C (Behavioral Complexity)', 0, 0); ctx.restore();

    // Tick labels
    ctx.font = '9px monospace'; ctx.fillStyle = '#445'; ctx.textAlign = 'center';
    for (let x = 0; x <= 1; x += 0.2) ctx.fillText(x.toFixed(1), toX(x), pad.top + ph + 14);
    ctx.textAlign = 'right';
    for (let y = 0; y <= 1; y += 0.2) ctx.fillText(y.toFixed(1), pad.left - 6, toY(y) + 3);

    // C equilibrium curve (I=0) -- the key structural line
    ctx.setLineDash([6, 4]);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = 'rgba(68, 136, 204, 0.6)';
    ctx.beginPath();
    for (let h = 0; h <= 1; h += 0.01) {
      const ceq = 0.1 + 0.85 * h * 0.7;
      if (h === 0) ctx.moveTo(toX(h), toY(ceq)); else ctx.lineTo(toX(h), toY(Math.min(1, ceq)));
    }
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#4488cc'; ctx.font = '9px system-ui'; ctx.textAlign = 'left';
    ctx.fillText('C equilibrium', toX(0.78), toY(0.1 + 0.85 * 0.78 * 0.7) - 8);
    ctx.fillStyle = '#4488cc88'; ctx.font = '8px system-ui';
    ctx.fillText('(sustainable complexity)', toX(0.78), toY(0.1 + 0.85 * 0.78 * 0.7) + 4);

    // Background trajectories (cached)
    const pKey = params ? (params.C + '|' + params.alpha_H + '|' + params.beta_M + '|' + params.lambda) : '';
    if (!this._hcCache || this._hcCacheKey !== pKey) {
      this._hcCache = this._computeHCTrajectories(params || {});
      this._hcCacheKey = pKey;
    }
    for (const t of this._hcCache) {
      const col = t.outcome === 'habit' ? 'rgba(68,204,136,' : 'rgba(180,60,80,';
      ctx.strokeStyle = col + '0.22)';
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      for (let i = 0; i < t.trail.length; i++) {
        const px = toX(t.trail[i].H); const py = toY(t.trail[i].C);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      // Start dot
      ctx.fillStyle = col + '0.45)';
      ctx.beginPath(); ctx.arc(toX(t.trail[0].H), toY(t.trail[0].C), 2, 0, Math.PI * 2); ctx.fill();
    }

    // Region labels
    ctx.globalAlpha = 0.8;
    ctx.font = 'bold 12px system-ui'; ctx.textAlign = 'center';

    ctx.fillStyle = '#44cc88';
    ctx.fillText('STABLE HABIT', toX(0.78), toY(0.18));
    ctx.font = '9px system-ui'; ctx.fillStyle = '#44cc8899';
    ctx.fillText('high H, matched C', toX(0.78), toY(0.18) + 13);

    ctx.font = 'bold 11px system-ui'; ctx.fillStyle = '#cc4488';
    ctx.fillText('COMPLEXITY', toX(0.12), toY(0.88));
    ctx.fillText('TRAP', toX(0.12), toY(0.88) + 14);
    ctx.font = '8px system-ui'; ctx.fillStyle = '#cc448888';
    ctx.fillText('C too high for H', toX(0.12), toY(0.88) + 26);

    ctx.font = 'bold 10px system-ui'; ctx.fillStyle = '#aa5555';
    ctx.fillText('SEDENTARY', toX(0.10), toY(0.25));
    ctx.font = '8px system-ui'; ctx.fillStyle = '#aa555588';
    ctx.fillText('low H, low C', toX(0.10), toY(0.25) + 12);

    ctx.font = '10px system-ui'; ctx.fillStyle = '#6699bb';
    ctx.fillText('progressive overload zone', toX(0.58), toY(0.52));

    ctx.globalAlpha = 1;

    // Draw the current trajectory
    if (history.length > 1) {
      const n = Math.min(history.length, currentIdx + 1);
      for (let i = 1; i < n; i++) {
        const alpha = Math.max(0.15, (i / n) * 0.9);
        const ci = history[i].C !== undefined ? history[i].C : (params ? params.C : 0.5);
        const cPrev = history[i-1].C !== undefined ? history[i-1].C : ci;
        ctx.strokeStyle = `rgba(136, 220, 255, ${alpha})`;
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(toX(history[i-1].H), toY(cPrev));
        ctx.lineTo(toX(history[i].H), toY(ci));
        ctx.stroke();
      }

      // Current position glow
      if (currentIdx < history.length) {
        const cur = history[currentIdx];
        const cc = cur.C !== undefined ? cur.C : (params ? params.C : 0.5);
        const px = toX(cur.H); const py = toY(cc);
        const grad = ctx.createRadialGradient(px, py, 0, px, py, 14);
        grad.addColorStop(0, 'rgba(100, 200, 255, 0.5)');
        grad.addColorStop(1, 'rgba(100, 200, 255, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(px, py, 14, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#88ddff';
        ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill();
      }

      // Start marker
      const s0 = history[0];
      const sc = s0.C !== undefined ? s0.C : (params ? params.C : 0.5);
      ctx.strokeStyle = '#889'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(toX(s0.H), toY(sc), 6, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = '#889'; ctx.font = '9px system-ui'; ctx.textAlign = 'left';
      ctx.fillText('start', toX(s0.H) + 9, toY(sc) + 3);
    }

    // Event markers
    for (const ev of events) {
      const idx = Math.round(ev.time / 0.1);
      if (idx < Math.min(history.length, currentIdx + 1)) {
        const h = history[idx];
        const ec = h.C !== undefined ? h.C : (params ? params.C : 0.5);
        ctx.fillStyle = '#cc8844';
        ctx.beginPath(); ctx.arc(toX(h.H), toY(ec), 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#cc884499'; ctx.font = '8px system-ui'; ctx.textAlign = 'left';
        ctx.fillText(ev.label, toX(h.H) + 6, toY(ec) - 4);
      }
    }
   } catch(e) {
    this.ctx.fillStyle = '#ff4444'; this.ctx.font = '12px monospace';
    this.ctx.fillText('H-C error: ' + e.message, 20, 30);
   }
  }

  _computeHCTrajectories(params) {
    const p = { ...DEFAULT_PARAMS, ...params, sigma_noise: 0 };
    const dyn = new HabitDynamics(p);
    const trails = [];
    for (let h0 = 0; h0 <= 0.8; h0 += 0.1) {
      for (let c0 = 0.1; c0 <= 0.95; c0 += 0.1) {
        let state = { H: Math.max(0.02, h0), M: 1.0, E: 0.3, I: 0, C: c0,
                       B: 0, F: 0, dE_prev: 0, injured: false, stress: 0, ii: 0, social_support: 0 };
        const trail = [{ H: state.H, C: state.C }];
        for (let t = 0; t < 300; t++) {
          state = dyn.step(state, 1, 0, 0);
          // Guard against NaN
          if (isNaN(state.H) || isNaN(state.C)) break;
          if (t % 4 === 0) trail.push({ H: state.H, C: state.C });
        }
        const hf = trail[trail.length - 1].H;
        trails.push({ trail, outcome: hf > 0.5 ? 'habit' : 'sedentary' });
      }
    }
    return trails;
  }

  renderPhasePortrait(history, events, currentIdx, params) {
    // Multi-trajectory H-M phase portrait
    const ctx = this.ctx;
    const pad = { left: 60, right: 30, top: 30, bottom: 50 };
    const pw = this.w - pad.left - pad.right;
    const ph = this.h - pad.top - pad.bottom;

    const toX = v => pad.left + v * pw;
    const toY = v => pad.top + ph - v / 4 * ph;

    // Grid
    ctx.strokeStyle = '#151520';
    ctx.lineWidth = 1;
    for (let x = 0; x <= 1; x += 0.1) {
      ctx.beginPath(); ctx.moveTo(toX(x), pad.top); ctx.lineTo(toX(x), pad.top + ph); ctx.stroke();
    }
    for (let y = 0; y <= 4; y += 0.5) {
      ctx.beginPath(); ctx.moveTo(pad.left, toY(y)); ctx.lineTo(pad.left + pw, toY(y)); ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#2a2a3a';
    ctx.beginPath(); ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + ph); ctx.lineTo(pad.left + pw, pad.top + ph); ctx.stroke();
    ctx.fillStyle = '#556';
    ctx.font = '11px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('H (Habit)', pad.left + pw / 2, this.h - 8);
    ctx.save();
    ctx.translate(14, pad.top + ph / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('M (Motivation)', 0, 0);
    ctx.restore();

    // Threshold line
    if (params) {
      ctx.strokeStyle = '#333344';
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (let h = 0; h <= 1; h += 0.01) {
        ctx.lineTo(toX(h), toY(params.C * (1 - h)));
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Run mini simulations from a grid of ICs
    if (!params) return;
    const dyn = new HabitDynamics(params);
    const ics = [];
    for (let h = 0; h <= 0.8; h += 0.2) {
      for (let m = 0.5; m <= 3.5; m += 0.75) {
        ics.push({ h, m });
      }
    }

    for (const ic of ics) {
      let state = { H: ic.h, M: ic.m, E: 0, I: 0, C: params.C, B: 0, F: 0, dE_prev: 0, injured: false, stress: 0, ii: 0, social_support: 0 };
      const trail = [{ H: state.H, M: state.M }];
      for (let t = 0; t < 200; t++) {
        state = dyn.step(state, 1, 0, 0);
        trail.push({ H: state.H, M: state.M });
      }

      // Determine outcome color
      const hFinal = trail[trail.length - 1].H;
      const color = hFinal > 0.5 ? 'rgba(68, 204, 136, 0.3)' : 'rgba(200, 80, 80, 0.3)';

      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let i = 0; i < trail.length; i++) {
        const px = toX(trail[i].H);
        const py = toY(trail[i].M);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Arrow at start
      ctx.fillStyle = color.replace('0.3', '0.6');
      ctx.beginPath();
      ctx.arc(toX(ic.h), toY(ic.m), 3, 0, Math.PI * 2);
      ctx.fill();
    }

    // Overlay the main trajectory
    if (history.length > 1) {
      const n = Math.min(history.length, currentIdx + 1);
      ctx.strokeStyle = '#88ddff';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let i = 0; i < n; i++) {
        const px = toX(history[i].H);
        const py = toY(history[i].M);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Current dot
      if (currentIdx < history.length) {
        ctx.fillStyle = '#88ddff';
        ctx.beginPath();
        ctx.arc(toX(history[currentIdx].H), toY(history[currentIdx].M), 5, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
}

window.Renderer = Renderer;
