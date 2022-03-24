function change_color(color) {
  const btn = document.getElementById('btn');

  btn.addEventListener('click', function onClick(event) {

    event.target.style.backgroundColor = color;

  });
}