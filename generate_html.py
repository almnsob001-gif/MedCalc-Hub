import sqlite3
import json
import os

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Medical Abbreviations</title>
    <style>
        :root { --bg: #f4f6f8; --primary: #00796b; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, sans-serif; }
        body { background-color: var(--bg); color: #333; padding-bottom: 20px; }
        header { background-color: var(--primary); color: white; padding: 20px; text-align: center; position: sticky; top: 0; z-index: 10; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        h1 { font-size: 1.4rem; margin-bottom: 5px; }
        .stats { font-size: 0.85rem; opacity: 0.9; }
        .search-container { padding: 15px; background-color: var(--primary); position: sticky; top: 75px; z-index: 9; }
        input[type="text"] { width: 100%; padding: 14px; border: none; border-radius: 8px; font-size: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.2); outline: none; }
        .results { padding: 15px; }
        .card { background: white; border-radius: 12px; padding: 14px; margin-bottom: 12px; display: flex; box-shadow: 0 2px 8px rgba(0,0,0,0.06); animation: slideIn 0.3s ease; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .color-bar { width: 6px; border-radius: 3px; margin-right: 14px; flex-shrink: 0; }
        .header-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
        .abbr { font-size: 1.25rem; font-weight: bold; }
        .category { font-size: 0.75rem; color: #777; background: #f0f0f0; padding: 2px 8px; border-radius: 12px; }
        .full-name { font-size: 0.95rem; color: #444; line-height: 1.3; }
        .empty { text-align: center; color: #888; margin-top: 50px; font-size: 1.1rem; }
    </style>
</head>
<body>
    <header>
        <h1>Medical Abbreviations</h1>
        <div class="stats" id="stats">Loading...</div>
    </header>
    <div class="search-container">
        <input type="text" id="searchInput" placeholder="Enter abbreviation (e.g., HTN, MI, COPD)" autocomplete="off">
    </div>
    <div class="results" id="resultsContainer"><div class="empty">Type an abbreviation to search...</div></div>

    <script>
        const data = /*DATA_PLACEHOLDER*/ [];
        const colors = {"Cardiology":"#e53935","Pulmonology":"#1e88e5","Neurology":"#8e24aa","Endocrinology":"#fb8c00","Gastroenterology":"#43a047","Nephrology":"#00acc1","Urology":"#00897b","Hematology":"#d32f2f","Infectious Disease":"#ab47bc","Rheumatology":"#f57c00","Dermatology":"#ec407a","Ophthalmology":"#3949ab","ENT":"#5c6bc0","Obstetrics":"#f06292","Gynecology":"#d81b60","Pediatrics":"#00bfa5","Psychiatry":"#7e57c2","Orthopedics":"#757575","Emergency":"#d84315","Critical Care":"#e64a19","Surgery":"#546e7a","Labs":"#0097a7","Imaging":"#607d8b","Documentation":"#546e7a","Pharmacology":"#9c27b0","Route":"#689f38","Frequency":"#827717","Orders":"#795548","Ventilation":"#1976d2","Vascular":"#c62828","Anatomy":"#6d4c41"};
        
        const resultsContainer = document.getElementById('resultsContainer');
        const searchInput = document.getElementById('searchInput');
        const stats = document.getElementById('stats');
        const categories = new Set(data.map(d => d.category).filter(Boolean));
        
        stats.textContent = data.length + " abbreviations · " + categories.size + " specialties";

        function renderCards(items) {
            resultsContainer.innerHTML = '';
            if (items.length === 0) {
                resultsContainer.innerHTML = '<div class="empty">No results found.</div>';
                return;
            }
            items.forEach(item => {
                const color = colors[item.category] || "#9e9e9e";
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div class="color-bar" style="background-color: ${color}"></div>
                    <div style="flex:1;">
                        <div class="header-row">
                            <span class="abbr" style="color: ${color}">${item.abbr}</span>
                            <span class="category">${item.category}</span>
                        </div>
                        <div class="full-name">${item.full_name}</div>
                    </div>
                `;
                resultsContainer.appendChild(card);
            });
        }

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim().toUpperCase();
            if (!query) {
                resultsContainer.innerHTML = '<div class="empty">Type an abbreviation to search...</div>';
                return;
            }
            const results = data.filter(item => item.abbr.toUpperCase().includes(query));
            results.sort((a, b) => (b.abbr.toUpperCase() === query ? 1 : 0) - (a.abbr.toUpperCase() === query ? 1 : 0));
            renderCards(results.slice(0, 100));
        });
    </script>
</body>
</html>
"""

conn = sqlite3.connect('medical_terms.db')
cur = conn.cursor()
cur.execute("SELECT abbr, full_name, category FROM abbreviations")
rows = cur.fetchall()
conn.close()

data = [{"abbr": r[0], "full_name": r[1], "category": r[2]} for r in rows]
html = html_template.replace("/*DATA_PLACEHOLDER*/ []", json.dumps(data))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html generated successfully!")