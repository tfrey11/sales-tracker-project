

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
                
            }],
        },
        options:{
            responsive: true,
            interaction:{
                mode: 'nearest',
            },
            elements: {
                line: {
                    
                },
            },

            scales: {
                y:{
                    type: 'linear',
                    beginAtZero: true
                },

                x: {
                    type: 'time',
                    
                    time: {
                        tooltipFormat: 'LLLL dd', unit: 'day',
                    },
                }
                    
            },
            
        },
    });
});