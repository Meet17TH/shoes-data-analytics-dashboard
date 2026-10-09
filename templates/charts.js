// charts.js
let chartInstance;

// Function to run when the page loads
document.addEventListener('DOMContentLoaded', function() {
  // Load top products by default
  loadChart(Price);
});

function destroyChart() {
  if (chartInstance) {
    chartInstance.destroy();
  }
}

function toggleView(showChart) {
  const tableContainer = document.getElementById('productTableContainer');
  
  if (showChart) {
    tableContainer.classList.add('hidden');
  } else {
    tableContainer.classList.remove('hidden');
  }
}

// Function to load top products
function loadChart(type) {
  destroyChart();
  toggleView(true); // Show chart, hide table

  if (type === 'price') {
    document.getElementById('chart-title').innerText = 'Price Distribution';
    fetch('http://localhost:8000/api/price-distribution')
      .then(res => res.json())
      .then(data => {
        const labels = Object.keys(data);
        const values = Object.values(data);
        chartInstance = new Chart(document.getElementById('mainChart'), {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Number of Products',
              data: values,
              backgroundColor: '#2a9d8f'
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      });
  }

  else if (type === 'discount') {
    document.getElementById('chart-title').innerText = 'Average Discount by Brand';
    fetch('http://localhost:8000/api/discounts')
      .then(res => res.json())
      .then(data => {
        const labels = Object.keys(data).slice(0, 10);
        const values = Object.values(data).slice(0, 10);
        chartInstance = new Chart(document.getElementById('mainChart'), {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Avg Discount (%)',
              data: values,
              backgroundColor: '#f4a261'
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      });
  }

  else if (type === 'kmeans') {
    document.getElementById('chart-title').innerText = 'KMeans Clustering (Price vs Discount)';
    fetch('http://localhost:8000/api/kmeans?k=3')
      .then(res => res.json())
      .then(data => {
        const clusterColors = ['#e76f51', '#2a9d8f', '#264653'];
        const datasets = [0, 1, 2].map(clusterId => {
          const points = data.filter(d => d.Cluster === clusterId).map(d => ({
            x: d.Price,
            y: d["Computed Discount %"]
          }));
          return {
            label: `Cluster ${clusterId}`,
            data: points,
            backgroundColor: clusterColors[clusterId],
            pointRadius: 5
          };
        });
        chartInstance = new Chart(document.getElementById('mainChart'), {
          type: 'scatter',
          data: { datasets },
          options: {
            responsive: true,
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Price (₹)'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Discount (%)'
                }
              }
            }
          }
        });
      });
  }

  else if (type === 'elbow') {
    document.getElementById('chart-title').innerText = 'Elbow Plot';
    fetch('http://localhost:8000/api/elbow')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(d => d.k);
        const values = data.map(d => d.inertia);
        chartInstance = new Chart(document.getElementById('mainChart'), {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Inertia',
              data: values,
              borderColor: '#e76f51',
              fill: false
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                title: {
                  display: true,
                  text: 'Inertia'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Number of Clusters (k)'
                }
              }
            }
          }
        });
      });
  }
}