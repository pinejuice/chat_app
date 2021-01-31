// $(function(){
//     var quill = new Quill('#editor', {
//         modules: {
//             toolbar: [
//                 [{ header: [1, 2, false] }],
//                 ['bold', 'italic', 'underline'],
//                 ['image', 'code-block']
//             ]
//         },
//         placeholder: 'Compose an epic...',
//         theme: 'snow'  // or 'bubble'
//     });
// });

$(function() {
    const url = 'ws://localhost:8888/ws'
    const ws = new WebSocket(url);
    const textbox = document.getElementById('edit_talk');
    const chat = document.getElementById('chat');

    ws.onmessage = function (e) {
      const li = document.createElement('li');
      li.textContent = e.data;
      chat.appendChild(li);
    }
    window.onload = function () {
      textbox.addEventListener('keypress', function (e) {
        if (e.keyCode == 13) {
          ws.send(textbox.value);
          textbox.value = "";
        }
      });
    }
})