import '../styles/base.scss';

var toggleBtn = document.getElementById('toggle');
var collapseMenu = document.getElementById('collapseMenu');

function handleClick() {
    if (collapseMenu.style.display === 'block') {
    collapseMenu.style.display = 'none';
    } else {
    collapseMenu.style.display = 'block';
    }
}

toggleBtn.addEventListener('click', handleClick);