document.addEventListener('DOMContentLoaded', () => {
    // initiate quill
    var container = document.querySelector('.editedPost');
    const editor = new Quill(container, {
      modules: {
        toolbar: [
          [{ header: [1, 2, 3, false] }],
          ['bold', 'italic', 'underline', 'strike'],
          [{'color': []}, {'background': []}],
          ['link'],
          ['clean']
        ]
      },
      initial: 'Compose an epic...',
      theme: 'snow'  // or 'bubble'
    });
    // if the edit button is clicked
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = () => {
            // get the post pk
            let postId = button.id;

            fetch('/post/'+postId)
            .then(response => response.json())
            .then(post => {
                // set the contents of the editor to the delta stored in server
                editor.setContents(JSON.parse(post.content));

                // set the editor id equal to the post id for reference when saving
                document.querySelector(".editedPost").id = post.id;
            });
        }
    });

    document.querySelectorAll('#saveEditedPost').forEach(button => {
        button.onclick = () => {
            // retrieve and JSON.stringify contents
            let content = JSON.stringify(editor.getContents());

            // also store html in db
            let html = editor.root.innerHTML;

            // retrieve postId from editedPost
            let postId = document.querySelector('.editedPost').id;

            fetch('/post/' + postId, {
                method: 'PUT',
                body: JSON.stringify({
                    content: content,
                    html: html
                })
            });
            // make innerHTML of post content equal to html
            document.querySelector('#content_' + postId).innerHTML = html;
        }
    });
});
