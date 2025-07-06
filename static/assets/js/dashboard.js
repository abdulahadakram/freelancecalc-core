$(function () {


    // =====================================
    // Profit
    // =====================================
    var chart = {
        series: [
            {
                name: "Earnings",
                data: [0, 1000, 1500, 2000, 2400, 2700, 2900, 3000], // Earnings gradually increasing towards the target
            },
            {
                name: "Target",
                data: [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000], // Constant target of $3000
            },
        ],

        chart: {
            type: "line",
            height: 345,
            offsetX: -15,
            toolbar: {show: false},
            foreColor: "#adb0bb",
            fontFamily: 'inherit',
            sparkline: {enabled: false},
        },

        colors: ["#5D87FF", "#81be76"],

        stroke: {
            show: true,
            width: [2, 3],
            curve: "smooth",
            colors: ["#5D87FF", "#81be76"],
            dashArray: [5, 0], // Dashed line for the earnings, solid line for the target
        },

        dataLabels: {
            enabled: false,
        },

        legend: {
            show: false,
        },

        grid: {
            borderColor: "rgba(0,0,0,0.1)",
            strokeDashArray: 3,
            xaxis: {
                lines: {
                    show: false,
                },
            },
        },

        xaxis: {
            type: "category",
            categories: ["16/08", "17/08", "18/08", "19/08", "20/08", "21/08", "22/08", "23/08"], // Dates when the projects were completed
            labels: {
                style: {cssClass: "grey--text lighten-2--text fill-color"},
            },
        },

        yaxis: {
            show: true,
            min: 0,
            max: 3500, // Max value slightly above the target
            tickAmount: 7, // Adjusted for better granularity
            labels: {
                formatter: function (value) {
                    return "$" + value; // Adding the $ sign to represent money
                },
                style: {
                    cssClass: "grey--text lighten-2--text fill-color",
                },
            },
        },

        tooltip: {
            theme: "light",
            y: {
                formatter: function (value) {
                    return "$" + value; // Adding $ sign to the tooltip
                }
            }
        },

        responsive: [
            {
                breakpoint: 600,
                options: {
                    chart: {
                        height: 300,
                    },
                    markers: {
                        size: 3,
                    },
                }
            }
        ]
    };

    var chart = new ApexCharts(document.querySelector("#chart"), chart);
    chart.render();


    // =====================================
    // Breakup
    // =====================================
    var breakup = {
        color: "#adb5bd",
        series: [38, 40, 25],
        labels: ["2022", "2021", "2020"],
        chart: {
            width: 180,
            type: "donut",
            fontFamily: "Plus Jakarta Sans', sans-serif",
            foreColor: "#adb0bb",
        },
        plotOptions: {
            pie: {
                startAngle: 0,
                endAngle: 360,
                donut: {
                    size: '75%',
                },
            },
        },
        stroke: {
            show: false,
        },

        dataLabels: {
            enabled: false,
        },

        legend: {
            show: false,
        },
        colors: ["#5D87FF", "#ecf2ff", "#F9F9FD"],

        responsive: [
            {
                breakpoint: 991,
                options: {
                    chart: {
                        width: 150,
                    },
                },
            },
        ],
        tooltip: {
            theme: "dark",
            fillSeriesColor: false,
        },
    };

    var chart = new ApexCharts(document.querySelector("#breakup"), breakup);
    chart.render();


    // =====================================
    // Earning
    // =====================================
    var earning = {
        chart: {
            id: "sparkline3",
            type: "area",
            height: 60,
            sparkline: {
                enabled: true,
            },
            group: "sparklines",
            fontFamily: "Plus Jakarta Sans', sans-serif",
            foreColor: "#adb0bb",
        },
        series: [
            {
                name: "Earnings",
                color: "#49BEFF",
                data: [25, 66, 20, 40, 12, 58, 20],
            },
        ],
        stroke: {
            curve: "smooth",
            width: 2,
        },
        fill: {
            colors: ["#f3feff"],
            type: "solid",
            opacity: 0.05,
        },

        markers: {
            size: 0,
        },
        tooltip: {
            theme: "dark",
            fixed: {
                enabled: true,
                position: "right",
            },
            x: {
                show: false,
            },
        },
    };
    new ApexCharts(document.querySelector("#earning"), earning).render();
})