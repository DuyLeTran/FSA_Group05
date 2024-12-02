//// Score Distribution Chart

var scoreData = JSON.parse(document.getElementById("score-distribution").textContent);
var course_name = JSON.parse(document.getElementById("course-name").textContent)
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
                text: 'Score Distribution for ' + course_name, // Tiêu đề biểu đồ
                position: 'top',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                padding: {
                    top: 10,
                    bottom: 20
                }
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



// ----------------------------
// Lấy dữ liệu JSON từ phần tử script
var scoreCompletionData = JSON.parse(document.getElementById("score-completion").textContent);

// Kiểm tra dữ liệu đã truyền
console.log(scoreCompletionData);

// Chuẩn bị dữ liệu cho biểu đồ
var scores = scoreCompletionData.map(d => d.score); // Điểm số
var completionRates = scoreCompletionData.map(d => d.completion_rate); // Tỷ lệ hoàn thành

// Vẽ biểu đồ bằng Chart.js
var ctx = document.getElementById('scoreCompletionChart').getContext('2d');
new Chart(ctx, {
    type: 'scatter', // Biểu đồ scatter
    data: {
        datasets: [{
            label: 'Score vs Completion Rate',
            data: scoreCompletionData.map(d => ({ x: d.completion_rate, y: d.score })), // Dữ liệu {x, y}
            backgroundColor: 'rgba(75, 192, 192, 0.6)', // Màu sắc
        }]
    },
    options: {
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Completion Rate (%)'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Score'
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `Rate: ${context.raw.x}%, Score: ${context.raw.y}`;
                    }
                }
            }
        }
    }
});




// Lấy dữ liệu từ JSON script
var courseStats = JSON.parse(document.getElementById("specific-info").textContent);

// Chuẩn bị dữ liệu
var labels = ['Enrollment Count', 'Average Score', 'Pass Rate']; // Nhãn trục X
var dataValues = [courseStats.enroll_count, courseStats.average_score, courseStats.pass_rate]; // Giá trị trục Y
var backgroundColors = ['#4caf50', '#2196f3', '#f44336']; // Màu sắc các cột

// Vẽ biểu đồ bằng Chart.js
var ctx = document.getElementById('courseStatsChart').getContext('2d');
new Chart(document.getElementById('courseStatsChart'), {
    type: 'bar',
    data: {
        labels: ['Enrollment Count', 'Average Score', 'Pass Rate'],
        datasets: [
            {
                label: 'Enrollment Count',
                data: [courseStats.enrollment_count, 0, 0], // Dữ liệu Enrollment Count
                backgroundColor: 'rgba(75, 192, 192, 0.6)', // Màu cột Enrollment
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                yAxisID: 'y',
            },
            {
                label: 'Average Score',
                data: [0, courseStats.average_score, 0], // Dữ liệu Average Score
                backgroundColor: 'rgba(255, 99, 132, 0.6)', // Màu cột Average Score
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                yAxisID: 'y1',
            },
            {
                label: 'Pass Rate',
                data: [0, 0, courseStats.pass_rate], // Dữ liệu Pass Rate
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Màu cột Pass Rate
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                yAxisID: 'y1',
            },
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: false,
                text: 'Course Statistics',
                position:'bottom',
                font: {
                    size: 18,
                    weight: 'bold',
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        if (context.dataset.label === 'Enrollment Count') {
                            return `Enrollments: ${context.raw}`;
                        } else if (context.dataset.label === 'Average Score') {
                            return `Average Score: ${context.raw}`;
                        } else if (context.dataset.label === 'Pass Rate') {
                            return `Pass Rate: ${context.raw}%`;
                        }
                        return null;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                position: 'left', // Trục Y bên trái
                title: {
                    display: true,
                    text: 'Enrollment Count',
                }
            },
            y1: {
                beginAtZero: true,
                position: 'right', // Trục Y bên phải
                title: {
                    display: true,
                    text: 'Average Score / Pass Rate (%)',
                },
                grid: {
                    drawOnChartArea: false, // Không vẽ lưới từ y1
                }
            }
        }
    }
});