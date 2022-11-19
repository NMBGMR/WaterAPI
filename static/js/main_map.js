//
// const gwlyAxis =  {
//                     position: "left",
//                     reverse: true,
//                     // beginAtZero: true,
//                     title: {text:  "Depth to Water (ft BGS)", display: true}
//
//                 }
//
// const dischargeyAxis =  {
//                     position: "left",
//                     reverse: false,
//                     // beginAtZero: true,
//                     title: {text:  "Discharge (cfs)", display: true}
//
//                 }
// const gageyAxis =  {
//                     position: "left",
//                     reverse: false,
//                     // beginAtZero: true,
//                     title: {text:  "Gage Height (ft)", display: true}
//
//                 }
// const xAxis = {
//                     position: "bottom",
//                     type: "time",
//                     title: {text: "Time", display: true}
//                 }
// const gwloptions = {scales: {yAxis: gwlyAxis,
//                           xAxis: xAxis},
//                  animation: {
//         duration: 0
//     }}
//
// const dischargeoptions = {scales: {yAxis: dischargeyAxis,
//                           xAxis: xAxis},
//                  animation: {
//         duration: 0
//     }}
//
// const gageoptions = {scales: {yAxis: gageyAxis,
//                           xAxis: xAxis},
//                  animation: {
//         duration: 0
//     }}
//
// const gwlChart = new Chart(document.getElementById('gwlchart').getContext('2d'), {type: 'line',
//                                     data: {labels: [], datasets:[]},
//         options: gwloptions
//     })
//
// const dischargeChart = new Chart(document.getElementById('dischargechart').getContext('2d'), {type: 'line',
//                                     data: {labels: [], datasets:[]},
//         options: dischargeoptions
//     })
// const gageChart = new Chart(document.getElementById('gagechart').getContext('2d'), {type: 'line',
//                                     data: {labels: [], datasets:[]},
//         options: gageoptions
//     })
//
// $('#chartprogress').hide()
//
// function toggleLocation(layer){
//     function deselect(chart, chartid){
//         chart.data.datasets = chart.data.datasets.filter(function(d){
//             return !(d.label === name)
//             })
//         chart.update()
//         layer.setStyle({color: layer.defaultColor,
//                         fillColor: layer.defaultColor})
//         console.log(chart.data.datasets, chart.data.datasets.empty)
//         if (!chart.data.datasets.length){
//             document.getElementById(chartid).style.setProperty("display", "none")
//         }
//     }
//
//     let iotid = layer.stid
//     let name = layer.name
//     if (gwlChart.data.datasets.map(function(d){
//         return d.label
//     }).includes(name)){
//         deselect(gwlChart, 'gwl')
//     } else if (dischargeChart.data.datasets.map(function(d){
//         return d.label
//     }).includes(name)){
//         deselect(dischargeChart, 'discharge')
//     }else if (gageChart.data.datasets.map(function(d){
//         return d.label
//     }).includes(name)){
//         deselect(gageChart, 'gage')
//     }
//     else{
//         selectLocation(layer, iotid, name)
//     }
// }
//
// function refreshGraph(gid){
//     if (gid==='gwl'){
//         gwlChart.data.datasets = []
//         gwlChart.update()
//
//     }else if(gid=='gage'){
//         gageChart.data.datasets = []
//         gageChart.update()
//
//     }else if (gid=='discharge'){
//         dischargeChart.data.datasets = []
//         dischargeChart.update()
//     }
// }
//
// function selectLocation(layer, iotid, name){
//
//     $('#chartprogress').show()
//
//     let url;
//     let dsname;
//
//     if (layer.source=='USGS'){
//         url = 'https://labs.waterdata.usgs.gov/sta/v1.1/'
//         dsname = ''
//         make_id = function(iotid){
//         return "'"+iotid+"'"
//         }
//         makecolor = function(iotid){
//             return colors[hashIOTID(iotid)%10]
//         }
//     }else{
//         url = "https://st2.newmexicowaterdata.org/FROST-Server/v1.1/"
//         dsname = 'Groundwater Levels'
//         make_id = function(iotid){
//         return iotid
//         }
//         makecolor = function(iotid){
//             return colors[iotid%10]
//         }
//     }
//
//     let locationURL = url+'Locations('+make_id(iotid)+')'
//     $.get(locationURL+'?$expand=Things/Datastreams/ObservedProperty,Things/Datastreams/Sensor').then(
//                     function (data){
//                         // console.log('reload data', data)
//                         var thing = data['Things'][0]
//                         let ds;
//                         if (dsname){
//                             ds = thing['Datastreams'].filter(function (d){
//                             return d['name'] == dsname
//                             })[0]
//                         }else{
//                             ds = thing['Datastreams'][0]
//                         }
//
//                         console.log(ds, dsname, thing)
//                         if (ds){
//                             const obsurl = url+"Datastreams("+make_id(ds["@iot.id"])+")/Observations?$top=1000&$orderby=phenomenonTime desc"
//
//                             let chart;
//                             let chartid;
//                             if (ds.description.startsWith('Discharge')){
//                                 chart = dischargeChart
//                                 chartid = 'discharge'
//                             } else if (ds.description.startsWith('Gage')){
//                                 chart = gageChart
//                                 chartid = 'gage'
//                             } else {
//                                 chart = gwlChart
//                                 chartid = 'gwl'
//                             }
//
//                             let datasets = chart.data.datasets
//
//                             if (!(datasets.map(function(d){return d.label}).includes(name))){
//
//                                 document.getElementById(chartid).style.setProperty("display", "block")
//
//                                 layer.setStyle({color: 'red',fillColor: 'red'})
//                                 layer.bringToFront();
//
//                                 retrieveItems(obsurl, 10000,
//                                     function(obs){
//                                         obs.forEach(o=>{
//                                             o['locationname'] = name
//                                         })
//                                     // ods.push(obs)
//                                     // loadYearlyChart(obs)
//                                     // updateSliders(obs)
//                                     let color = makecolor(iotid)
//                                     ndata = {
//                                             iot: {'Datastream': ds,
//                                                   'Thing': thing,
//                                                   'Location': {'name': name,
//                                                                 '@iot.id': iotid,
//                                                                 'url': locationURL,
//                                                                 'location': data['location']},
//                                                   'sourceURL': url,
//                                                   // 'source': m.source
//                                             },
//                                             label: name,
//                                             data: obs.map(f=>{
//                                                 var d = new Date(f['phenomenonTime'])
//                                                 d.setHours(d.getHours()+6)
//                                                 return [d, f['result']]
//                                             }),
//                                             borderColor: color,
//                                             backgroundColor: color,
//                                             tension: 0.1
//                                         }
//
//                                     datasets.push(ndata)
//                                         // let obspropname = ds['ObservedProperty']['name']
//                                         // if (obspropname==='Depth to Water Below Ground Surface'){
//                                         //     gwlChart.options.scales.yAxis.reverse = true
//                                         // }
//                                     chart.update()
//                                     $('#chartprogress').hide()
//                             }
//                          )}
//                         }
//                         $('#chartprogress').hide()
//                     }
//     )
//
// }
// // function loadObsChart(name, data, locationURL, url,
// //                       m,
// //                       thing, ds, obs, iotid, color){
// //
// //     ndata = {
// //             iot: {'Datastream': ds,
// //                   'Thing': thing,
// //                   'Location': {'name': name,
// //                                 '@iot.id': iotid,
// //                                 'url': locationURL,
// //                                 'location': data['location']},
// //                   'sourceURL': url,
// //                   'source': m.source},
// //             label: name,
// //             data: obs.map(f=>{
// //                 var d = new Date(f['phenomenonTime'])
// //                 d.setHours(d.getHours()+6)
// //                 return [d, f['result']]
// //             }),
// //             borderColor: color,
// //             backgroundColor: color,
// //             tension: 0.1
// //         }
// //     let obspropname = ds['ObservedProperty']['name']
// //     if (obspropname==='Depth to Water Below Ground Surface'){
// //         myChart.options.scales.yAxis.reverse = true
// //     }else{
// //         myChart.options.scales.yAxis.reverse = false
// //     }
// //
// //     myChart.options.scales.yAxis.title.text=obspropname
// //     myChart.data.datasets.push(ndata)
// //     myChart.update()
// //
// //     return obspropname
// // }