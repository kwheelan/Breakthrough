function blink()
{
  let thank = document.querySelector('#thanks');

  if (thank.style.visibility === 'hidden')
  {
    thank.style.visibility = 'visible';
  }
  else
  {
    thank.style.visibility = 'hidden';
  }
}

window.setInterval(blink, 500)
