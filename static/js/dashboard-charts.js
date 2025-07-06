// Dashboard Charts Configuration
class DashboardCharts {
    constructor() {
        this.pipelineData = null;
        this.projectStats = null;
        this.init();
    }

    init() {
        // Get data from global variables set in template
        this.pipelineData = window.pipelineData || [];
        this.projectStats = window.projectStats || {};
        
        this.initPipelineChart();
        this.initProjectStatsChart();
    }

    initPipelineChart() {
        if (!this.pipelineData || this.pipelineData.length === 0) {
            console.log('No pipeline data available');
            return;
        }

        const pipelineOptions = {
            series: [{
                name: 'Payments',
                data: this.pipelineData.map(item => item.amount)
            }],
            chart: {
                type: 'area',
                height: 350,
                toolbar: {
                    show: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 3
            },
            colors: ['#556ee6'],
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.2,
                    stops: [0, 90, 100]
                }
            },
            xaxis: {
                categories: this.pipelineData.map(item => item.month)
            },
            yaxis: {
                labels: {
                    formatter: function(value) {
                        return value.toLocaleString() + ' PKR';
                    }
                }
            },
            tooltip: {
                y: {
                    formatter: function(value) {
                        return value.toLocaleString() + ' PKR';
                    }
                }
            },
            noData: {
                text: 'No payment data available',
                align: 'center',
                verticalAlign: 'middle',
                offsetX: 0,
                offsetY: 0,
                style: {
                    color: '#666',
                    fontSize: '14px'
                }
            }
        };

        const chartElement = document.querySelector("#payment-pipeline-chart");
        if (chartElement) {
            const pipelineChart = new ApexCharts(chartElement, pipelineOptions);
            pipelineChart.render();
        }
    }

    initProjectStatsChart() {
        if (!this.projectStats || Object.keys(this.projectStats).length === 0) {
            console.log('No project stats data available');
            return;
        }

        // Ensure we have valid numbers
        const active = this.projectStats.active || 0;
        const completed = this.projectStats.completed || 0;
        const proposal = this.projectStats.proposal || 0;

        const projectOptions = {
            series: [active, completed, proposal],
            chart: {
                type: 'donut',
                height: 250
            },
            labels: ['Active', 'Completed', 'Proposal'],
            colors: ['#f1b44c', '#34c38f', '#556ee6'],
            legend: {
                position: 'bottom'
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '70%'
                    }
                }
            },
            noData: {
                text: 'No project data available',
                align: 'center',
                verticalAlign: 'middle',
                offsetX: 0,
                offsetY: 0,
                style: {
                    color: '#666',
                    fontSize: '14px'
                }
            }
        };

        const chartElement = document.querySelector("#project-stats-chart");
        if (chartElement) {
            const projectChart = new ApexCharts(chartElement, projectOptions);
            projectChart.render();
        }
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new DashboardCharts();
}); 