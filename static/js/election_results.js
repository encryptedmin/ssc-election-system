(function () {
    const root = document.getElementById('election-results-app');
    const dataNode = document.getElementById('election-results-data');

    if (!root || !dataNode) {
        return;
    }

    const charts = {};
    const resultsUrl = root.dataset.resultsUrl;
    const electionActive = root.dataset.electionActive === 'true';
    let currentResults = JSON.parse(dataNode.textContent);

    function numberText(value) {
        return Number(value || 0).toLocaleString();
    }

    function percentText(value) {
        return Number(value || 0).toLocaleString(
            undefined,
            { maximumFractionDigits: 1 }
        );
    }

    function setText(selector, value) {
        const element = root.querySelector(selector);

        if (element) {
            element.textContent = value;
        }
    }

    function updateSummary(data) {
        Object.entries(data.summary).forEach(([key, value]) => {
            const formatter = key === 'turnout_percentage'
                ? percentText
                : numberText;

            setText(`[data-summary="${key}"]`, formatter(value));
        });

        setText('[data-generated-at]', data.generated_at);
    }

    function updateLiveCounts(data) {
        data.positions.forEach((position) => {
            setText(
                `[data-position-total="${position.id}"]`,
                numberText(position.total_votes)
            );
            setText(
                `[data-position-chart-total="${position.id}"]`,
                numberText(position.total_votes)
            );

            position.candidates.forEach(updateCandidateRow);
        });
    }

    function updateCandidateRow(candidate) {
        const row = root.querySelector(
            `[data-candidate-row="${candidate.id}"]`
        );

        if (!row) {
            return;
        }

        setText(
            `[data-candidate-votes="${candidate.id}"]`,
            numberText(candidate.votes)
        );
        setText(
            `[data-candidate-percentage="${candidate.id}"]`,
            percentText(candidate.percentage)
        );

        const badge = root.querySelector(
            `[data-candidate-winner="${candidate.id}"]`
        );
        const bar = root.querySelector(
            `[data-candidate-bar="${candidate.id}"]`
        );

        row.classList.toggle('border-green-500', candidate.is_winner);
        row.classList.toggle('bg-green-500/10', candidate.is_winner);
        row.classList.toggle('border-slate-800', !candidate.is_winner);
        row.classList.toggle('bg-slate-950', !candidate.is_winner);

        if (badge) {
            badge.classList.toggle('hidden', !candidate.is_winner);
            badge.textContent = electionActive ? 'Leading' : 'Winner';
        }

        if (bar) {
            bar.style.width = `${candidate.percentage}%`;
            bar.classList.toggle('bg-green-500', candidate.is_winner);
            bar.classList.toggle('bg-blue-500', !candidate.is_winner);
        }
    }

    function updateDepartmentTable(data) {
        data.department_participation.forEach((department) => {
            const row = root.querySelector(
                `[data-department-row="${cssEscape(department.department)}"]`
            );

            if (!row) {
                return;
            }

            row.querySelector('[data-department-registered]').textContent =
                numberText(department.registered);
            row.querySelector('[data-department-voted]').textContent =
                numberText(department.voted);
            row.querySelector('[data-department-percentage]').textContent =
                percentText(department.percentage);
        });
    }

    function cssEscape(value) {
        if (window.CSS && CSS.escape) {
            return CSS.escape(value);
        }

        return String(value).replace(/"/g, '\\"');
    }

    function chartOptions(horizontal) {
        const categoryAxis = {
            ticks: { color: '#94a3b8' },
            grid: { color: '#1e293b' }
        };
        const valueAxis = {
            beginAtZero: true,
            ticks: {
                precision: 0,
                color: '#94a3b8'
            },
            grid: { color: '#1e293b' }
        };

        return {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: horizontal ? 'y' : 'x',
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            },
            scales: horizontal
                ? { x: valueAxis, y: categoryAxis }
                : { x: categoryAxis, y: valueAxis }
        };
    }

    function doughnutOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            }
        };
    }

    function renderCharts(data) {
        if (!window.Chart) {
            return;
        }

        renderChart(
            'turnout',
            root.querySelector('[data-chart="turnout"]'),
            {
                type: 'doughnut',
                data: {
                    labels: ['Voted', 'Not Voted'],
                    datasets: [{
                        data: [
                            data.summary.voted_voters,
                            data.summary.not_voted
                        ],
                        backgroundColor: ['#22c55e', '#475569'],
                        borderColor: '#0f172a'
                    }]
                },
                options: doughnutOptions()
            }
        );

        renderChart(
            'registered-voted',
            root.querySelector('[data-chart="registered-voted"]'),
            {
                type: 'bar',
                data: {
                    labels: ['Registered', 'Voted'],
                    datasets: [{
                        label: 'Voters',
                        data: [
                            data.summary.registered_voters,
                            data.summary.voted_voters
                        ],
                        backgroundColor: ['#38bdf8', '#22c55e']
                    }]
                },
                options: chartOptions(false)
            }
        );

        renderChart(
            'department',
            root.querySelector('[data-chart="department"]'),
            {
                type: 'bar',
                data: {
                    labels: data.department_participation.map(
                        (item) => item.department
                    ),
                    datasets: [
                        {
                            label: 'Registered',
                            data: data.department_participation.map(
                                (item) => item.registered
                            ),
                            backgroundColor: '#38bdf8'
                        },
                        {
                            label: 'Voted',
                            data: data.department_participation.map(
                                (item) => item.voted
                            ),
                            backgroundColor: '#22c55e'
                        }
                    ]
                },
                options: chartOptions(false)
            }
        );

        data.positions.forEach((position) => {
            renderChart(
                `position-${position.id}`,
                root.querySelector(`[data-position-chart="${position.id}"]`),
                {
                    type: 'bar',
                    data: {
                        labels: position.candidates.map(
                            (candidate) => candidate.name
                        ),
                        datasets: [{
                            label: 'Votes',
                            data: position.candidates.map(
                                (candidate) => candidate.votes
                            ),
                            backgroundColor: position.candidates.map(
                                (candidate) => candidate.is_winner
                                    ? '#22c55e'
                                    : '#3b82f6'
                            )
                        }]
                    },
                    options: chartOptions(true)
                }
            );
        });
    }

    function renderChart(key, canvas, config) {
        if (!canvas) {
            return;
        }

        if (!charts[key]) {
            charts[key] = new Chart(canvas, config);
            return;
        }

        charts[key].data = config.data;
        charts[key].options = config.options;
        charts[key].update();
    }

    function render(data) {
        updateSummary(data);
        updateLiveCounts(data);
        updateDepartmentTable(data);
        renderCharts(data);
    }

    async function refreshResults() {
        if (!resultsUrl) {
            return;
        }

        try {
            const response = await fetch(resultsUrl, {
                headers: { Accept: 'application/json' },
                cache: 'no-store'
            });

            if (!response.ok) {
                return;
            }

            currentResults = await response.json();
            render(currentResults);
        } catch (error) {
            console.error('Unable to refresh election results.', error);
        }
    }

    render(currentResults);
    window.setInterval(refreshResults, 5000);
}());
