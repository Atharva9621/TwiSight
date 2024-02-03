var ctx2 = document.getElementById('myPieChart').getContext('2d');
var sample_data = {
    labels: ['Negative', 'Neutral', 'Positive'],
    values: [12, 19, 32]
};
sample_data = tweetData;
var myPieChart = new Chart(ctx2, {
    type: 'pie', // Specify the type of chart (pie chart)
    data: {
        labels: sample_data.labels, // Provide labels for the segments
        datasets: [{
            label: 'My Dataset', // Provide a label for the dataset
            data: sample_data.values, // Provide the data for the segments
            backgroundColor: [ // Specify the background colors for the segments
                'rgba(255, 99, 132, 0.5)', // Red
                'rgba(255, 206, 86, 0.5)', // Yellow
                'rgba(75, 192, 192, 0.5)', // Green
            ],  
            borderColor: [ // Specify the border colors for the segments
                'rgba(255, 99, 132, 1)', // Red
                'rgba(255, 150, 86, 1)', // Orange
                'rgba(75, 192, 192, 1)', // Green
            ],
            borderWidth: 1 // Specify the border width for the segments
        }]
    },
    options: {
        // Additional options (e.g., title, legend) can be specified here
    }
});
