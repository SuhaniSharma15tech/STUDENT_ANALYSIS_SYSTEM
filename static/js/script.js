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
                    <h2 style="font-size: 1.1rem; margin-bottom: 1rem;">${personaName} Traits</h2>
                    <div style="flex-grow: 1; position: relative; width: 100%;">
                        <canvas id="spider-${index}"></canvas>
                    </div>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px;">Click to view score</p>
                </div>
                
                <div class="flip-card-back">
                    <h2 style="color: white; margin-bottom: 5px;">${personaName}</h2>
                    <p style="opacity: 0.9;">Average Performance</p>
                    <div style="font-size: 4rem; font-weight: 800; margin: 20px 0;">${avgScore}%</div>
                    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 0.85rem;">
                        ${rawData.is_predicted ? "Predicted Exam Score" : "average exam score of this persona"}
                    </div>
                </div>
            </div>
        `;

        spiderContainer.appendChild(card);

        // Toggle Flip
        card.addEventListener("click", () => {
            card.classList.toggle("is-flipped");
        });

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

