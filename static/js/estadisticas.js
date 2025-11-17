fetch("/api/estadisticas")
    .then(res => res.json())
    .then(data => {
        const fechas = data.por_dia.map(d => {
            const date = new Date(d.fecha);
            return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1)
        .toString()
        .padStart(2, '0')}`;
        });
        const cantidades = data.por_dia.map(d => d.cantidad);

        Highcharts.chart("chartPorDia", {
            chart: { type: "line" },
            title: { text: "Aviso agregados por dia" },
            xAxis: { categories: fechas, title: {text: "Día"} },
            yAxis: { title: { text: "Cantidad de avisos"} },
            series: [{ name: "Aviso", data: cantidades }],
            credits: { enabled: false }

        });

        const tortaData = data.por_tipo.map(d => ({ name: d.tipo, y: d.cantidad}));

        Highcharts.chart("chartPorTipo", {
            chart: { type: "pie" },
            title: { text: "Distribucion por tipo de mascota"},
            series: [{
                name: "Cantidad",
                colorByPoint: true,
                data: tortaData
            }],
            credits: { enabled: false }
        });

        const meses = [...new Set(data.por_mes_tipo.map(d=> d.mes))].sort((a, b) => a - b);
        const nombresMeses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        const gatos = meses.map(m => {
            const item = data.por_mes_tipo.find(d => d.mes === m && d.tipo === "gato");
            return item ? item.cantidad : 0;
        });

        const perros = meses.map(m => {
            const item = data.por_mes_tipo.find(d => d.mes === m && d.tipo === "perro");
            return item ? item.cantidad : 0;
        });

        Highcharts.chart("chartPorMesTipo", {
            chart: { type: "column" },
            title: { text: "Aviso por mes y tipo" },
            xAxis: {
                categories: meses.map(m => `${nombresMeses[m - 1]}`),
                title: { text: "Mes" }
            },
            yAxis: {
                min: 0,
                title: { text: "Cantidad de avisos" }

            },
            plotOptions: { column: { grouping: true, shadow: false, borderWidth: 0} },
            series: [
                { name: "Gatos", data: gatos, color: "#FF69B4" },
                { name: "Perros", data: perros, color: "#053155ff" }
            ],
            credits: { enabled: false }

        });
    })

    .catch(err => {
        console.error("Error al cargar estadisticas:", err);
        alert("No se pudieron cargas las estadisticas");
    });