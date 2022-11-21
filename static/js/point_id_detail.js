const ytitle = 'Depth to Water (ft BGS)'

const yAxis =  {
                    position: "left",
                    reverse: true,
                    // beginAtZero: true,
                    title: {text: ytitle, display: true}

                }
const xAxis = {
                    position: "bottom",
                    type: "time",
                    title: {text: "Time", display: true}
                }
const options = {scales: {yAxis: yAxis,
                          xAxis: xAxis},
                 animation: {
        duration: 0
    }}

const myChart = new Chart(document.getElementById('chartdiv').getContext('2d'), {type: 'line',
                                    data: {labels: [], datasets:[]},
        options: options
    })

const obsdtt =  $('#obstable').DataTable(
                                {'columns': [
                                            // {'data': 'locationname'},
                                             {'data': 'timestamp'},
                                            {'data': 'value',
                                                'render': $.fn.dataTable.render.number('', '.', 2, '')}]})

function chartInit(config, point_id){

    let url =config.base_api_url+'waterlevels?point_id='+point_id
    $('#chartprogress').show()
    retrieveItems(url, 20000, (measurements)=>updateChart(point_id, measurements))

}

function updateChart(point_id, measurements){

    obsdtt.rows.add(measurements).draw()

    let color = 'black'
         let ndata = [{
                // iot: {'Datastream': ds,
                //           'Thing': thing,
                //           'Location': {'name': name,
                //                         '@iot.id': iotid,
                //                         'url': locationURL,
                //                         'location': data['location']},
                //           'sourceURL': url,
                //           'source': m.source},
                    label: point_id,
                    data: measurements.map(f=>{
                        var d = new Date(f['timestamp'])
                        // d.setHours(d.getHours()+6)
                        return [d, f['value']]
                    }),
                    borderColor: color,
                    backgroundColor: color,
                    tension: 0.1
                }]

            // datasets.push(ndata)
            myChart.data.datasets=ndata
            myChart.update()
            // div.classList.remove('spinner')
            // let div = document.getElementById("chartoverlay")
            // div.style.display="block"
            // console.log(evt.originalEvent.clientY, evt.originalEvent.clientY+20+'px')
            // div.style.top = evt.originalEvent.clientY+20+'px'
            // div.style.left = evt.originalEvent.clientX+20+'px'

            $('#chartprogress').hide()


}