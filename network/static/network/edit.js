document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'btn btn-primary edit') {
        let postId = element.id;

        fetch('/post/'+postId)
        .then(response => response.json())
        .then(post => {
            document.querySelector('.editedPost').value = post.content;
            document.querySelector('.editedPost').id = post.id;
        });
    }
    if (element.className === 'btn btn-primary saveEditedPost') {
        let content = document.querySelector('.editedPost').value;
        let postId = document.querySelector('.editedPost').id;

        fetch('/post/' + postId, {
            method: 'PUT',
            body: JSON.stringify({
                content: content
            })
        });
        document.querySelector('#content_' + postId).innerHTML = content;
    }
});

/*
fetch('/emails/100', {
  method: 'PUT',
  body: JSON.stringify({
      archived: true
  })
})
*/
