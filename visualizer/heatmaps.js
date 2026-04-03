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
    this.dataCPU = null;    // Ground truth (CPU, lower resolution)
    this.dataGPU = null;    // High-res approximation (GPU, may have tiny numerical drift)
    this.data = null;       // Active data source
    this.source = 'cpu';    // 'cpu' or 'gpu'
    this.activeMetric = 'success';
    this.alpha = 0.25;
    this.imageCache = {};
    this.loading = false;
    this.loaded = false;
  }

  async load(cpuUrl, gpuUrl) {
    if (this.loading) return;
    this.loading = true;
    try {
      const [cpuResp, gpuResp] = await Promise.allSettled([
        fetch(cpuUrl).then(r => r.json()),
        gpuUrl ? fetch(gpuUrl).then(r => r.json()) : Promise.reject('no gpu url'),
      ]);
      if (cpuResp.status === 'fulfilled') {
        this.dataCPU = cpuResp.value;
        this.data = this.dataCPU;
        this.loaded = true;
        console.log('CPU heatmap:', this.dataCPU.n_points, 'points');
      }
      if (gpuResp.status === 'fulfilled') {
        this.dataGPU = gpuResp.value;
        console.log('GPU heatmap:', this.dataGPU.n_points, 'points (high-res approx)');
      }
    } catch (e) {
      console.warn('Could not load heatmap data:', e.message);
    }
    this.loading = false;
  }

  setSource(source) {
    if (source === 'gpu' && this.dataGPU) {
      this.data = this.dataGPU;
      this.source = 'gpu';
    } else {
      this.data = this.dataCPU;
      this.source = 'cpu';
    }
    this.imageCache = {}; // Clear cache on source change
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

    // Try both orderings since sweep uses list order, not alphabetical
    let key = `${v1}_${v2}`;
    let swapped = false;
    let hm = this.data.heatmaps[key];
    if (!hm) {
      key = `${v2}_${v1}`;
      swapped = true;
      hm = this.data.heatmaps[key];
    }
    if (!hm) return;

    const metric = hm.metrics[this.activeMetric];
    if (!metric) return;

    const cacheKey = `${key}_${this.activeMetric}_${pw}_${ph}`;
    if (!this.imageCache[cacheKey]) {
      const data = metric.data;
      const res = data.length;
      const cmap = COLORMAPS[METRIC_COLORMAPS[this.activeMetric] || 'viridis'];
      const vmin = metric.min;
      const vmax = metric.max;
      const range = vmax - vmin || 1;

      // Render at native resolution (small), then let canvas scale with smoothing
      const small = document.createElement('canvas');
      small.width = res;
      small.height = res;
      const sctx = small.getContext('2d');
      const imgData = sctx.createImageData(res, res);

      for (let i = 0; i < res; i++) {
        for (let j = 0; j < res; j++) {
          const val = swapped ? data[j][i] : data[i][j];
          const t = Math.max(0, Math.min(1, (val - vmin) / range));
          const [r, g, b] = cmap(t);
          // v1 on x (i), v2 on y (j inverted: row 0 = top = high v2)
          const row = swapped ? (res - 1 - i) : (res - 1 - j);
          const col = swapped ? j : i;
          const idx = (row * res + col) * 4;
          imgData.data[idx] = r;
          imgData.data[idx + 1] = g;
          imgData.data[idx + 2] = b;
          imgData.data[idx + 3] = 255;
        }
      }
      sctx.putImageData(imgData, 0, 0);

      // Scale up with bilinear interpolation
      const offscreen = document.createElement('canvas');
      offscreen.width = pw;
      offscreen.height = ph;
      const octx = offscreen.getContext('2d');
      octx.imageSmoothingEnabled = true;
      octx.imageSmoothingQuality = 'high';
      octx.drawImage(small, 0, 0, pw, ph);

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

    // Min/max from summary stats
    if (this.data.summary && this.data.summary[this.activeMetric]) {
      const s = this.data.summary[this.activeMetric];
      ctx.textAlign = 'left';
      ctx.fillText(s.min.toFixed(1), x, y + h + 10);
      ctx.textAlign = 'right';
      ctx.fillText(s.max.toFixed(1), x + w, y + h + 10);
    }
    // Source badge
    const srcLabel = this.source === 'gpu'
      ? `GPU ~${(this.data.n_points/1000).toFixed(0)}K pts`
      : `CPU ${(this.data.n_points/1000).toFixed(1)}K pts`;
    ctx.fillStyle = this.source === 'gpu' ? '#886633' : '#338866';
    ctx.font = '8px system-ui';
    ctx.textAlign = 'right';
    ctx.fillText(srcLabel, x + w, y - 12);
  }
}

window.HeatmapManager = HeatmapManager;
window.METRIC_LABELS = METRIC_LABELS;
