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
//
// const yearChart = new Chart(document.getElementById('ygraph').getContext('2d'), {type: 'line',
//                                     data: {labels: [], datasets:[]},
//         options: options
//     })

let ods = [];
// $(document).on({
//     ajaxStart: function(){
//         console.log('start')
//
//     },
//     ajaxStop: function(){
//         console.log('stop')
//         $("#graphcontainer").removeClass("loading");
//     }
// });
// function getRow(rows, m) {
//     for (const j in rows) {
//         let row = rows[j]
//         if (row.id === m.stid) {
//             return m
//         }
//     }
// }

// function filterMap(e, settings){
//     let data = $('#wellstable').DataTable()
//
//     for (const i in allmarkers) {
//         let m = allmarkers[i]
//         map.removeLayer(m)
//     }
//     let rows = data.rows( { filter : 'applied'} ).data()
//     for (const i in allmarkers){
//         let m = allmarkers[i]
//         let row = rows.filter(function(r){
//             return r.id===m.stid
//         })[0]
//         if (row){
//             map.addLayer(m)
//         }
//     }
//         // m.visible = false
//         // console.log(m, m.visible)
//
// }

$(document).ready(function (){

    var table = $('#selectiontable')
        var dtt = table.DataTable({select: {style: 'multi'},
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

    // $('#chartprogress').hide()
    // $('#locationprogress').show()

    // $.ajaxSetup({
    // async: false
    // });
    // let locations = []
    // function loadSource(s){
    //     const url = 'https://raw.githubusercontent.com/NMWDI/VocabService/main/'+PROJECT+'/'+s.name+'.json'
    //     $.getJSON(url).done(
    //         function(data){
    //             let ls = data['locations']
    //             locations = locations.concat(ls)
    //         }
    //     )
    // }
    // sources.forEach(loadSource)

    // $.ajaxSetup({
    //         async: true
    //     });
    // var table = $('#wellstable')
    // console.log("got wells", locations.length)
    //
    // locations.forEach(function(loc){
    //     loc['id'] = loc['@iot.id']
    //     loc['thingname'] = 'Well'
    //
    //     if(loc.source==='USGS'){
    //         $.ajax({url: loc['Things@iot.navigationLink'],
    //         async: false,
    //         success: function(data){
    //             loc['Things'] = data['value']
    //             loc['thingname'] = data['value'][0].properties.monitoringLocationName
    //         }})
    //     }
    // })
    //
    // var dtt = table.DataTable({select: {style: 'multi'},
    //                         aaData: locations,
    //                         columns: [
    //                                   // {data: "id"},
    //                                   {data: "name"},
    //                                   {data: "description"},
    //                                   {data: "thingname"},
    //                                   {data: "source"}]})
    // dtt.on('search', filterMap)
    // add a button to the column
    //{data: null,
    //                                 render: function (data) {
    //                             return `<div class="text-center">
    //                             <a class='btn  btn-primary' onclick="AddToCart(${data})" >
    //                                <i class='far fa-trash-alt'></i> Delete
    //                             </a></div>`}},
    // var obstable = $('#obstable')
    // var obsdtt = obstable.DataTable({
    //             // ajax: {url:'https://st2.newmexicowaterdata.org/FROST-Server/v1.1/Observations?$top=0',
    //             //        cache: true,
    //             //        dataSrc: "value"
    //             // },
    //             columns: [{data: 'phenomenonTime'},
    //                       {data: 'result',
    //                         render: $.fn.dataTable.render.number(',', '.', 2, '')}]
    //             });
    // let obsdtt = obstable.DataTable();

    // let obsdtt =  $('#obstable').DataTable(
    //                             {'columns': [{'data': 'locationname'},
    //                                          {'data': 'phenomenonTime'},
    //                                         {'data': 'result',
    //                                             'render': $.fn.dataTable.render.number('', '.', 2, '')}]})
    //
    //
    // dtt.on('deselect', function ( e, dt, type, indexes ){
    //     if ( type === 'row' ) {
    //     var iotid = dtt.rows( indexes ).data().pluck( 'id' )[0];
    //     var name = dtt.rows( indexes ).data().pluck( 'name' )[0];
    //
    //     deselectLocation(iotid, name)
    //     }
    // });
    //
    // dtt.on( 'select', function ( e, dt, type, indexes ) {
    //     if ( type === 'row' ) {
    //     var iotid = dtt.rows( indexes ).data().pluck( 'id' )[0];
    //     var name = dtt.rows( indexes ).data().pluck( 'name' )[0];
    //
    //     selectLocation(iotid, name)
    //     }
    // })
    // $('#locationprogress').hide()

})

//
// function AddToCart(id){
//             alert(id);
//             $('#lblID').val(id);
//             $('#deleteConfirmationModal').modal('show');
// }

// function toggleLocation(iotid, name){
//     if (myChart.data.datasets.map(function(d){
//         return d.label
//     }).includes(name)){
//         deselectLocation(iotid, name)
//     }else{
//
//         selectLocation(iotid, name)
//
//     }
//
// }
// function deselectLocation(iotid, name){
//     console.log('deselect location')
//     var datasets = myChart.data.datasets
//     console.log(iotid, name)
//     // console.log(datasets.filter(function(d){
//     //     return !(d.label === name)
//     // }))
//     myChart.data.datasets = datasets.filter(function(d){
//         return !(d.label === name)
//     })
//     myChart.update()
//
//     allmarkers.forEach(function (m){
//         if (m.stid===iotid){
//             m.setStyle({color: m.defaultColor,
//                         fillColor: m.defaultColor})
//         }
//     })
// }

// const colors = chroma.scale(['#eeee14','#1471a2']).mode('lch').colors(10)

// function hashIOTID(iotid) {
//   var hash = 0, i, chr;
//   if (iotid.length === 0) return hash;
//   for (i = 0; i < iotid.length; i++) {
//     chr   = iotid.charCodeAt(i);
//     hash  = ((hash << 5) - hash) + chr;
//     hash |= 0; // Convert to 32bit integer
//   }
//   return hash;
// }
// function getMarker(iotid){
//     return allmarkers.filter(function (m){ return m.stid == iotid})[0]
// }

function show_location_table(evt, location, base_api_url){
    console.log('location selected', location)
    let url = base_api_url+'wells?location_id='+location.id

    fetch(url).then(resp=>resp.json()).then((data)=>{
        console.log('location data', data)
        let well =data.items[0]
        populate_selection_table(well, location.point_id, '#selectiontable')

    })

    myChart.update()
    $('#chartprogress').show()


    let div = document.getElementById("chartoverlay")
    console.log(evt)
    // console.log(evt.originalEvent.clientY, evt.originalEvent.clientY+20+'px')
    // div.style.top = evt.originalEvent.clientY+20+'px'
    // div.style.left = evt.originalEvent.clientX+20+'px'
    div.style.top = '200px'
    div.style.left = '200px'
    div.style.display = "block"

    url = base_api_url+'waterlevels?location_id='+location.id
    retrieveItems(url, 10000, (measurements)=>{
        // let datasets = myChart.data.datasets
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
                    label: location.point_id,
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


    })

    // let locationURL = url+'Locations('+make_id(iotid)+')'
    // console.log(locationURL+'?$expand=Things/Datastreams/ObservedProperty,Things/Datastreams/Sensor')
    // $('#chartprogress').show()
    //
    // $.get(locationURL+'?$expand=Things/Datastreams/ObservedProperty,Things/Datastreams/Sensor').then(
    //                 function (data){
    //                     // console.log('reload data', data)
    //                     var thing = data['Things'][0]
    //
    //                     populateThingInfoTable(thing)
    //                     openInfo(null, 'Location')
    //                     populateDatastreamsInfoTable(thing['Datastreams'])
    //
    //                     let ds;
    //                     if (dsname){
    //                         ds = thing['Datastreams'].filter(function (d){
    //                         return d['name'] == dsname
    //                         })[0]
    //                     }else{
    //                         ds = thing['Datastreams'][0]
    //                     }
    //
    //
    //                     if (ds){
    //                         populateDatastreamInfoTable(ds)
    //                         populateSensorInfoTable(ds['Sensor'])
    //                         populateObservedPropertyInfoTable(ds['ObservedProperty'])
    //                         m.setStyle({color: 'red',fillColor: 'red'})
    //                         m.bringToFront();
    //                         let obsdtt =  $('#obstable').DataTable()
    //
    //                         const obsurl = url+"Datastreams("+make_id(ds["@iot.id"])+")/Observations?$top=1000&$orderby=phenomenonTime desc"
    //                         // fetch(obsurl).then(response=>response.json()).then(data=>{
    //                         //     console.log('objsasdf', data)
    //                         //     obsdtt.clear()
    //                         //     obsdtt.rows.add(data['value']).draw()
    //                         // })
    //                         // obsdtt.ajax.url(obsurl)
    //                         // obsdtt.ajax.reload()
    //
    //                         var datasets = myChart.data.datasets
    //
    //                         if (!(datasets.map(function(d){return d.label}).includes(name))){
    //                             retrieveItems(obsurl, 10000,
    //                                 function(obs){
    //                                     obs.forEach(o=>{
    //                                         o['locationname'] = name
    //                                     })
    //                                 obsdtt.rows.add(obs).draw()
    //                                 ods.push(obs)
    //                                 loadYearlyChart(obs)
    //                                 updateSliders(obs)
    //                                 let color = makecolor(iotid)
    //                                 ndata = {
    //                                         iot: {'Datastream': ds,
    //                                               'Thing': thing,
    //                                               'Location': {'name': name,
    //                                                             '@iot.id': iotid,
    //                                                             'url': locationURL,
    //                                                             'location': data['location']},
    //                                               'sourceURL': url,
    //                                               'source': m.source},
    //                                         label: name,
    //                                         data: obs.map(f=>{
    //                                             var d = new Date(f['phenomenonTime'])
    //                                             d.setHours(d.getHours()+6)
    //                                             return [d, f['result']]
    //                                         }),
    //                                         borderColor: color,
    //                                         backgroundColor: color,
    //                                         tension: 0.1
    //                                     }
    //
    //                                 datasets.push(ndata)
    //                                     let obspropname = ds['ObservedProperty']['name']
    //                                     if (obspropname==='Depth to Water Below Ground Surface'){
    //                                         myChart.options.scales.yAxis.reverse = true
    //                                     }else{
    //                                         yearChart.options.scales.yAxis.reverse = false
    //                                     }
    //                                     yearChart.options.scales.yAxis.title.text=obspropname
    //
    //                                   $(obsdtt.column(0).header()).text('Location Name')
    //                                   $(obsdtt.column(1).header()).text('Measurement Time')
    //                                   $(obsdtt.column(2).header()).text( obspropname)
    //
    //                                 myChart.update()
    //                                 yearChart.update()
    //
    //                                 // document.getElementById("chartprogress").style.display ="none"
    //                                     $('#chartprogress').hide()
    //                         }
    //                      )}
    //                     }
    //                 }
    // )
}

//
// const retrieveItems = (url, maxitems, callback) => {
//     new Promise((resolve, reject) => {
//         getItems(url, maxitems, 0, [], resolve, reject)}).then(callback)
// }
//
//
// const getItems = (url, maxitems, i, items, resolve, reject) =>{
//     $.get(url).then(response=>{
//         let ritems = items.concat(response.value)
//         if (maxitems>0){
//             if (ritems.length>maxitems){
//                 ritems = ritems.slice(0,maxitems)
//                 resolve(ritems)
//                 return
//             }
//         }
//
//         if (response['@iot.nextLink']!=null){
//             getItems(response['@iot.nextLink'], maxitems, i+1, ritems, resolve, reject)
//         }else{
//             resolve(ritems)
//         }
//     })
// }

function clearInfoTables(){
    $('#datastreaminfotable').html(makeInfoContent( '', '', null))
    $('#thinginfotable').html(makeInfoContent('', '', null))
    $('#locationinfotable').html(makeInfoContent('', '', null))

}

function makeWellInfoContent(well){
    let infocontent = ``
    let keys = ['id', 'public_release']
    for(let i=0; i<2; i++){
        let key = keys[i]
         let value = well[key]
        let row='<tr>'+
            '<td>'+key+'</td>'+
            '<td>'+value+'</td>'+
            '</tr>'
        infocontent+=row
    }
    let wc = well['well_construction']

    infocontent+='<tr><td>Casing Diameter</td>'+
        '<td>'+wc['casing_diameter']+'</td>'+
        '<tr/><tr><td>Hole Depth</td>'+
        '<td>'+wc['hole_depth']+'</td>'+
        '<tr/><tr><td>Well Depth</td>'+
        '<td>'+wc['well_depth']+'</td><tr/>'

    return infocontent

}
function makeInfoContent(location){

    let infocontent=`<thead>
                        <tr>
                            <th>Property</th>
                            <th>Value</th>
                        </tr>
                    </thead>`

     for (const key in location){
         let value = location[key]
         if (value instanceof Object){
             value = JSON.stringify(value)
         }
        let row='<tr>'+
            '<td>'+key+'</td>'+
            '<td>'+value+'</td>'+
            '</tr>'
        infocontent+=row
    }
     return infocontent
}

// function populateSTInfoTable(obj, id){
//     let iotid = obj['@iot.id']
//     let name = obj['name']
//     let properties = obj['properties']
//     $(id).html(makeInfoContent( iotid, name, properties))
// }
// function populateSensorInfoTable(obj){
//     populateSTInfoTable(obj, '#sensorinfotable')
// }

// function populateObservedPropertyInfoTable(obj){
//     populateSTInfoTable(obj, '#obspropinfotable')
// }
//
// function populateDatastreamsInfoTable(dss){
//     let table = '';
//     for (const di in dss){
//         let item = dss[di]
//         let content = '<td>'+item['@iot.id'] +'</td>'+
//             '<td>'+item['name'] +'</td>'+
//             '<td>'+item['unitOfMeasurement']['symbol'] +'</td>'
//         let row = '<tr>'+content+'</tr>'
//         table+=row
//     }
//
//     $('#datastreamsinfotable').html(table)
//
//
// }
// function populateDatastreamInfoTable(ds){
//     // let iotid = ds['@iot.id']
//     // let name = ds['name']
//     // let properties = ds['properties']
//     // $('#datastreaminfotable').html(makeInfoContent( iotid, name, properties))
//     populateSTInfoTable(ds, '#datastreaminfotable')
// }

// function populateThingInfoTable(thing){
//     // let iotid = thing['@iot.id']
//     // let name = thing['name']
//     // let properties = thing['properties']
//
//     // $('#thinginfotable').html(makeInfoContent(iotid, name, properties))
//     populateSTInfoTable(thing, '#thinginfotable')
// }

function populateWellInfoTable(well){
    // console.log(layer, 'asfd')
    $('#wellinfotable').html(makeWellInfoContent(well))
}

function populateLocationInfoTable(location){
    // console.log(layer, 'asfd')
    $('#locationinfotable').html(makeInfoContent(location))
}

function openInfo(evt, name) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(name).style.display = "block";
  if (evt){
    evt.currentTarget.className += " active";
  }

}