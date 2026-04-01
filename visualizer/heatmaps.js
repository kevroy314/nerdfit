/**
 * Heatmap underlay system.
 * Loads precomputed 2D metric heatmaps and renders them as colored grid underlays.
 * Each metric uses a distinct colormap.
 */

// Colormaps: functions that take [0,1] and return [r,g,b] in [0,255]
const COLORMAPS = {
  viridis: t => {
    // Simplified viridis
    const r = Math.round(68 + t * (253 - 68) * (1 - t) + t * t * 200 * (1 - t * 0.5));
    const g = Math.round(1 + t * 220);
    const b = Math.round(84 + (1 - t) * 170 - t * 60);
    return [Math.min(255, r), Math.min(255, g), Math.max(0, b)];
  },
  magma: t => {
    const r = Math.round(t * 250);
    const g = Math.round(t * t * 200);
    const b = Math.round(80 + t * 120 - t * t * 60);
    return [r, g, b];
  },
  inferno: t => {
    const r = Math.round(t * 230 + 20);
    const g = Math.round(t * t * 180);
    const b = Math.round(30 + (1 - t) * t * 300);
    return [Math.min(255, r), g, Math.min(255, b)];
  },
  plasma: t => {
    const r = Math.round(50 + t * 200);
    const g = Math.round(t * t * 220);
    const b = Math.round(140 - t * 100 + t * t * 80);
    return [r, g, Math.max(0, b)];
  },
  cividis: t => {
    const r = Math.round(0 + t * 220);
    const g = Math.round(30 + t * 190);
    const b = Math.round(80 + (1 - t) * 100);
    return [r, g, b];
  },
  coolwarm: t => {
    const r = Math.round(t < 0.5 ? 60 + t * 200 : 200 + (t - 0.5) * 110);
    const g = Math.round(80 + Math.sin(t * Math.PI) * 120);
    const b = Math.round(t < 0.5 ? 200 + (0.5 - t) * 110 : 200 - (t - 0.5) * 200);
    return [Math.min(255, r), Math.min(255, g), Math.max(0, Math.min(255, b))];
  },
};

// Metric -> colormap assignment
const METRIC_COLORMAPS = {
  success: 'viridis',
  cognitive_load: 'magma',
  net_activity: 'inferno',
  path_length: 'plasma',
  settling: 'cividis',
  time_to_habit: 'coolwarm',
};

const METRIC_LABELS = {
  success: 'Success Rate',
  cognitive_load: 'Cognitive Load (total)',
  net_activity: 'Net Activity (C*B total)',
  path_length: 'Path Length (state-space distance)',
  settling: 'Settling (lower = more stable)',
  time_to_habit: 'Time to Habit (days)',
};

class HeatmapManager {
  constructor() {
    this.data = null;
    this.activeMetric = 'success';
    this.alpha = 0.25; // Underlay opacity
    this.imageCache = {}; // Cache rendered ImageData per key
    this.loading = false;
    this.loaded = false;
  }

  async load(url) {
    if (this.loading || this.loaded) return;
    this.loading = true;
    try {
      const resp = await fetch(url);
      this.data = await resp.json();
      this.loaded = true;
      console.log('Heatmap data loaded:', this.data.n_points, 'points,',
                  Object.keys(this.data.heatmaps).length, 'planes');
    } catch (e) {
      console.warn('Could not load heatmap data:', e.message);
    }
    this.loading = false;
  }

  setMetric(metric) {
    this.activeMetric = metric;
  }

  setAlpha(a) {
    this.alpha = a;
  }

  /**
   * Render the heatmap underlay for a given plane (e.g., "H_M", "H_C").
   * ctx: canvas context
   * v1, v2: variable names (e.g., "H", "M")
   * toX, toY: coordinate transform functions
   * pw, ph: plot width/height in pixels
   * padLeft, padTop: plot padding
   */
  renderUnderlay(ctx, v1, v2, toX, toY, pw, ph, padLeft, padTop) {
    if (!this.loaded || !this.data) return;

    const key = v1 < v2 ? `${v1}_${v2}` : `${v2}_${v1}`;
    const swapped = v1 > v2; // If axes are swapped relative to data
    const hm = this.data.heatmaps[key];
    if (!hm) return;

    const metric = hm.metrics[this.activeMetric];
    if (!metric) return;

    const cacheKey = `${key}_${this.activeMetric}_${pw}_${ph}`;
    if (!this.imageCache[cacheKey]) {
      // Render to offscreen canvas
      const offscreen = document.createElement('canvas');
      offscreen.width = pw;
      offscreen.height = ph;
      const octx = offscreen.getContext('2d');

      const data = metric.data; // [res][res]
      const res = data.length;
      const cmap = COLORMAPS[METRIC_COLORMAPS[this.activeMetric] || 'viridis'];
      const vmin = metric.min;
      const vmax = metric.max;
      const range = vmax - vmin || 1;

      const cellW = pw / res;
      const cellH = ph / res;

      for (let i = 0; i < res; i++) {
        for (let j = 0; j < res; j++) {
          // data[i][j]: i = v1 axis, j = v2 axis
          const val = swapped ? data[j][i] : data[i][j];
          const t = Math.max(0, Math.min(1, (val - vmin) / range));
          const [r, g, b] = cmap(t);
          octx.fillStyle = `rgb(${r},${g},${b})`;
          // v1 on x-axis (i), v2 on y-axis (j, inverted)
          if (swapped) {
            octx.fillRect(j * cellW, ph - (i + 1) * cellH, cellW + 1, cellH + 1);
          } else {
            octx.fillRect(i * cellW, ph - (j + 1) * cellH, cellW + 1, cellH + 1);
          }
        }
      }

      this.imageCache[cacheKey] = offscreen;
    }

    ctx.globalAlpha = this.alpha;
    ctx.drawImage(this.imageCache[cacheKey], padLeft, padTop);
    ctx.globalAlpha = 1;
  }

  /**
   * Draw a small colorbar legend.
   */
  drawLegend(ctx, x, y, w, h) {
    if (!this.loaded || !this.data) return;

    const cmap = COLORMAPS[METRIC_COLORMAPS[this.activeMetric] || 'viridis'];
    const label = METRIC_LABELS[this.activeMetric] || this.activeMetric;

    // Draw gradient bar
    for (let i = 0; i < w; i++) {
      const t = i / w;
      const [r, g, b] = cmap(t);
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.fillRect(x + i, y, 1, h);
    }

    // Label
    ctx.fillStyle = '#889';
    ctx.font = '9px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(label, x + w / 2, y - 3);

    // Min/max labels
    const hmKey = Object.keys(this.data.heatmaps)[0];
    if (hmKey) {
      const metric = this.data.heatmaps[hmKey].metrics[this.activeMetric];
      if (metric) {
        ctx.textAlign = 'left';
        ctx.fillText(metric.min.toFixed(1), x, y + h + 10);
        ctx.textAlign = 'right';
        ctx.fillText(metric.max.toFixed(1), x + w, y + h + 10);
      }
    }
  }
}

window.HeatmapManager = HeatmapManager;
window.METRIC_LABELS = METRIC_LABELS;
