

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
        if (response.items.length>0){
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
