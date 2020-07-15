document.addEventListener('click', event => {
    const element = event.target;
    if (element.className == 'btn btn-primary edit') {
        var postId = element.id;
        var content = element.dataset.content;

        document.querySelector('.editedPost').innerHTML = content
    }
});
