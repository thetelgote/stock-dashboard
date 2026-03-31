let chart;

async function loadData() {
    let symbol = document.getElementById("company1").value;

    let res = await fetch(`http://127.0.0.1:8000/data/${symbol}`);
    let data = await res.json();

    let labels = data.map(d => d.Date);
    let prices = data.map(d => d.Close);
    let ma = data.map(d => d.MA_7);

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: symbol + " Price",
                    data: prices,
                    borderWidth: 2
                },
                {
                    label: "7-Day Moving Avg",
                    data: ma,
                    borderDash: [5,5],
                    borderWidth: 2
                }
            ]
        }
    });
}

async function compareData() {
    let s1 = document.getElementById("company1").value;
    let s2 = document.getElementById("company2").value;

    let res = await fetch(`http://127.0.0.1:8000/compare?symbol1=${s1}&symbol2=${s2}`);
    let data = await res.json();

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: Array.from({length: data[s1].length}, (_, i) => i+1),
            datasets: [
                {
                    label: s1,
                    data: data[s1],
                    borderWidth: 2
                },
                {
                    label: s2,
                    data: data[s2],
                    borderWidth: 2
                }
            ]
        }
    });
}