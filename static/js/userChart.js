

fetch('/sales_this_month_user.json')
.then(response => response.json())
.then(responseJson => {
    const data = responseJson.data.map(dailyTotal => ({
        x: dailyTotal.date, y: dailyTotal.total,
    }));
    new Chart(document.querySelector('#month_sales_chart'), {
        type: 'line',
        data: {
            datasets: [{
                label: 'Sales This Month',
                data,
                fill: false,
                spanGaps: 1000 * 60 * 60 * 24
                
            }],
        },
        options:{
            responsive: true,
            interaction:{
                mode: 'nearest',
            },
            elements: {
                line: {
                    borderColor: "black", 
                    
                },
            },
            plugins: {
                legend: {
                    display:false,
                },
                title: {
                    display: true,
                    text: 'Monthly Sales',
                    color: 'black',
                    font: {
                        size: '20rem'
                    }
                }
            },

            scales: {
                y:{
                    type: 'linear',
                    beginAtZero: true,
                    grid:{
                        color: 'white',
                        
                    },
                    ticks: {
                        color: 'black',
                        font: {
                            weight: 'bolder',
                            size: '15rem'
                        }
                    }
                },

                x: {
                    type: 'time',
                    
                    time: {
                        tooltipFormat: 'LLLL dd', unit: 'day',
                    },
                    grid: {
                        color: 'white',
                    },
                    ticks: {
                        color: 'black',
                        font: {
                            weight: 'bolder',
                            size: '15rem'
                        }
                    }
                }
                    
            },
            
        },
    });
});