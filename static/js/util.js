
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

let layerControl = L.control.layers({"OpenStreetMap": osm,
    'MacroStrat': macrostrat,
    'OpenTopo': opentopo,
    "ESRI World Imagery": esri_wi,
    'USGS National Basemap': usgs
    }, null)

function populate_selection_table(well, point_id, id){
    console.log('ffffff', point_id, id, well)
    var table = $(id).DataTable()
        table.clear()
        table.rows.add([{key: "PointID", value: point_id },
            {key: "Hole Depth (ft)", value: well.well_construction.hole_depth},
            {key: "Well Depth (ft)", value: well.well_construction.well_depth},
            {key: "Casing Depth", value: well.well_construction.casing_depth},
            {key: "Casing Diameter", value: well.well_construction.casing_diameter.toFixed(2)},
            {key: "Casing Description", value: well.well_construction.casing_description},
            {key: "Measuring Point", value: well.well_construction.measuring_point},
            {key: "Measuring Point Height", value: well.well_construction.measuring_point_height},

            {key: "OSE Well ID", value: well.ose_well_id},
            {key: "OSE Well Tag ID", value: well.ose_well_tag_id},

            {key: "Aquifer Class", value: well.thing.aquifer_class},
            {key: "Aquifer Type", value: well.thing.aquifer_type},
            {key: "Formation", value: well.thing.formation},
            {key: "Status", value: well.thing.status},
            {key: "CurrentUse", value: well.thing.current_use}

        ]).draw()

}

const retrieveItems = (url, maxitems, callback) => {
    new Promise((resolve, reject) => {
        getItems(url, maxitems, 1, [], resolve, reject)}).then(callback)
}


const getItems = (url, maxitems, i, items, resolve, reject) =>{
    let qurl = url
    if (url.includes('?')){
        qurl+='&page='+i
    }else{
        qurl+='?page='+i
    }

    $.get(qurl).then(response=>{
        console.log(url, response)
        let ritems = items.concat(response.items)
        if (maxitems>0){
            if (ritems.length>maxitems){
                ritems = ritems.slice(0,maxitems)
                resolve(ritems)
                return
            }
        }
        // console.log(url, ritems)
        // console.log('asdfasdf', .total)
        if (ritems.length<response.total){
            getItems(url, maxitems, i+1, ritems, resolve, reject)
        }else{
            resolve(ritems)
        }
        // resolve(ritems)
        // if (response['@iot.nextLink']!=null){
        //     getItems(response['@iot.nextLink'], maxitems, i+1, ritems, resolve, reject)
        // }else{
        // }
    })
}


const colors = chroma.scale(['#eeee14','#1471a2']).mode('lch').colors(10)

function hashIOTID(iotid) {
  var hash = 0, i, chr;
  if (iotid.length === 0) return hash;
  for (i = 0; i < iotid.length; i++) {
    chr   = iotid.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
}
