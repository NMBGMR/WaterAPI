
const retrieveItems = (url, maxitems, callback) => {
    new Promise((resolve, reject) => {
        getItems(url, maxitems, 0, [], resolve, reject)}).then(callback)
}


const getItems = (url, maxitems, i, items, resolve, reject) =>{
    $.get(url).then(response=>{
        let ritems = items.concat(response.value)
        if (maxitems>0){
            if (ritems.length>maxitems){
                ritems = ritems.slice(0,maxitems)
                resolve(ritems)
                return
            }
        }

        if (response['@iot.nextLink']!=null){
            getItems(response['@iot.nextLink'], maxitems, i+1, ritems, resolve, reject)
        }else{
            resolve(ritems)
        }
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
