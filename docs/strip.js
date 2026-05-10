/**
 * Time-series strip renderer: compact sparklines below the main canvas.
 * Shows state variables as thin lines with vertical event markers.
 */

class StripRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.dpr = window.devicePixelRatio || 1;
    this.visible = {
      H: true, M: true, E: false, I: false, C: true, B: false,
      cogLoad: false, activity: false, cumCogLoad: false,
      cumActivity: false, cumPath: false, settling: false,
    };
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

  setVisible(key, val) {
    this.visible[key] = val;
  }

  render(history, events, currentIdx, t_end) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.w, this.h);
    if (history.length < 2) return;

    const pad = { left: 30, right: 10, top: 4, bottom: 14 };
    const pw = this.w - pad.left - pad.right;
    const ph = this.h - pad.top - pad.bottom;
    const maxT = t_end || history[history.length - 1].t || 730;
    const toX = t => pad.left + (t / maxT) * pw;
    const n = Math.min(history.length, currentIdx + 1);

    // Variables config: key, color, range [lo, hi]
    const vars = [
      { key: 'H', color: '#44cc88', range: [0, 1] },
      { key: 'M', color: '#ff8844', range: [0, 3] },
      { key: 'E', color: '#cc4488', range: [-2, 3] },
      { key: 'I', color: '#8844cc', range: [0, 1] },
      { key: 'C', color: '#aacc44', range: [0, 1] },
      { key: 'B', color: '#44aacc', range: [0, 1] },
      // Aggregate metrics (instantaneous)
      { key: 'cogLoad', color: '#ff6688', range: [0, 0.5] },
      { key: 'activity', color: '#66ffaa', range: [0, 0.8] },
      // Cumulative metrics (auto-ranged)
      { key: 'cumCogLoad', color: '#ff668866', range: 'auto' },
      { key: 'cumActivity', color: '#66ffaa66', range: 'auto' },
      { key: 'cumPath', color: '#ffaa6666', range: 'auto' },
      { key: 'settling', color: '#aa88ff', range: [0, 0.1] },
    ];

    // Event markers (vertical lines) -- draw first so lines go on top
    for (const ev of events) {
      if (ev.time > maxT) continue;
      const px = toX(ev.time);
      const evIdx = Math.round(ev.time / 0.1);
      if (evIdx >= n) continue;

      // Color by event type
      let col = '#cc884440';
      if (ev.type === 'stress' || ev.type === 'lapse') col = '#cc444460';
      else if (ev.type === 'social' || ev.type === 'shock' || ev.type === 'new_year') col = '#44cc8840';
      else if (ev.type === 'simplify') col = '#aacc4450';
      else if (ev.type === 'injury_start') col = '#cc666660';
      else if (ev.type === 'injury_end') col = '#66cc6640';

      ctx.strokeStyle = col;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(px, pad.top);
      ctx.lineTo(px, pad.top + ph);
      ctx.stroke();

      // Short label at top, rotated to avoid overlap
      ctx.fillStyle = col.replace(/[0-9a-f]{2}$/, 'aa');
      ctx.font = '7px system-ui';
      ctx.save();
      ctx.translate(px + 2, pad.top + 2);
      ctx.rotate(-0.3);
      // Truncate label to 12 chars
      const label = ev.label ? ev.label.substring(0, 14) : ev.type;
      ctx.fillText(label, 0, 0);
      ctx.restore();
    }

    // Draw sparklines
    // Downsample for performance
    const step = Math.max(1, Math.floor(n / (pw * 2)));

    for (const v of vars) {
      if (!this.visible[v.key]) continue;

      // Compute range
      let lo, hi;
      if (v.range === 'auto') {
        // Auto-range from data
        let vmin = Infinity, vmax = -Infinity;
        for (let i = 0; i < n; i += step) {
          const val = history[i][v.key];
          if (val !== undefined) { vmin = Math.min(vmin, val); vmax = Math.max(vmax, val); }
        }
        lo = Math.min(0, vmin);
        hi = Math.max(vmax, lo + 0.01);
      } else {
        [lo, hi] = v.range;
      }
      const toY = val => pad.top + ph - ((Math.min(Math.max(val, lo), hi) - lo) / (hi - lo)) * ph;

      ctx.strokeStyle = v.color;
      ctx.lineWidth = 1.2;
      ctx.globalAlpha = 0.8;
      ctx.beginPath();

      for (let i = 0; i < n; i += step) {
        const val = history[i][v.key];
        if (val === undefined) continue;
        const px = toX(history[i].t);
        const py = toY(val);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.globalAlpha = 1;
    }

    // Current time marker
    if (currentIdx < history.length) {
      const px = toX(history[currentIdx].t);
      ctx.strokeStyle = 'rgba(140, 200, 255, 0.4)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(px, pad.top);
      ctx.lineTo(px, pad.top + ph);
      ctx.stroke();
    }

    // Time axis labels
    ctx.fillStyle = '#445';
    ctx.font = '8px monospace';
    ctx.textAlign = 'center';
    const nTicks = Math.min(8, Math.floor(pw / 60));
    for (let i = 0; i <= nTicks; i++) {
      const t = (i / nTicks) * maxT;
      ctx.fillText(Math.round(t) + 'd', toX(t), this.h - 2);
    }

    // Left axis hint
    ctx.fillStyle = '#334';
    ctx.font = '7px system-ui';
    ctx.textAlign = 'right';
    ctx.fillText('1', pad.left - 3, pad.top + 6);
    ctx.fillText('0', pad.left - 3, pad.top + ph);
  }
}

window.StripRenderer = StripRenderer;
