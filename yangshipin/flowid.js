

function get_flowid() {
    flowid = `${(new Date).getTime().toString(36)}_${Math.random().toString(36).replace(/^0./, "")}`
    console.log(flowid)
    return flowid
}
get_flowid()