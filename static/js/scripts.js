
  const form = document.getElementById('myForm');
  const submitButton = document.querySelector('.btn-primary');
  const formGroup = document.querySelector('.form-group');
  const h1 = document.querySelector('.masthead h1');
  const lead = document.querySelector('.lead');
  const label = document.querySelector('.WT1');

  form.addEventListener('submit', function (event) {
    event.preventDefault(); 
    
    submitButton.classList.add('move-up');
    formGroup.classList.add('move-up');
    h1.classList.add('move-up');
    lead.classList.add('move-up');
    label.classList.add('move-up');

    setTimeout(function () {
      submitButton.classList.remove('move-up');
      formGroup.classList.remove('move-up');
      h1.classList.remove('move-up');
      lead.classList.remove('move-up');
      label.classList.remove('move-up');
    }, 500); 
  });


