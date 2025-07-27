class DashboardCharts {
    constructor() {
        this.init();
    }

    init() {
        this.initPipelineChart();
        this.initProjectStatusChart();
        this.initRevenueGrowthChart();
    }

    initPipelineChart() {
        const pipelineElement = document.getElementById('pipeline-chart');
        if (!pipelineElement) {
            console.log('Pipeline chart element not found');
            return;
        }

        // Get data from window object (set by Django template)
        const pipelineData = window.pipelineData || {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            series: [0, 0, 0, 0, 0, 0]
        };

        // Validate data structure
        if (!pipelineData.labels || !pipelineData.series) {
            console.error('Invalid pipeline data structure:', pipelineData);
            return;
        }

        // Ensure series is an array
        const seriesData = Array.isArray(pipelineData.series) ? pipelineData.series : [0];

        const pipelineOptions = {
            series: [{
                name: 'Revenue',
                data: seriesData
            }],
            chart: {
                type: 'line',
                height: 320,
                toolbar: {
                    show: false
                },
                foreColor: '#adb0bb',
                fontFamily: 'inherit'
            },
            colors: ['#5D87FF'],
            stroke: {
                curve: 'smooth',
                width: 3
            },
            markers: {
                size: 6,
                colors: ['#5D87FF'],
                strokeColors: '#fff',
                strokeWidth: 2,
                hover: {
                    size: 8
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: pipelineData.labels,
                labels: {
                    style: {
                        cssClass: 'grey--text lighten-2--text fill-color'
                    }
                }
            },
            yaxis: {
                title: {
                    text: 'Revenue (PKR)'
                },
                labels: {
                    style: {
                        cssClass: 'grey--text lighten-2--text fill-color'
                    },
                    formatter: function(value) {
                        return 'PKR ' + value.toLocaleString();
                    }
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: 'vertical',
                    shadeIntensity: 0.3,
                    gradientToColors: ['#5D87FF'],
                    inverseColors: false,
                    opacityFrom: 0.7,
                    opacityTo: 0.1,
                    stops: [0, 100]
                }
            },
            tooltip: {
                theme: 'dark',
                y: {
                    formatter: function (val) {
                        return 'PKR ' + val.toLocaleString()
                    }
                }
            },
            grid: {
                borderColor: 'rgba(0,0,0,0.1)',
                strokeDashArray: 3,
                xaxis: {
                    lines: {
                        show: false
                    }
                }
            }
        };

        try {
            const pipelineChart = new ApexCharts(pipelineElement, pipelineOptions);
            pipelineChart.render();
        } catch (error) {
            console.error('Error rendering pipeline chart:', error);
        }
    }

    initProjectStatusChart() {
        const projectStatusElement = document.getElementById('project-status-chart');
        if (!projectStatusElement) {
            console.log('Project status chart element not found');
            return;
        }

        // Get data from window object (set by Django template)
        const projectStats = window.projectStats || {
            total: 0,
            active: 0,
            completed: 0,
            proposal: 0
        };

        // Validate data
        if (typeof projectStats.total === 'undefined') {
            console.error('Invalid project stats data:', projectStats);
            return;
        }

        const projectStatusOptions = {
            series: [projectStats.active, projectStats.completed, projectStats.proposal],
            chart: {
                type: 'donut',
                height: 320,
                toolbar: {
                    show: false
                }
            },
            colors: ['#FFA726', '#66BB6A', '#42A5F5'],
            labels: ['In Progress', 'Completed', 'Proposal'],
            dataLabels: {
                enabled: true,
                formatter: function (val, opts) {
                    return opts.w.globals.seriesTotals[opts.seriesIndex];
                },
                style: {
                    fontSize: '14px',
                    fontFamily: 'inherit',
                    fontWeight: 'bold'
                }
            },
            legend: {
                position: 'bottom',
                fontSize: '12px',
                fontFamily: 'inherit'
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '60%',
                        labels: {
                            show: true,
                            name: {
                                show: true,
                                fontSize: '14px',
                                fontFamily: 'inherit',
                                fontWeight: 600,
                                color: '#6c757d'
                            },
                            value: {
                                show: true,
                                fontSize: '16px',
                                fontFamily: 'inherit',
                                fontWeight: 700,
                                color: '#495057'
                            },
                            total: {
                                show: true,
                                label: 'Total',
                                fontSize: '14px',
                                fontFamily: 'inherit',
                                fontWeight: 600,
                                color: '#6c757d',
                                formatter: function (w) {
                                    return w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                                }
                            }
                        }
                    }
                }
            },
            tooltip: {
                theme: 'dark',
                y: {
                    formatter: function (val) {
                        return val + ' projects';
                    }
                }
            }
        };

        try {
            const projectStatusChart = new ApexCharts(projectStatusElement, projectStatusOptions);
            projectStatusChart.render();
        } catch (error) {
            console.error('Error rendering project status chart:', error);
        }
    }

    initRevenueGrowthChart() {
        const growthElement = document.getElementById('revenue-growth-chart');
        if (!growthElement) return;

        // Get data from window object (set by Django template)
        const growthData = window.revenueGrowthData || {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            actual: [0, 0, 0, 0, 0, 0],
            expenses: [0, 0, 0, 0, 0, 0],
            netProfit: [0, 0, 0, 0, 0, 0],
            target: [0, 0, 0, 0, 0, 0]
        };

        // Validate data structure
        if (!growthData.labels || !growthData.actual || !growthData.expenses || !growthData.netProfit || !growthData.target) {
            console.error('Invalid revenue growth data structure:', growthData);
            return;
        }

        const growthOptions = {
            series: [
                {
                    name: 'Revenue',
                    data: growthData.actual,
                    type: 'column'
                },
                {
                    name: 'Expenses',
                    data: growthData.expenses,
                    type: 'column'
                },
                {
                    name: 'Net Profit',
                    data: growthData.netProfit,
                    type: 'line'
                },
                {
                    name: 'Target',
                    data: growthData.target,
                    type: 'line'
                }
            ],
            chart: {
                type: 'line',
                height: 350,
                stacked: false,
                toolbar: {
                    show: false
                },
                foreColor: '#adb0bb',
                fontFamily: 'inherit'
            },
            colors: ['#5D87FF', '#FF6B6B', '#66BB6A', '#FFA726'],
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '40%',
                    borderRadius: 4
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: [0, 0, 3, 3],
                curve: 'smooth'
            },
            xaxis: {
                categories: growthData.labels,
                labels: {
                    style: {
                        cssClass: 'grey--text lighten-2--text fill-color'
                    }
                }
            },
            yaxis: {
                title: {
                    text: 'Amount (PKR)'
                },
                labels: {
                    style: {
                        cssClass: 'grey--text lighten-2--text fill-color'
                    },
                    formatter: function(value) {
                        return 'PKR ' + value.toLocaleString();
                    }
                }
            },
            fill: {
                opacity: [1, 1, 1, 1],
                gradient: {
                    inverseColors: false,
                    shade: 'light',
                    type: 'vertical',
                    opacityFrom: 0.85,
                    opacityTo: 0.55,
                    stops: [0, 100, 100, 100]
                }
            },
            tooltip: {
                theme: 'dark',
                y: {
                    formatter: function (val) {
                        return 'PKR ' + val.toLocaleString()
                    }
                }
            },
            grid: {
                borderColor: 'rgba(0,0,0,0.1)',
                strokeDashArray: 3,
                xaxis: {
                    lines: {
                        show: false
                    }
                }
            },
            legend: {
                position: 'top',
                horizontalAlign: 'right',
                fontFamily: 'inherit',
                fontSize: '12px'
            }
        };

        try {
            const growthChart = new ApexCharts(growthElement, growthOptions);
            growthChart.render();
        } catch (error) {
            console.error('Error initializing revenue growth chart:', error);
        }
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new DashboardCharts();
}); 