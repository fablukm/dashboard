async function updateTransport() {
    try {
        Logger.info('Fetching transport data at', new Date().toISOString());

        const response = await fetch('/transport');
        const data = await response.json();

        Logger.debug('Raw transport API response:', data);

        const bielContainer = document.querySelector('.biel-connections');
        const otherContainer = document.querySelector('.other-connections');
        // Clear containers except for their h2
        bielContainer.innerHTML = '';
        otherContainer.innerHTML = '';

        data.forEach(group => {
            const targetContainer = group.station_departure.name === "Biel/Bienne"
                ? bielContainer
                : otherContainer;

            // Title per connection group
            const title = document.createElement('h3');
            if (!group.connections || group.connections.length === 0) {
                title.textContent = `no connections ${group.station_departure.name} → ${group.station_arrival.name}`;
                targetContainer.appendChild(title);
                // Do not show the table
                return;
            } else {
                title.textContent = `${group.station_departure.name} → ${group.station_arrival.name}`;
            }
            targetContainer.appendChild(title);

            const table = document.createElement('div');
            table.classList.add('transport-table');

            group.connections.forEach(conn => {
                const row = document.createElement('div');
                row.classList.add('transport-row');

                // Icon based on line or type
                const icon = document.createElement('div');
                icon.classList.add('cell', 'transport-icon');
                const iconName = getIconForLine(conn.line);
                icon.innerHTML = `<img src="/static/assets/icons/${iconName}.svg" alt="Transport icon">`;
                row.appendChild(icon);

                row.innerHTML += `
                    <div class="cell departure-time">${conn.time}</div>
                    <div class="cell delay">${conn.delay ? '+' + conn.delay : ''}</div>
                    <div class="cell platform">${
                        group.show_platform && conn.platform
                            ? `<img src="/static/assets/icons/platforms/platform_${conn.platform}.svg" alt="Platform ${conn.platform}">`
                            : ''
                    }</div>
                    <div class="cell terminus">${conn.terminus.name}</div>
                    <div class="cell airport-icon">${conn.airport ? '<img src="/static/assets/icons/airplane-medium.svg" alt="Stops at airport">' : ''}</div>
                    <div class="cell arrival-time">${conn.arrival_time}</div>
                `;
                table.appendChild(row);
            });

            targetContainer.appendChild(table);
        });
    } catch (error) {
        Logger.error("Transport data fetch failed:", error);
    }
}

function getIconForLine(line) {
    const lower = line.toLowerCase();
    if (/^\d+$/.test(lower)) return 'bus-right';
    // if (lower.includes('ic')) return 'train';
    // if (lower.includes('ir')) return 'train';
    // if (lower.includes('re')) return 'train';
    // if (lower.startsWith('s')) return 'strain';
    return lower; // default fallback
}

document.addEventListener('DOMContentLoaded', updateTransport);

// keep polling every 20 seconds, due to the limit of 10080 requests per day
setInterval(updateTransport, 20000);