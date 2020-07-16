function likePost(element) {
    let postId = element.id;
    let likes = document.querySelector('#likes_'+postId).innerHTML;
    let like = false;
    if (element.innerHTML === "Like"){
        likes ++;
        like = true;
        element.innerHTML = "unlike";
        element.className = "card-link btn btn-primary unlike";
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
