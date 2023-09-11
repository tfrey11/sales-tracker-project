fetch('/sales_this_month_dealer.json')
.then(response => response.json())
.then(responseJson => {
    const data = responseJson.data.map(dailyTotal => ({
        x: dailyTotal.date, y: dailyTotal.total,
    }));
    new Chart(document.querySelector('#dealer-sales'), {
        type: 'line',
        data: {
            datasets: [{
                label: 'Dealer Sales This Month',
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
                    borderColor: "black",
                },
            },
            plugins:{
                legend:{
                    display: false
                }, 
                title:{
                    display: true,
                    text: 'Monthly sales',
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
                        color:'white',
                        tickColor:'black'
                    },
                    ticks:{
                        color:'black',
                        font:{
                            weight: 'bolder'
                        }
                    }
                },

                x: {
                    type: 'time',
                    
                    time: {
                        tooltipFormat: 'LLLL dd', unit: 'day',
                    },
                    grid:{
                        color:'white'
                    },
                    ticks:{
                        color:'black',
                        font:{
                            weight: 'bolder',
                        }

                    }
                }
                    
            },
            
        },
    });
});