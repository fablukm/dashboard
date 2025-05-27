// reads /configs/logging.json once and logs to console

window.Logger = {
  _levels: { error: 0, info: 1, debug: 2 },
  _current: 2,  // default to debug but read later from file

  async init() {
    try {
      const r = await fetch('/configs/logging.json');
      const cfg = await r.json();
      const lvl = cfg.frontend?.level?.toLowerCase();
      if (this._levels[lvl] != null) this._current = this._levels[lvl];
    } catch (e) {
      console.error('Logger init failed, defaulting to debug', e);
    }
    this.debug('Logger initialized with level:', Object.keys(this._levels)[this._current]);
  },

  _log(levelName, ...args) {
    const lvl = this._levels[levelName];
    if (lvl <= this._current) console[levelName](...args);
  },

  debug(...args) { this._log('debug', ...args); },
  info (...args) { this._log('info',  ...args); },
  error(...args) { this._log('error', ...args); }
};

// immediately kick off config load
Logger.init();
