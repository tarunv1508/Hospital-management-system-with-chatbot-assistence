/**
 * Auto-fill appointment form fields based on URL parameters
 * Usage: appointment.html?department=cardiology&doctor=DR.S.Arjun%20Reddy
 */

document.addEventListener('DOMContentLoaded', function() {
  // Get URL parameters using search string parsing
  function getUrlParam(param) {
    const searchParams = new URL(window.location).searchParams;
    return searchParams.get(param);
  }

  const urlDepartment = getUrlParam('department') || getUrlParam('dept');
  const urlDoctor = getUrlParam('doctor');
  const savedDepartment = localStorage.getItem('selectedDepartment');
  const savedDoctor = localStorage.getItem('selectedDoctor');
  let departmentParam = urlDepartment || savedDepartment;
  const doctorParam = urlDoctor || savedDoctor;

  // Get form elements
  const departmentSelect = document.getElementById('departmentSelect');
  const doctorSelect = document.getElementById('doctorSelect');

  // Create or update a hidden input so disabled fields still submit
  function setHiddenField(name, value) {
    let hiddenInput = document.querySelector(`input[type="hidden"][name="${name}"]`);
    if (!hiddenInput) {
      hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = name;
      const form = document.querySelector('#appointment-form');
      if (form) {
        form.appendChild(hiddenInput);
      }
    }
    hiddenInput.value = value;
  }

  // Function to filter doctor options based on department
  function filterDoctorsByDepartment(deptValue) {
    if (!doctorSelect) return;
    const options = doctorSelect.querySelectorAll('option');
    options.forEach(option => {
      if (option.value === '') {
        option.style.display = 'block'; // Always show the placeholder
      } else {
        const optionDept = option.getAttribute('data-department');
        if (optionDept === deptValue) {
          option.style.display = 'block';
        } else {
          option.style.display = 'none';
        }
      }
    });
  }

  // Auto-fill department if provided
  if (departmentParam && departmentSelect) {
    // First filter doctors
    filterDoctorsByDepartment(departmentParam);
    
    // Then set department value
    departmentSelect.value = departmentParam;
    setHiddenField('department', departmentParam);
    departmentSelect.disabled = true; // Prevent manual change
    departmentSelect.style.backgroundColor = '#e9ecef'; // Visual feedback
    departmentSelect.style.cursor = 'not-allowed';
  }

  // Auto-fill doctor if provided
  if (doctorParam && doctorSelect) {
    // If department is not explicit, infer it from the doctor option.
    if (!urlDepartment) {
      const doctorOption = doctorSelect.querySelector(`option[value="${doctorParam}"]`);
      if (doctorOption && doctorOption.getAttribute('data-department')) {
        departmentParam = departmentParam || doctorOption.getAttribute('data-department');
      }
    }

    if (departmentParam) {
      filterDoctorsByDepartment(departmentParam);
      departmentSelect.value = departmentParam;
      setHiddenField('department', departmentParam);
      departmentSelect.disabled = true;
      departmentSelect.style.backgroundColor = '#e9ecef';
      departmentSelect.style.cursor = 'not-allowed';
    }

    setTimeout(function() {
      doctorSelect.value = doctorParam;
      setHiddenField('doctor', doctorParam);
      doctorSelect.disabled = true; // Prevent manual change
      doctorSelect.style.backgroundColor = '#e9ecef'; // Visual feedback
      doctorSelect.style.cursor = 'not-allowed';

      // Clear the fallback storage only after successfully using it.
      localStorage.removeItem('selectedDoctor');
      localStorage.removeItem('selectedDepartment');
    }, 100);
  }

  // Add department change listener (only if department is not locked)
  if (departmentSelect && doctorSelect && !departmentParam) {
    departmentSelect.addEventListener('change', function() {
      filterDoctorsByDepartment(this.value);
      
      // Reset doctor selection if current selection doesn't match department
      if (doctorSelect.value) {
        const selectedOption = doctorSelect.querySelector(`option[value="${doctorSelect.value}"]`);
        if (selectedOption && selectedOption.style.display === 'none') {
          doctorSelect.value = '';
        }
      }
    });
  }

  // Add a note if fields are auto-filled
  if ((departmentParam || doctorParam) && departmentSelect) {
    // Use a small timeout to ensure form element exists in the DOM
    setTimeout(function() {
      const formElement = departmentSelect.closest('form');
      if (formElement) {
        const noteDiv = document.createElement('div');
        noteDiv.className = 'alert alert-info mt-3';
        noteDiv.innerHTML = '<i class="bi bi-info-circle"></i> Your department and/or doctor have been pre-selected based on your previous selection. Fields are locked to ensure accuracy.';
        formElement.appendChild(noteDiv);
      }
    }, 200);
  }
});
