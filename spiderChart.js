// add this in place of the initialize chart function for line charts
// spider chart
// Initialize Chart
        const ctx = document.getElementById(`spider-${index}`).getContext("2d");
        chartInstances[`spider-${index}`] = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: Object.keys(features),
                datasets: [{
                    data: Object.values(features),
                    backgroundColor: labelColorMap[personaName] + '44',
                    borderColor: labelColorMap[personaName],
                    borderWidth: 2,
                    pointBackgroundColor: labelColorMap[personaName]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        ticks: { display: false },
                        grid: { color: 'rgba(0,0,0,0.05)' }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });


// line graph
        {// Initialize Chart
            const ctx = document.getElementById(`spider-${index}`).getContext("2d");
        chartInstances[`spider-${index}`] = new Chart(ctx, {
            type: 'line', // 1. Change type to line
            data: {
                labels: Object.keys(features),
                datasets: [{
                    label: 'Deviation from Average',
                    data: Object.values(features),
                    borderColor: labelColorMap[personaName],
                    backgroundColor: labelColorMap[personaName] + '22',
                    fill: true, // 2. Fills area between the line and the zero-axis
                    tension: 0.4, // 3. Curves the line for a modern look
                    pointRadius: 4,
                    pointBackgroundColor: labelColorMap[personaName],
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true, // 4. Ensures 0 (the class average) is the baseline
                        grid: {
                            // 5. Makes the zero-line (average) bold/darker
                            color: (context) => context.tick.value === 0 ? '#1e293b' : '#e2e8f0',
                            lineWidth: (context) => context.tick.value === 0 ? 2 : 1
                        },
                        ticks: {
                            // 6. Adds a "+" or "-" sign to the values for clarity
                            callback: function(value) {
                                return (value > 0 ? '+' : '') + value;
                            }
                        }
                    },
                    x: {
                        grid: { display: false } // Cleans up the background
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let val = context.parsed.y;
                                let status = val >= 0 ? "Above Average" : "Below Average";
                                return `${Math.abs(val)} Std Dev ${status}`;
                            }
                        }
                    }
                }
            }
        });
        }