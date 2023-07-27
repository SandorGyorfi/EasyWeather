document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const layer = document.getElementById('layer');
  
    form.addEventListener('submit', function (event) {
      event.preventDefault();
  
      setTimeout(function () {
        layer.classList.add('show');
      }, 2000);
  
      const cityNameInput = document.getElementById('cityName');
      cityNameInput.value = '';
    });
  });
  