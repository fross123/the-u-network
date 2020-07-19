document.addEventListener('DOMContentLoaded', () => {
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
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = () => {
            let postId = button.id;

            fetch('/post/'+postId)
            .then(response => response.json())
            .then(post => {
                editor.setContents(JSON.parse(post.content));
                document.querySelector(".editedPost").id = post.id;
            });
        }
    });

    document.querySelectorAll('#saveEditedPost').forEach(button => {
        button.onclick = () => {
            let content = JSON.stringify(editor.getContents());
            let html = editor.root.innerHTML;
            let postId = document.querySelector('.editedPost').id;

            fetch('/post/' + postId, {
                method: 'PUT',
                body: JSON.stringify({
                    content: content,
                    html: html
                })
            });
            document.querySelector('#content_' + postId).innerHTML = html;
        }
    });
});
