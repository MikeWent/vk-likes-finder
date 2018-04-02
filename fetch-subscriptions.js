var user_id = $user_id;
var subscriptions_total = API.users.getSubscriptions({
    "user_id": user_id,
    "extended": 1,
    "count": 0
}).count;

var user_subscriptions = [];
var fetched_total = 0;
var offset = 0;
while (fetched_total < subscriptions_total) {
    var chunk = API.users.getSubscriptions({
        "user_id": user_id,
        "extended": 1,
        "count": 200,
        "offset": offset
    }).items;
    var i = 0;
    while (i < chunk.length){
        if (chunk[i].type == "page"){
            user_subscriptions.push(chunk[i]);
        }
        i = i + 1;
    }
    fetched_total = fetched_total + chunk.length;
    offset = offset + 200;
}

return user_subscriptions;
