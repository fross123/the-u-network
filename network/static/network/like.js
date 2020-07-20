function likePost(element) {
    let postId = element.id;
    let likes = document.querySelector('#likes_'+postId).innerHTML;
    let like = false;

    // if user clicks the "Like" button
    if (element.innerHTML === "Like"){
        likes ++;
        like = true;
        element.innerHTML = "unlike";
        element.className = "card-link btn btn-primary unlike";

    // if user clicks "Unlike" button
    } else if (element.innerHTML === "unlike") {
        likes --;
        like = false;
        element.innerHTML = "Like";
        element.className = "card-link btn btn-outline-primary like";
    }
    document.querySelector('#likes_'+postId).innerHTML = likes;

    fetch('/post/' + postId, {
        method: 'PUT',
        body: JSON.stringify({
            likes: likes,
            like: like
        })
    });
};

function getLikes(postId) {
    fetch('/post/'+postId)
    .then(response => response.json())
    .then(post => {
        if (post.liked == "") {
            document.querySelector('#listOfLikes').innerHTML = "No Likes";
        }
        else {
            document.querySelector('#listOfLikes').innerHTML = "";
            listOfLikes = [];
            for (i in post.liked) {
                let element = document.createElement('li');
                element.className = "list-group-item";
                element.innerHTML = post.liked[i];
                listOfLikes.push(element);
            }
            listOfLikes.forEach(element => {
                document.querySelector('#listOfLikes').appendChild(element);
            })

        }
    });
};
