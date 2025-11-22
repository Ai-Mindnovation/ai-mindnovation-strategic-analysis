/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, useRef } from "@odoo/owl";

/**
 * Widget para gráfico DOFA (Pie Chart)
 */
class DofaPieChart extends Component {
    setup() {
        this.chartRef = useRef("dofaCanvas");
        this.chartInstance = null;

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.chartRef.el;
        if (!ctx) return;

        const props = this.props.record.data;
        
        // Destruir instancia previa si existe
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        this.chartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Fortalezas', 'Debilidades', 'Oportunidades', 'Amenazas'],
                datasets: [{
                    data: [
                        props.dofa_fortalezas || 0,
                        props.dofa_debilidades || 0,
                        props.dofa_oportunidades || 0,
                        props.dofa_amenazas || 0
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',   // Verde - Fortalezas
                        'rgba(255, 193, 7, 0.7)',   // Amarillo - Debilidades
                        'rgba(0, 123, 255, 0.7)',   // Azul - Oportunidades
                        'rgba(220, 53, 69, 0.7)'    // Rojo - Amenazas
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(0, 123, 255, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            font: { size: 14 },
                            padding: 15
                        }
                    },
                    title: {
                        display: true,
                        text: 'Distribución DOFA',
                        font: { size: 18, weight: 'bold' }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
}

DofaPieChart.template = "ai_mindnovation_analysis.DofaPieChart";

/**
 * Widget para gráfico SPACE (Radar Chart)
 */
class SpaceRadarChart extends Component {
    setup() {
        this.chartRef = useRef("spaceCanvas");
        this.chartInstance = null;

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.chartRef.el;
        if (!ctx) return;

        const props = this.props.record.data;
        const tipo = this.props.tipo || 'tradicional'; // 'tradicional' o 'ponderado'
        
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        const prefix = tipo === 'tradicional' ? 'space_trad_' : 'space_pond_';
        
        const competitiva = Math.abs(props[prefix + 'competitiva'] || 0);
        const financiera = Math.abs(props[prefix + 'financiera'] || 0);
        const industria = Math.abs(props[prefix + 'industria'] || 0);
        const entorno = Math.abs(props[prefix + 'entorno'] || 0);

        this.chartInstance = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Competitiva', 'Financiera', 'Industria', 'Entorno'],
                datasets: [{
                    label: `SPACE ${tipo === 'tradicional' ? 'Tradicional' : 'Ponderado'}`,
                    data: [competitiva, financiera, industria, entorno],
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                        grid: { color: 'rgba(0, 0, 0, 0.1)' },
                        pointLabels: {
                            font: { size: 14, weight: 'bold' }
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1,
                            backdropColor: 'rgba(255, 255, 255, 0.75)'
                        },
                        min: 0,
                        max: 5
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: `Análisis SPACE ${tipo === 'tradicional' ? 'Tradicional' : 'Ponderado'}`,
                        font: { size: 18, weight: 'bold' }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.r.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    }
}

SpaceRadarChart.template = "ai_mindnovation_analysis.SpaceRadarChart";

/**
 * Widget para gráfico McKinsey (Scatter Chart con matriz 3x3)
 */
class McKinseyScatterChart extends Component {
    setup() {
        this.chartRef = useRef("mckinseyCanvas");
        this.chartInstance = null;

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.chartRef.el;
        if (!ctx) return;

        const props = this.props.record.data;
        
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        const interno = props.mckinsey_prom_internas || 2.5;
        const externo = props.mckinsey_prom_externas || 2.5;

        this.chartInstance = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Posición Estratégica',
                    data: [{
                        x: externo,
                        y: interno
                    }],
                    backgroundColor: 'rgba(255, 99, 132, 0.8)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointRadius: 12,
                    pointHoverRadius: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        min: 0,
                        max: 5,
                        title: {
                            display: true,
                            text: 'Factores Externos (Industria + Entorno)',
                            font: { size: 14, weight: 'bold' }
                        },
                        ticks: {
                            stepSize: 1
                        },
                        grid: {
                            color: function(context) {
                                // Líneas de división de matriz
                                if (context.tick.value === 2 || context.tick.value === 3) {
                                    return 'rgba(0, 0, 0, 0.5)';
                                }
                                return 'rgba(0, 0, 0, 0.1)';
                            },
                            lineWidth: function(context) {
                                if (context.tick.value === 2 || context.tick.value === 3) {
                                    return 2;
                                }
                                return 1;
                            }
                        }
                    },
                    y: {
                        min: 0,
                        max: 5,
                        title: {
                            display: true,
                            text: 'Factores Internos (Competitiva + Financiera)',
                            font: { size: 14, weight: 'bold' }
                        },
                        ticks: {
                            stepSize: 1
                        },
                        grid: {
                            color: function(context) {
                                if (context.tick.value === 2 || context.tick.value === 3) {
                                    return 'rgba(0, 0, 0, 0.5)';
                                }
                                return 'rgba(0, 0, 0, 0.1)';
                            },
                            lineWidth: function(context) {
                                if (context.tick.value === 2 || context.tick.value === 3) {
                                    return 2;
                                }
                                return 1;
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Matriz McKinsey (Interna-Externa)',
                        font: { size: 18, weight: 'bold' }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const x = context.parsed.x.toFixed(2);
                                const y = context.parsed.y.toFixed(2);
                                return [`Externos: ${x}`, `Internos: ${y}`];
                            }
                        }
                    }
                }
            }
        });
    }
}

McKinseyScatterChart.template = "ai_mindnovation_analysis.McKinseyScatterChart";

/**
 * Widget para gráfico Valor Percibido (Radar multi-línea)
 */
class ValorPercibidoRadarChart extends Component {
    setup() {
        this.chartRef = useRef("valorPercibidoCanvas");
        this.chartInstance = null;

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.chartRef.el;
        if (!ctx) return;

        const props = this.props.record.data;
        
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        // Obtener variables y competidores desde el registro
        const variables = props.analysis_variable_ids || [];
        const competidores = props.competitor_ids || [];

        if (variables.length === 0) {
            // Sin variables, mostrar mensaje
            ctx.getContext('2d').clearRect(0, 0, ctx.width, ctx.height);
            return;
        }

        // Preparar labels (palabras clave de variables)
        const labels = variables.map(v => v.palabras_clave || 'Variable');
        
        // Dataset empresa (desempeño)
        const empresaData = variables.map(v => v.media_desemp || 0);
        
        // Datasets competidores
        const competidoresDatasets = competidores.map((comp, idx) => {
            const colores = [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ];
            
            return {
                label: comp.name || `Competidor ${idx + 1}`,
                data: comp.competitor_value_ids?.map(cv => cv.value) || [],
                fill: true,
                backgroundColor: colores[idx % colores.length],
                borderColor: colores[idx % colores.length].replace('0.5', '1'),
                pointBackgroundColor: colores[idx % colores.length].replace('0.5', '1'),
                pointBorderColor: '#fff',
                pointRadius: 4,
                borderWidth: 2
            };
        });

        // Dataset mercado (promedio de competidores)
        const mercadoData = variables.map((v, idx) => {
            const valoresComp = competidores.map(comp => {
                const valor = comp.competitor_value_ids?.[idx]?.value || 0;
                return valor;
            });
            return valoresComp.length > 0 
                ? valoresComp.reduce((a, b) => a + b, 0) / valoresComp.length 
                : 0;
        });

        this.chartInstance = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Empresa',
                        data: empresaData,
                        fill: true,
                        backgroundColor: 'rgba(40, 167, 69, 0.2)',
                        borderColor: 'rgb(40, 167, 69)',
                        pointBackgroundColor: 'rgb(40, 167, 69)',
                        pointBorderColor: '#fff',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        borderWidth: 3
                    },
                    ...competidoresDatasets,
                    {
                        label: 'Promedio Mercado',
                        data: mercadoData,
                        fill: false,
                        backgroundColor: 'rgba(108, 117, 125, 0.2)',
                        borderColor: 'rgb(108, 117, 125)',
                        borderDash: [5, 5],
                        pointBackgroundColor: 'rgb(108, 117, 125)',
                        pointBorderColor: '#fff',
                        pointRadius: 4,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                        grid: { color: 'rgba(0, 0, 0, 0.1)' },
                        pointLabels: {
                            font: { size: 12 }
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1,
                            backdropColor: 'rgba(255, 255, 255, 0.75)'
                        },
                        min: 0,
                        max: 5
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 12 },
                            padding: 10
                        }
                    },
                    title: {
                        display: true,
                        text: 'Análisis de Valor Percibido',
                        font: { size: 18, weight: 'bold' }
                    }
                }
            }
        });
    }
}

ValorPercibidoRadarChart.template = "ai_mindnovation_analysis.ValorPercibidoRadarChart";

// Registrar los widgets
registry.category("fields").add("dofa_pie_chart", DofaPieChart);
registry.category("fields").add("space_radar_chart", SpaceRadarChart);
registry.category("fields").add("mckinsey_scatter_chart", McKinseyScatterChart);
registry.category("fields").add("valor_percibido_radar_chart", ValorPercibidoRadarChart);
