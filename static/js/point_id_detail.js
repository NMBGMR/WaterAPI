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
$('#pointidtable').DataTable({select: {style: 'multi'},
                            paging: false,
                            ordering: false,
                            info: false,
                            searching: false,
                            columns: [
                                      {data: "key"},
                                      {data: "value"},
                                      // {data: "name"},
                                      // {data: "description"},
                                      // {data: "thingname"},
                                      // {data: "source"}
                            ]})

const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
})

const macrostrat = L.tileLayer('http://tiles.macrostrat.org/carto/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="https://macrostrat.org">MacroStrat</a> contributors'
})

const opentopo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)\''
})


const esri_wi = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    {attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'})

const usgs = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}',
    {attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'})


const map = L.map('map_detail', {
        preferCanvas: true,
        updateWhenZooming: false,
        updateWhenIdle: true,
        layers: [osm]
    }
)
let layerControl = L.control.layers({"OpenStreetMap": osm,
    'MacroStrat': macrostrat,
    'OpenTopo': opentopo,
    "ESRI World Imagery": esri_wi,
    'USGS National Basemap': usgs
    }, null).addTo(map)

function chartInit(config, point_id){

    fetch(config.base_api_url+'locations?point_id='+point_id).then(resp=>resp.json()).then((data)=>{
        let location =data.items[0]
        let latlng =[location.latitude, location.longitude]
        map.setView(latlng, 8);
        let marker = L.circleMarker(latlng,{radius: 5})
        marker.addTo(map)
    })
    fetch(config.base_api_url+'wells?point_id='+point_id).then(resp=>resp.json()).then((data)=>{
        console.log('ddd', data)
        populate_selection_table(data.items[0], point_id, '#pointidtable')
    })

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