
// create map and add layers
const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-106, 34.25]),
    zoom: 7
  })
});

var select = new ol.interaction.Select({
      // layers: [flickrLayer],
      // style: selectedStyle
    });

map.addInteraction(select);
select.getFeatures().on("add", (evt)=>{
    console.log('asdfasdfsa', evt.element.values_.location)
    selectedLocation = evt.element.values_.location
    show_location_table(evt, evt.element.values_.location, CONFIG.base_api_url)

})
select.getFeatures().on("remove", (evt)=>{
    // console.log('asdfasdfsa', evt.element.values_.location)
    // show_location_table(evt, evt.element.values_.location, CONFIG.base_api_url)
    document.getElementById("chartoverlay").style.display="none"
})



let CONFIG;
function mapInit(cfg){
    CONFIG=cfg
}

let selectedLocation;

function make_point_id_report(){
    if (selectedLocation){
        window.location.href = '/frontend/point_id_report/'+selectedLocation.point_id
    }
}

function goto_detail(){
    if (selectedLocation){
        window.location.href = '/frontend/point_id_detail/'+selectedLocation.point_id
    }
}

function location_search(){
    let use_gwl_trends = document.querySelector("#use_gwl_trends").checked

    let project = document.querySelector("#project_entry").value;
    let pointid = document.querySelector("#pointid_entry").value;
    let url = CONFIG.base_api_url+'locations?'
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
            add_locations_to_map(locations, use_gwl_trends)
        })
    }else{
        alert('Please enter a search term')
    }
}



function clear_locations_from_map(){
    // if (locationLayer){
    //     map.removeLayer(locationLayer)
    // }
}

function add_locations_to_map(locations, use_gwl_trends){
    console.log('adding locations', locations)

    let increase = new ol.style.RegularShape({
                    radius:10,
                    points: 3,
                    fill: new ol.style.Fill({color: 'green'}),
                    stroke: new ol.style.Stroke({color: 'green', width: 1})
                })
    let decrease = new ol.style.RegularShape({
                    radius:10,
                    points: 3,
                    rotation: 180*Math.PI/180,
                    fill: new ol.style.Fill({color: 'red'}),
                    stroke: new ol.style.Stroke({color: 'red', width: 1})
                })
    let features = locations.map((loc)=>{
        let f= new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([loc.longitude, loc.latitude])),
                location: loc,
            })
        if (use_gwl_trends){
            fetch('/api/v1/gwtrend/'+loc.point_id).then(resp=>resp.json()).then((data)=>{
                // let color = data.trend<0? increase:decrease
                let style = new ol.style.Style({image: data.trend<0? increase:decrease})
                f.setStyle(style)
            })
        }
        return f
    })
    const vectorSource = new ol.source.Vector(
        {features: features}
    );

    const vectorLayer = new ol.layer.Vector({
      source: vectorSource,
    });
    map.addLayer(vectorLayer)
}