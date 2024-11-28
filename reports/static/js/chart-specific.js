//// Score Distribution Chart

var scoreData = JSON.parse(document.getElementById("score-distribution").textContent);

// Chart.js - Biểu đồ phân phối điểm
var ctx1 = document.getElementById('scoreDistributionChart').getContext('2d');
new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: scoreData.ranges, // Các khoảng điểm (0-10, 10-20, ...)
        datasets: [{
            label: 'Number of Students', // Nhãn biểu đồ
            data: scoreData.counts, // Số lượng sinh viên
            backgroundColor: '#4caf50', // Màu thanh
            borderColor: '#388e3c', // Màu viền
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Score Distribution for Course' // Tiêu đề biểu đồ
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.label}: ${context.raw} students`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true, // Trục Y bắt đầu từ 0
                title: {
                    display: true,
                    text: 'Number of Students'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Score Ranges'
                }
            }
        }
    }
});