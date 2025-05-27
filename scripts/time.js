// scripts/time.js
;(async function() {
  // 1) Load once
  const resp = await fetch('/configs/locations.json');
  if (!resp.ok) {
    console.error('Failed to load locations.json');
    return;
  }
  const locations = await resp.json();

  // 2) Update both title (once) and time (repeatedly)
  locations.forEach((loc, idx) => {
    const titleEl = document.getElementById(`location${idx}-title`);
    if (titleEl) titleEl.textContent = loc.displayname;
  });

  function updateClocks() {
    Logger.debug('Updating clocks...');
    const now = new Date();
    locations.forEach((loc, idx) => {
      const timeStr = new Intl.DateTimeFormat('en-US', {
        hour:   '2-digit',
        minute: '2-digit',
        timeZone: loc.timezone,
        hour12: false
      }).format(now);

      const timeEl = document.getElementById(`location${idx}-time`);
      if (timeEl) timeEl.textContent = timeStr;
    });
  }

  // 3) Kick off immediately, then every 500 ms
  updateClocks();
  setInterval(updateClocks, 500);
})();
