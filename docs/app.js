/**
 * Main application controller.
 * Manages simulation state, UI interactions, and render loop.
 */

class App {
  constructor() {
    this.canvas = document.getElementById('main-canvas');
    this.renderer = new Renderer(this.canvas);
    this.stripCanvas = document.getElementById('strip-canvas');
    this.strip = this.stripCanvas ? new StripRenderer(this.stripCanvas) : null;
    this.heatmaps = new HeatmapManager();
    this.heatmaps.load('heatmap_data.json', 'heatmap_data_gpu.json');
    this.dynamics = new HabitDynamics();
    this.history = [];
    this.events = [];
    this.currentIdx = 0;
    this.playing = false;
    this.speed = 1;
    this.dt = 0.1; // simulation timestep (days)
    this.stepsPerFrame = 1;
    this.activePreset = null;
    this.t_end = 730;

    this.state = {
      H: 0.02, M: 1.0, E: 0, I: 0, C: 0.5,
      B: 0, F: 0, dE_prev: 0,
      injured: false, stress: 0, ii: 0, social_support: 0,
    };

    this.setupUI();
    this.loadPreset('bootstrap');
    this.renderLoop();
  }

  setupUI() {
    // Preset buttons
    const presetList = document.getElementById('preset-list');
    for (const [key, scenario] of Object.entries(SCENARIOS)) {
      const btn = document.createElement('div');
      btn.className = 'preset-btn';
      btn.dataset.key = key;
      btn.innerHTML = `${scenario.name}<span class="tag">${scenario.phenomena.join(', ')}</span>`;
      btn.addEventListener('click', () => this.loadPreset(key));
      presetList.appendChild(btn);
    }

    // Character buttons
    const clusterList = document.getElementById('cluster-list');
    const chars = (typeof CHARACTERS !== 'undefined') ? CHARACTERS : {};
    for (const [key, character] of Object.entries(chars)) {
      const btn = document.createElement('div');
      btn.className = 'preset-btn';
      btn.dataset.key = key;
      const nEvents = character.events ? character.events.length : 0;
      btn.innerHTML = `${character.name}<span class="tag">${nEvents} events over 2yr &mdash; ${character.description.substring(0, 50)}...</span>`;
      btn.addEventListener('click', () => this.loadCluster(key));
      clusterList.appendChild(btn);
    }
    if (Object.keys(chars).length === 0) {
      clusterList.innerHTML = '<div style="color:#666;font-size:10px;padding:4px">No characters loaded. Check console.</div>';
    }

    // View toggle
    document.querySelectorAll('.view-toggle .btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.view-toggle .btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.renderer.setView(btn.dataset.view);
      });
    });

    // Play/Pause/Reset
    document.getElementById('btn-play').addEventListener('click', () => this.play());
    document.getElementById('btn-pause').addEventListener('click', () => this.pause());
    document.getElementById('btn-reset').addEventListener('click', () => this.reset());

    // Speed
    document.getElementById('sim-speed').addEventListener('change', e => {
      this.speed = parseFloat(e.target.value);
    });

    // Initial condition sliders
    this.setupSlider('ic-h', 'ic-h-val', v => { this.state.H = v; this.reset(); });
    this.setupSlider('ic-m', 'ic-m-val', v => { this.state.M = v; this.reset(); });
    this.setupSlider('ic-e', 'ic-e-val', v => { this.state.E = v; this.reset(); });
    this.setupSlider('ic-i', 'ic-i-val', v => { this.state.I = v; this.reset(); });

    // Parameter sliders
    this.setupSlider('p-c', 'p-c-val', v => this.dynamics.updateParams({ C: v }));
    this.setupSlider('p-ah', 'p-ah-val', v => this.dynamics.updateParams({ alpha_H: v }));
    this.setupSlider('p-bm', 'p-bm-val', v => this.dynamics.updateParams({ beta_M: v }));
    this.setupSlider('p-g', 'p-g-val', v => this.dynamics.updateParams({ gamma: v }));
    this.setupSlider('p-l', 'p-l-val', v => this.dynamics.updateParams({ lambda: v }));
    this.setupSlider('p-f0', 'p-f0-val', v => this.dynamics.updateParams({ f_0: v }));
    this.setupSlider('p-ewth', 'p-ewth-val', v => this.dynamics.updateParams({ E_wth: v }));
    this.setupSlider('p-noise', 'p-noise-val', v => this.dynamics.updateParams({ sigma_noise: v }));

    // Event injection: type selector, strength slider, narrative display, inject button
    const evTypeSelect = document.getElementById('ev-type-select');
    const evStrength = document.getElementById('ev-strength');
    const evStrVal = document.getElementById('ev-str-val');
    const evNarrative = document.getElementById('ev-narrative');

    const updateNarrative = () => {
      const type = evTypeSelect.value;
      const str = parseInt(evStrength.value);
      evStrVal.textContent = str;
      const narrative = getEventNarrative(type, str);
      evNarrative.textContent = narrative;
    };

    evTypeSelect.addEventListener('change', updateNarrative);
    evStrength.addEventListener('input', updateNarrative);
    updateNarrative(); // Initialize

    document.getElementById('btn-inject').addEventListener('click', () => {
      const type = evTypeSelect.value;
      const str = parseInt(evStrength.value);
      this.injectEvent(type, str);
    });
  }

  setupSlider(sliderId, valId, onChange) {
    const slider = document.getElementById(sliderId);
    const valEl = document.getElementById(valId);
    slider.addEventListener('input', () => {
      const v = parseFloat(slider.value);
      valEl.textContent = v.toFixed(slider.step.includes('.0') ? 1 : slider.step.split('.')[1]?.length || 2);
      onChange(v);
    });
  }

  loadPreset(key) {
    const scenario = SCENARIOS[key];
    if (!scenario) return;

    this.activePreset = key;

    // Update active button
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector(`.preset-btn[data-key="${key}"]`);
    if (btn) btn.classList.add('active');

    // Set parameters
    const params = { ...DEFAULT_PARAMS, ...scenario.params };
    this.dynamics = new HabitDynamics(params);

    // Set initial conditions
    const ic = scenario.initial;
    this.state = {
      H: ic.H, M: ic.M, E: ic.E, I: ic.I,
      C: params.C,
      B: 0, F: 0, dE_prev: 0,
      injured: false, stress: 0, ii: 0, social_support: 0,
    };

    // Set events
    this.events = (scenario.events || []).map(e => ({ ...e }));
    this.t_end = scenario.t_end || 730;

    // Update UI sliders
    this.updateSlider('ic-h', ic.H); this.updateSlider('ic-m', ic.M);
    this.updateSlider('ic-e', ic.E); this.updateSlider('ic-i', ic.I);
    this.updateSlider('p-c', params.C); this.updateSlider('p-ah', params.alpha_H);
    this.updateSlider('p-bm', params.beta_M); this.updateSlider('p-g', params.gamma);
    this.updateSlider('p-l', params.lambda); this.updateSlider('p-f0', params.f_0);
    this.updateSlider('p-ewth', params.E_wth); this.updateSlider('p-noise', params.sigma_noise);

    // Log
    this.clearLog();
    this.log(0, `Loaded: ${scenario.name}`, 'event');
    this.log(0, scenario.description, 'state');

    this.reset();
    this.play();
  }

  loadCluster(key) {
    const cluster = CHARACTERS[key];
    if (!cluster) return;

    this.activePreset = key;
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector(`.preset-btn[data-key="${key}"]`);
    if (btn) btn.classList.add('active');

    const params = { ...DEFAULT_PARAMS, ...cluster.params };
    this.dynamics = new HabitDynamics(params);

    const ic = cluster.initial;
    this.state = {
      H: ic.H, M: ic.M, E: ic.E, I: ic.I,
      C: params.C,
      B: 0, F: 0, dE_prev: 0,
      injured: false, stress: 0, ii: 0, social_support: 0,
    };

    this.events = (cluster.events || []).map(e => ({ ...e }));
    this.t_end = cluster.t_end || 730;

    this.updateSlider('ic-h', ic.H); this.updateSlider('ic-m', ic.M);
    this.updateSlider('ic-e', ic.E); this.updateSlider('ic-i', ic.I);
    this.updateSlider('p-c', params.C); this.updateSlider('p-ah', params.alpha_H);
    this.updateSlider('p-bm', params.beta_M); this.updateSlider('p-g', params.gamma);
    this.updateSlider('p-l', params.lambda); this.updateSlider('p-f0', params.f_0);
    this.updateSlider('p-ewth', params.E_wth); this.updateSlider('p-noise', params.sigma_noise);

    this.clearLog();
    this.log(0, `Loaded cluster: ${cluster.name}`, 'event');
    this.log(0, cluster.description, 'state');

    this.reset();
    this.play();
  }

  updateSlider(id, value) {
    const slider = document.getElementById(id);
    if (slider) {
      slider.value = value;
      slider.dispatchEvent(new Event('input'));
    }
  }

  reset() {
    this.pause();
    // Rebuild initial state from sliders
    const ic = {
      H: parseFloat(document.getElementById('ic-h').value),
      M: parseFloat(document.getElementById('ic-m').value),
      E: parseFloat(document.getElementById('ic-e').value),
      I: parseFloat(document.getElementById('ic-i').value),
    };

    this.simState = {
      H: ic.H, M: ic.M, E: ic.E, I: ic.I,
      C: this.dynamics.p.C,
      B: 0, F: 0, dE_prev: 0,
      injured: false, stress: 0, ii: 0, social_support: 0,
    };

    this.simTime = 0;
    this.history = [{
      t: 0, H: ic.H, M: ic.M, E: ic.E, I: ic.I, C: this.dynamics.p.C, B: 0, F: 0,
    }];
    this.currentIdx = 0;
    this.pendingEvents = (this.events || []).map(e => ({ ...e }));
    this.firedEvents = new Set();

    this.updateStateDisplay(this.simState);
    document.getElementById('day-display').textContent = '0';
  }

  play() {
    this.playing = true;
    document.getElementById('btn-play').classList.add('primary');
    document.getElementById('btn-pause').classList.remove('primary');
  }

  pause() {
    this.playing = false;
    document.getElementById('btn-pause').classList.add('primary');
    document.getElementById('btn-play').classList.remove('primary');
  }

  injectEvent(type, strength = 3) {
    const t = this.simTime;
    const spec = getEventSpec(type, strength);
    if (!spec) return;

    const ev = {
      time: t,
      type: spec.type,
      amplitude: spec.amplitude,
      label: spec.label,
    };

    this.pendingEvents.push(ev);
    this.events.push(ev);
    this.log(t, `[${strength}/5] ${spec.label}`, 'event');

    // Apply immediately
    const result = this.dynamics.applyEvent(this.simState, ev);
    this.simState = result.state;
    if (result.mImpulse !== 0 || result.eImpulse !== 0) {
      this.simState = this.dynamics.step(this.simState, this.dt, result.mImpulse, result.eImpulse);
    }
  }

  simulateStep() {
    if (!this.playing) return;
    if (this.simTime >= this.t_end) {
      this.pause();
      return;
    }

    const stepsPerFrame = Math.max(1, Math.round(this.speed * 3));

    for (let s = 0; s < stepsPerFrame; s++) {
      // Check for events (impulse-based: applied directly to state, not through rates)
      let mImpulse = 0, eImpulse = 0;
      for (const ev of this.pendingEvents) {
        const evKey = `${ev.type}_${ev.time}`;
        if (!this.firedEvents.has(evKey) && this.simTime >= ev.time && this.simTime < ev.time + this.dt * 2) {
          this.firedEvents.add(evKey);
          const result = this.dynamics.applyEvent(this.simState, ev);
          this.simState = result.state;
          mImpulse += result.mImpulse;
          eImpulse += result.eImpulse;
          this.log(ev.time, ev.label, 'event');
        }
      }

      this.simState = this.dynamics.step(this.simState, this.dt, mImpulse, eImpulse);
      this.simTime += this.dt;

      // Compute running aggregate metrics
      const s = this.simState;
      const C = s.C !== undefined ? s.C : this.dynamics.p.C;
      const cogLoad = C * (1 - s.H) * s.B;  // Instantaneous cognitive load
      const activity = C * s.B;               // Instantaneous activity volume

      // Running totals (accumulated)
      const prev = this.history.length > 0 ? this.history[this.history.length - 1] : null;
      const cumCogLoad = (prev ? prev.cumCogLoad : 0) + cogLoad * this.dt;
      const cumActivity = (prev ? prev.cumActivity : 0) + activity * this.dt;

      // Path length increment
      const dH = prev ? Math.abs(s.H - prev.H) : 0;
      const dM = prev ? Math.abs(s.M - prev.M) : 0;
      const dE = prev ? Math.abs(s.E - prev.E) : 0;
      const pathInc = Math.sqrt(dH*dH + dM*dM + dE*dE);
      const cumPath = (prev ? prev.cumPath : 0) + pathInc;

      // Settling: exponential moving average of |derivatives|
      const deriv = dH + dM + dE;
      const settling = prev ? 0.95 * prev.settling + 0.05 * deriv / this.dt : 0;

      // Record history (downsample for performance)
      if (this.history.length < 10000) {
        this.history.push({
          t: this.simTime,
          H: s.H, M: s.M, E: s.E, I: s.I, C: C, B: s.B, F: s.F,
          cogLoad, activity, cumCogLoad, cumActivity, cumPath, settling,
        });
      }
      this.currentIdx = this.history.length - 1;
    }

    // Update displays
    this.updateStateDisplay(this.simState);
    document.getElementById('day-display').textContent = Math.round(this.simTime);
  }

  updateStateDisplay(s) {
    const cv = (s.C !== undefined ? s.C : this.dynamics.p.C).toFixed(2);
    document.getElementById('val-h').textContent = s.H.toFixed(2);
    document.getElementById('val-m').textContent = s.M.toFixed(2);
    document.getElementById('val-e').textContent = s.E.toFixed(2);
    document.getElementById('val-i').textContent = s.I.toFixed(2);
    document.getElementById('val-c').textContent = cv;
    document.getElementById('val-b').textContent = s.B.toFixed(2);
    // Mobile duplicates
    const hm = document.getElementById('val-h-m');
    if (hm) {
      hm.textContent = s.H.toFixed(2);
      document.getElementById('val-m-m').textContent = s.M.toFixed(2);
      document.getElementById('val-e-m').textContent = s.E.toFixed(2);
      document.getElementById('val-i-m').textContent = s.I.toFixed(2);
      document.getElementById('val-c-m').textContent = cv;
      document.getElementById('val-b-m').textContent = s.B.toFixed(2);
    }
  }

  log(time, message, type = 'state') {
    const logEl = document.getElementById('log-content');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="time">d${Math.round(time)}</span> <span class="${type}">${message}</span>`;
    logEl.appendChild(entry);
    logEl.parentElement.scrollTop = logEl.parentElement.scrollHeight;
  }

  clearLog() {
    document.getElementById('log-content').innerHTML = '';
  }

  renderLoop() {
    this.simulateStep();
    this.renderer.render(this.history, this.events, this.currentIdx, this.dynamics.p, this.heatmaps);
    if (this.strip) {
      this.strip.render(this.history, this.events, this.currentIdx, this.t_end);
    }
    requestAnimationFrame(() => this.renderLoop());
  }
}

// Initialize on load
window.addEventListener('load', () => {
  window.app = new App();
});
