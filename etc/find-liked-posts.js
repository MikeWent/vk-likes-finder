var posts = API.wall.get({
    "owner_id": $wall_id,
    "count": 24,
    "offset": $posts_offset
}).items;

var liked_urls = [];
var i = 0;
while (i < posts.length){
    var post = posts[i];
    var status = API.likes.isLiked({
        "type": "post",
        "user_id": $user_id,
        "owner_id": post.owner_id,
        "item_id": post.id
    });
    if (status.liked == 1){
        var url = "https://vk.com/wall"+post.owner_id+"_"+post.id;
        liked_urls.push(url);
    }
    i = i+1;
}

return liked_urls;
