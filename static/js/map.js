
//========================================================================================
// Configuration variables
const PROJECT = 'NMBGMR Water Webmap'
// const sources = [
//         {'name': 'nmbgmr', 'label': 'NMBGMR', 'color':'purple'},
//         {'name': 'ose_roswell', 'label': 'OSE Roswell', 'color':'blue'},
//         {'name': 'isc_seven_rivers', 'label': 'ISC Seven Rivers', 'color':'orange'},
//         {'name': 'usgs', 'label': 'USGS', 'color': 'green'},
//         {'name': 'pvacd_hydrovu', 'label': 'PVACD', 'color': 'yellow'},
//     ]
//========================================================================================


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

const map = L.map('map', {
        preferCanvas: true,
        updateWhenZooming: false,
        updateWhenIdle: true,
        layers: [osm]
    }
)


// this can be used to add multiple tile layers together
// let grp = L.featureGroup()
// map.createPane('pane1')
// map.createPane('pane2')
// map.getPane('pane1').style.zIndex = 50;
// map.getPane('pane2').style.zIndex = 250;
//
// const test = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
//     {attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid,' +
//             ' IGN, IGP, UPR-EGP, and the GIS User Community',
//     pane: 'pane1'}).addTo(grp)
//
// const opentopot = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
//     opacity: 0.5,
// attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a' +
//     ' href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)\'',
// pane: 'pane2'}).addTo(grp)
//


const layerControl = L.control.layers({"OpenStreetMap": osm,
    'MacroStrat': macrostrat,
    'OpenTopo': opentopo,
    "ESRI World Imagery": esri_wi,
    'USGS National Basemap': usgs
    }, null).addTo(map);

new L.Control.Draw({
    draw: {
        rectangle: true,
        polyline: false,
        circle: false,
        polygon: false,
        circlemarker: false,
        marker: false
    },
    edit: false
}).addTo(map);

const allmarkers = [];

L.Rectangle.include({
    contains: function (latLng) {
        return this.getBounds().contains(latLng);
    }
});
//
// map.on(L.Draw.Event.CREATED, function (e) {
//     let selected = allmarkers.filter(function(marker){
//         return map.hasLayer(marker) && e.layer.contains(marker.getLatLng())
//     })
//
//     if (selected.length>20){
//         alert('You have selected '+ selected.length +' locations. The maximum number is 20')
//         return
//     }
//
//     selected.forEach(function(s){
//         selectLocation(s.stid, s.name)
//     })
//
// });

let MAP_CFG;
// function ResetSelection(){
//      myChart.data.datasets = [];
//      myChart.update()
//     yearChart.data.datasets = [];
//      yearChart.update()
//     $('#obstable').DataTable().clear().draw()
//
//     allmarkers.forEach(function (m){
//             m.setStyle({color: m.defaultColor,
//                              fillColor: m.defaultColor})
//     })
//
// }

function mapInit(cfg){
    MAP_CFG = cfg;
    map.setView([cfg.center_lat, cfg.center_lon], cfg.zoom);


    // loadLayer()
    // $.ajaxSetup({
    // async: false
    // });
    // function loadSource(s){
    //     const url = 'https://raw.githubusercontent.com/NMWDI/VocabService/main/'+PROJECT+'/'+s.name+'.json'
    //     $.getJSON(url).done(
    //         function(data){
    //             let ls = data['locations']
    //             console.debug('loading source', s)
    //             loadLayer(ls, s.color, s.label)
    //         }
    //     )
    //
    // }
    // sources.forEach(loadSource)
    loadLegend()

    // $.ajaxSetup({
    //     async: true
    // });
}
function loadLegend(){
    let legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {
        let div = L.DomUtil.create('div', 'info legend');
        let lines = ['<strong>Sources</strong>']
        // sources.forEach(s=>{
        //     lines.push(
        //         '<i class="circle" style="background: ' + s.color + '"></i> ' + s.label)
        // })

        div.innerHTML = '<div style="background: white; padding: 5px">'+ lines.join('<br>') +'</div>';
        console.log(div.innerHTML)
        return div;
    };

    legend.addTo(map);

}

function loadLayer(){
    // let url = MAP_CFG.base_api_url+'/locations'
    // let url = 'http://localhost/api/v1/locations'

    // retrieveItems(url, 20000, (locations)=>{
    //     console.log('asdfasdf', locations)
    //     let markers = locations.map((loc)=>{
    //         let marker = L.circleMarker([loc.latitude, loc.longitude],
    //             {radius: 5})
    //         marker.location = loc
    //         return marker
    //     })
    //     const layer = new L.featureGroup(markers)
    //     map.addLayer(layer)
    //     layer.on('click', function(e){
    //         show_location_table(e, e.layer.location)
    //     })
    // })

}

let locationLayer;

function clear_locations_from_map(){
    if (locationLayer){
        map.removeLayer(locationLayer)
    }
}
function add_locations_to_map(locations){
    console.log('adding locations', locations)
    let markers = locations.map((loc)=>{
    let marker = L.circleMarker([loc.latitude, loc.longitude],
        {radius: 5})
    marker.location = loc
    marker.bindPopup(loc['point_id'])
    marker.on('mouseover', function(e) {
        marker.openPopup();
    } )
    marker.on('mouseout', function(e) {
        map.closePopup();
    } )
    return marker
})
locationLayer = new L.featureGroup(markers)
map.addLayer(locationLayer)
locationLayer.on('click', function(e){
    show_location_table(e, e.layer.location, MAP_CFG.base_api_url)
})

}

function chartoff(){
    document.getElementById("chartoverlay").style.display="none"
}

function project_search(){
    location_search('#project_entry', 'project')
}
function point_id_search(){
    location_search('#pointid_entry', 'point_id')
}

function location_search(){

    let project = document.querySelector("#project_entry").value;
    let pointid = document.querySelector("#pointid_entry").value;
    let url = MAP_CFG.base_api_url+'locations?'
    if (pointid){
        url+="point_id="+pointid
    }
    if (project){
        if (pointid){
            url+='&'
        }
        url+='project='+project
    }

    if (project || pointid){
        console.log('search', pointid, project, url)
        retrieveItems(url, 20000, (locations)=>{
            clear_locations_from_map()
            add_locations_to_map(locations)
        })
    }else{
        alert('Please enter a search term')
    }
}



// function loadLayer(ls, color, label, load_things){
//     console.debug('load layer')
//
//     let mywell_id = MAP_CFG.mywell_id
//     let markers = ls.map(function (loc){return loadMarker(loc, color, load_things, mywell_id
//     )})
//
//     const layer = new L.featureGroup(markers)
//     map.addLayer(layer)
//     layerControl.addOverlay(layer, '<span class="circle" style="background: ' +
//         color+'"></span> ' +
//         label)
//
//     layer.on('click', function(e){
//         toggleLocation(e.layer)
//     })
// // }
// function loadMarker(loc, color, load_things, mywell_id){
//     var marker = L.circleMarker([loc['location']['coordinates'][1], loc['location']['coordinates'][0], ],)
//
//     if (mywell_id && loc['@iot.id'] == mywell_id){
//         marker.defaultColor = 'black'
//         color = 'black'
//         marker.setStyle({color: color,
//         fillColor: color,
//         radius: 10})
//     }
//     else{
//         marker.defaultColor = color
//         marker.setStyle({color: color,
//         fillColor: color,
//         radius: 4})
//     }
//     marker.stid = loc['@iot.id']
//     marker.name = loc['name']
//     // console.log('lasdfasdf', loc['source'], loc)
//     marker.source = loc['source']
//     marker.properties = loc['properties']
//     if (load_things){
//         $.get(loc['Things@iot.navigationLink']).then(function(data){
//               let things = data['value']
//             marker.bindPopup(loc['name']+'<br/>'+ things[0]['properties']['monitoringLocationName'])
//         })
//     }else{
//         marker.bindPopup(loc['name']+'<br/>'+ loc['source'])
//     }
//
//     // console.log(loc, loc['Things'])
//     marker.on('mouseover', function(e) {
//         marker.openPopup();
//     } )
//     marker.on('mouseout', function(e) {
//         map.closePopup();
//     } )
//
//     allmarkers.push(marker)
//     return marker
//     // markers.push(marker)
// }
// var sourceURL = 'https://raw.githubusercontent.com/NMWDI/VocabService/main/ose_roswell.json';
// var ose_roswell_markers = []
// loadSource(sourceURL, ose_roswell_markers, 'blue', 'OSE Roswell');

// var sourceURL = 'https://raw.githubusercontent.com/NMWDI/VocabService/main/usgs_pvacd.json';
// var usgs_pvacd_markers = []
// loadSource(sourceURL, usgs_pvacd_markers, 'green', 'USGS');



//
// $.getJSON("st2locations").then(
//     function (data) {
//         var options=data['options'];
//         var fuzzy_options=data['fuzzy_options'];
//         var markers=data['markers'];
//         var fuzzy_markers=data['fuzzy_markers'];
//         var markers_layer = L.geoJson(markers, {
//             pointToLayer: function (feature, latln){
//                 var marker = L.circleMarker(latln, options)
//                 return marker
//             }
//         })
//
//             if (use_cluster){
//                 var cluster= L.markerClusterGroup();
//                 cluster.addLayer(markers_layer)
//             }else{
//                 cluster = markers_layer
//             }
//
//             map.addLayer(cluster)
//             layerControl.addOverlay(cluster, 'ST2')
//
//
//             var fuzzy_layer = L.geoJson(fuzzy_markers, fuzzy_options)
//             layerControl.addOverlay(fuzzy_layer, 'OSE RealTime')
//     })
//
// $.getJSON("nmenvlocations").then(
// function (data) {
// var options=data['options'];
// var markers=data['markers'];
// var layer = L.geoJson(markers, {
//     pointToLayer: function (feature, latln){
//         var marker = L.circleMarker(latln, options)
//         return marker
//     }
// })
//     if (use_cluster){
//         var cluster= L.markerClusterGroup();
//         cluster.addLayer(layer)
//     }else{
//         cluster = layer
//     }
//     map.addLayer(cluster)
//     layerControl.addOverlay(cluster, 'NMENV')
//
//
// })
//
// $.getJSON("oselocations").then(
// function (data) {
// var options=data['options'];
// var markers=data['markers'];
// var layer = L.geoJson(markers, {
//     pointToLayer: function (feature, latln){
//         var marker = L.circleMarker(latln, options)
//         return marker
//     }
// })
//         if (use_cluster){
//             var cluster= L.markerClusterGroup({'chunkedLoading': true});
//             cluster.addLayers(layer)
//
//         }else{
//             cluster = layer
//         }
//
//         map.addLayer(cluster)
//         layerControl.addOverlay(cluster, 'OSE PODS')
// })



