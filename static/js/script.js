const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#C9CBCF', '#FF9F40'];

// Object to store every chart instance to prevent overlapping/glitching
let chartInstances = {};

function render_charts(rawData) {
    // make everything visible
    document.getElementById("post_analysis").style.display = "block";

    //  display mode of analysis
    const isPredicted = rawData.is_predicted;
    let modeText = "";
    // 2. Determine the text based on the flag
    if (isPredicted) {
        modeText = "Pre Sem Analysis ";
    } else {
        modeText = "Post Exam Analysis ";
    }
    document.getElementById("mode").innerHTML=`<h2>${modeText}</h2>`

// 3. Update the HTML
// Make sure you have an element with id="mode" in your HTML
    // Clear existing instances
    Object.values(chartInstances).forEach(chart => chart.destroy());
    chartInstances = {}; 

    // 1. BUILD THE COLOR MAP
    // This assigns a permanent color to every unique label found in your data
    const personaLabels = Object.keys(rawData.mega_pie.persona);
    const trajectoryLabels = Object.keys(rawData.mega_pie.academic);
    const allUniqueLabels = [...new Set([...personaLabels, ...trajectoryLabels])];
    
    const labelColorMap = {};
    allUniqueLabels.forEach((label, index) => {
        labelColorMap[label] = colors[index % colors.length];
    });
     
    // 3. Overall Academic Pie
    chartInstances['academicPie'] = new Chart(document.getElementById('academicPie'), {
        type: 'pie',
        data: {
            labels: Object.keys(rawData.mega_pie.academic),
            datasets: [{ data: Object.values(rawData.mega_pie.academic), backgroundColor: colors }]
        }
    });
    
    // 3. Update Overall Persona Pie
    chartInstances['personaPie'] = new Chart(document.getElementById('personaPie'), {
        type: 'pie',
        data: {
            labels: personaLabels,
            datasets: [{ 
                data: Object.values(rawData.mega_pie.persona), 
                backgroundColor: personaLabels.map(l => labelColorMap[l]) // Map colors to labels
            }]
        }
    });

    // 4. Update Trajectory Composition per Persona
    const trajContainer = document.getElementById('trajectoryPersonaContainer');
    trajContainer.innerHTML = '';
    
    Object.entries(rawData.trajectory_mapping).forEach(([persona, dist], i) => {
        const chartId = `traj-p-${i}`;
        const div = document.createElement('div');
        div.className = 'chart-container';
        div.innerHTML = `<h2>${persona}: Trajectory Breakdown</h2><canvas id="${chartId}"></canvas>`;
        trajContainer.appendChild(div);

        const currentLabels = Object.keys(dist);

        chartInstances[chartId] = new Chart(document.getElementById(chartId), {
            type: 'pie',
            data: {
                labels: currentLabels,
                datasets: [{ 
                    data: Object.values(dist), 
                    backgroundColor: currentLabels.map(l => labelColorMap[l]) // Consistency across charts
                }]
            }
        });
    });

    // 6. Persona Profiles (Dynamic Spider Charts)
    const spiderContainer = document.getElementById("spiderContainer");
    spiderContainer.innerHTML = ""; 

    Object.entries(rawData.spider).forEach(([personaName, features], index) => {
        const card = document.createElement("div");
        card.className = "flip-card";
        
        // Get score from backend
        const avgScore = rawData.persona_averages[personaName] || 0;

        card.innerHTML = `
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <div style="text-align: center; margin-bottom: 0.5rem;">
                    <h2 style="font-size: 1.1rem; margin: 0; color: var(--text-main);">${personaName}</h2>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 2px 0;">Relative to Class Average</p>
                </div>
                
                <div style="flex: 1; min-height: 0; width: 100%;">
                    <canvas id="spider-${index}"></canvas>
                </div>
                
                <p style="font-size: 0.7rem; color: var(--text-muted); text-align: center; margin-top: 5px;">
                    <span style="color: var(--primary); font-weight: bold;">↑</span> Strengths | 
                    <span style="color: #ef4444; font-weight: bold;">↓</span> Deficits
                </p>
            </div>
            
            <div class="flip-card-back">
                <h2 style="color: white; margin-bottom: 5px;">${personaName}</h2>
                <p style="opacity: 0.9; font-size: 0.9rem;">Average Performance</p>
                <div style="font-size: 3rem; font-weight: 800; margin: 10px 0;">${avgScore}%</div>
                <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">
                    ${rawData.is_predicted ? "Model Prediction" : "Actual Class Average"}
                </div>
            </div>
        </div>
        `;
        spiderContainer.appendChild(card);

        // Toggle Flip
        card.addEventListener("click", () => {
            card.classList.toggle("is-flipped");
        });

        
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
    });

    // 7. Helper for Double Bar Charts (Demographics)
    function createDoubleBar(id, source, k1, k2) {
        const labels = Object.keys(source);
        chartInstances[id] = new Chart(document.getElementById(id), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    { label: k1, data: labels.map(l => source[l][k1]), backgroundColor: '#36A2EB' },
                    { label: k2, data: labels.map(l => source[l][k2]), backgroundColor: '#FF6384' }
                ]
            },
            options: { 
                responsive: true,
                scales: { y: { beginAtZero: true, max: 100 } } 
            }
        });
    }

    // 8. Render Demographic Bar Charts
    createDoubleBar('genderPersonaBar', rawData.gender_summary.persona, 'Male', 'Female');
    createDoubleBar('genderAcademicBar', rawData.gender_summary.academic, 'Male', 'Female');
    createDoubleBar('schoolPersonaBar', rawData.school_summary.persona, 'Public', 'Private');
    createDoubleBar('schoolAcademicBar', rawData.school_summary.academic, 'Public', 'Private');

    const insights=rawData.AI_insights;
    show_ai_insights(insights); 
}


/**
 * Fills all the divs of class 'insights' with structured AI content.
 */
function show_ai_insights(insights) {
    // 1. Map the JSON keys from app.py to the HTML IDs in index.html
    const mapping = {
        'pie_insights': insights.mega_pie_insights,
        'nested_insights': insights.trajectory_wise_persona,
        'spider_insights': insights.spider_chart_inferences,
        'gender_insights': insights.gender_insights,
        'school_insights': insights.school_insights,
        'actionable_insights_content': insights.actionable_recommendations
    };

    // 2. Loop through the mapping and update the DOM
    Object.entries(mapping).forEach(([elementId, content]) => {
        const element = document.getElementById(elementId);
        if (element && content) {
            // Check if the content is an error message
            if (insights.error) {
                element.innerHTML = `<p style="color: #ef4444;">⚠️ ${insights.error}</p>`;
            } else {
                // Convert AI bullet points (\n) into HTML breaks or list items
                // This makes the response look clean in the UI
                element.innerHTML = format_insight_text(content);
            }
        }
    });
}

/**
 * Helper to turn AI text blocks into clean HTML list items
 */
function format_insight_text(text) {
    if (!text) return "No data available.";
    
    // Split by newlines and create a bulleted list
    const lines = text.split('\n').filter(line => line.trim() !== "");
    let html = '<ul style="list-style-type: none; padding-left: 0;">';
    
    lines.forEach(line => {
        // Clean up common AI markers like "**" or "-"
        const cleanLine = line.replace(/^\s*[\*\-\•]\s*/, '').replace(/\*\*/g, '');
        html += `<li style="margin-bottom: 0.8rem; display: flex; align-items: flex-start;">
                    <span style="color: #6366f1; margin-right: 10px;">✦</span>
                    <span>${cleanLine}</span>
                 </li>`;
    });
    
    html += '</ul>';
    return html;
}

