// Available skills
const ALL_SKILLS = [
    "DSA", "DBMS", "OS", "Python", "Java", "OOP", "Web Development", "Machine Learning"
];

// Currently selected skills
let selectedSkills = new Set(["DSA", "Python"]);
let selectedFile = null;

// Initialize Skill Pills
function initSkills() {
    const container = document.getElementById('skillsContainer');
    ALL_SKILLS.forEach(skill => {
        const pill = document.createElement('div');
        pill.className = `skill-pill ${selectedSkills.has(skill) ? 'selected' : ''}`;
        pill.textContent = skill;
        pill.onclick = () => toggleSkill(skill, pill);
        container.appendChild(pill);
    });
}

function toggleSkill(skill, element) {
    if (selectedSkills.has(skill)) {
        selectedSkills.delete(skill);
        element.classList.remove('selected');
    } else {
        selectedSkills.add(skill);
        element.classList.add('selected');
    }
}

// File Upload Logic
function initFileUpload() {
    const dropZone = document.getElementById('fileUploadZone');
    const fileInput = document.getElementById('resumePdf');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            if (file.type === 'application/pdf') {
                fileInput.files = e.dataTransfer.files; // assign to input
                handleFile(file);
            } else {
                alert('Please upload a PDF file.');
            }
        }
    });

    function handleFile(file) {
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        fileNameDisplay.classList.add('file-selected');
    }
}

function updateCGPA(value) {
    document.getElementById('cgpaValue').textContent = value;
}

// Perform Analysis
async function analyzeProfile() {
    const cgpa = document.getElementById('cgpa').value;
    const numSkills = document.getElementById('numSkills').value;
    const numProjects = document.getElementById('numProjects').value;
    const skillsArray = Array.from(selectedSkills).join(',');

    if (!selectedFile) {
        alert("Please upload your resume (PDF) before analyzing.");
        return;
    }

    // Build Form Data
    const formData = new FormData();
    formData.append('cgpa', cgpa);
    formData.append('numSkills', numSkills);
    formData.append('numProjects', numProjects);
    formData.append('skills', skillsArray);
    formData.append('resumePdf', selectedFile);

    const btn = document.querySelector('.analyze-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Analyzing...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error("Server Error");
        
        const data = await response.json();
        displayResults(data, Array.from(selectedSkills));
        
    } catch (error) {
        alert("Failed to analyze profile. Make sure the backend server is running.");
        console.error(error);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function displayResults(results, selectedSkillsArray) {
    const { probability, scoreBreakdown, missingSkills, suggestions, companyPredictions, resumeScore } = results;

    let category, emoji, colorClass;
    if (probability >= 70) {
        category = "High"; emoji = "🟢"; colorClass = "var(--success)";
    } else if (probability >= 40) {
        category = "Medium"; emoji = "🟡"; colorClass = "var(--warning)";
    } else {
        category = "Low"; emoji = "🔴"; colorClass = "var(--danger)";
    }
    
    // Update UI
    document.getElementById('probabilityText').textContent = `Placement Chance: ${probability.toFixed(1)}%`;
    document.getElementById('categoryText').textContent = `${emoji} Category: ${category}`;
    
    const progressFill = document.getElementById('progressFill');
    progressFill.style.width = '0%';
    setTimeout(() => {
        progressFill.style.width = `${probability}%`;
        progressFill.style.backgroundColor = colorClass;
    }, 100);
    
    // Score breakdown
    document.getElementById('scoreBreakdown').innerHTML = `
        <p style="margin-bottom: 8px;"><strong>CGPA Score:</strong> ${scoreBreakdown.cgpaScore.toFixed(1)}/40</p>
        <p style="margin-bottom: 8px;"><strong>Skills Score:</strong> ${scoreBreakdown.skillsScore.toFixed(1)}/30</p>
        <p style="margin-bottom: 8px;"><strong>Projects Score:</strong> ${scoreBreakdown.projectsScore.toFixed(1)}/20</p>
        <p><strong>Key Skills Bonus:</strong> ${scoreBreakdown.keySkillsBonus.toFixed(1)}/10</p>
    `;
    
    // Company predictions
    let companyHTML = '';
    for (const [company, prob] of Object.entries(companyPredictions)) {
        companyHTML += `
            <div class="company-score">
                <span>${company}</span>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${prob}%; background: ${prob >= 70 ? 'var(--success)' : prob >= 40 ? 'var(--warning)' : 'var(--danger)'}"></div>
                    </div>
                    <span style="font-weight:600; width: 45px; text-align:right;">${prob.toFixed(1)}%</span>
                </div>
            </div>
        `;
    }
    document.getElementById('companyPredictions').innerHTML = companyHTML;
    
    // Skill gap
    let skillHTML = '<p style="margin-bottom: 10px; color: var(--text-muted);"><strong>Your Current Skills:</strong></p>';
    selectedSkillsArray.forEach(skill => {
        skillHTML += `<span class="skill-item">${skill}</span>`;
    });
    
    if (missingSkills.length > 0) {
        skillHTML += '<p style="margin-top: 20px; margin-bottom: 10px; color: var(--text-muted);"><strong>Missing Key Skills:</strong></p>';
        missingSkills.forEach(skill => {
            skillHTML += `<span class="skill-item missing-skill">${skill}</span>`;
        });
    } else {
        skillHTML += '<p style="margin-top: 20px; color: var(--success); font-weight: 500;">✅ You have all the key skills!</p>';
    }
    document.getElementById('skillGap').innerHTML = skillHTML;
    
    // Resume score
    let resumeHTML = `<h4 style="font-size: 2rem; margin-bottom: 10px;">${resumeScore}<span style="font-size: 1rem; color: var(--text-muted);">/100</span></h4>`;
    if (resumeScore >= 80) {
        resumeHTML += '<p style="color: var(--success); font-weight: 500;">🎉 Excellent resume!</p>';
    } else if (resumeScore >= 60) {
        resumeHTML += '<p style="color: var(--warning); font-weight: 500;">👍 Good resume, can be improved</p>';
    } else {
        resumeHTML += '<p style="color: var(--danger); font-weight: 500;">⚠️ Resume needs significant improvement</p>';
    }
    document.getElementById('resumeScore').innerHTML = resumeHTML;
    
    // Suggestions
    let suggestionsHTML = '';
    suggestions.forEach(suggestion => {
        suggestionsHTML += `<div class="suggestion">${suggestion}</div>`;
    });
    document.getElementById('suggestions').innerHTML = suggestionsHTML;
    
    // Show results
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initSkills();
    initFileUpload();
});
