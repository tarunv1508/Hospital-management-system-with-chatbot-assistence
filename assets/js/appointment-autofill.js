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

  /**
   * Infer department from a referring department/service page when the query is missing.
   */
  function getPageNameFromUrl(url) {
    try {
      return new URL(url).pathname.split('/').pop().toLowerCase();
    } catch (e) {
      return '';
    }
  }

  function getQueryParamFromUrl(url, param) {
    try {
      return new URL(url).searchParams.get(param);
    } catch (e) {
      return null;
    }
  }

  function inferDepartmentFromReferrer(referrer) {
    if (!referrer) return null;

    const pageName = getPageNameFromUrl(referrer);
    if (!pageName) return null;

    // If referrer is the generic department-details page, try to extract the department
    // from its query string (it renders different departments dynamically).
    if (pageName === 'department-details.html') {
      return getQueryParamFromUrl(referrer, 'dept') || getQueryParamFromUrl(referrer, 'department') || getQueryParamFromUrl(referrer, 'id') || null;
    }

    // If referrer is the generic service-details page, try to extract the service/department
    if (pageName === 'service-details.html') {
      return getQueryParamFromUrl(referrer, 'dept') || getQueryParamFromUrl(referrer, 'department') || getQueryParamFromUrl(referrer, 'service') || null;
    }

    const departmentPages = {
      'department-cardiology.html': 'cardiology',
      'department-dental.html': 'dental',
      'department-dermatology.html': 'dermatology',
      // 'department-details.html' is handled above by extracting its query param
      'department-neurology.html': 'neurology',
      'department-oncology.html': 'oncology',
      'department-ophthalmology.html': 'ophthalmology',
      'department-orthopedics.html': 'orthopedics',
      'department-pediatrics.html': 'pediatrics'
    };

    const servicePages = {
      'service-details.html': 'general',
      'service-emergency-care.html': 'general',
      'service-laboratory-testing.html': 'general',
      'service-medical-imaging.html': 'general',
      'service-mental-health.html': 'psychiatry',
      'service-pharmacy-services.html': 'general',
      'service-physiotherapy.html': 'orthopedics',
      'service-telemedicine.html': 'general',
      'service-wellness-programs.html': 'general'
    };

    if (departmentPages[pageName]) {
      return departmentPages[pageName];
    }

    if (servicePages[pageName]) {
      return servicePages[pageName];
    }

    if (pageName === 'departments.html' || pageName === 'services.html') {
      return getQueryParamFromUrl(referrer, 'dept') || null;
    }

    return null;
  }

  if (!departmentParam) {
    departmentParam = inferDepartmentFromReferrer(document.referrer);
  }

  // Get form elements
  const departmentSelect = document.getElementById('departmentSelect');
  const doctorSelect = document.getElementById('doctorSelect');

  function normalizeValue(value) {
    return value ? value.toString().trim().toLowerCase() : '';
  }

  function getValidDepartmentValue(deptValue) {
    if (!departmentSelect || !deptValue) {
      return deptValue;
    }
    const normalizedDept = normalizeValue(deptValue);
    const exactOption = Array.from(departmentSelect.options).find(opt => normalizeValue(opt.value) === normalizedDept);
    if (exactOption) {
      return exactOption.value;
    }
    const fuzzyOption = Array.from(departmentSelect.options).find(opt => normalizeValue(opt.textContent).includes(normalizedDept));
    return fuzzyOption ? fuzzyOption.value : deptValue;
  }

  function triggerDepartmentSelectChange() {
    if (departmentSelect) {
      departmentSelect.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  departmentParam = getValidDepartmentValue(departmentParam);

  if (departmentParam && !urlDepartment) {
    const url = new URL(window.location);
    url.searchParams.set('department', departmentParam);
    window.history.replaceState({}, '', url);
  }

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
  function getDepartmentAliases(deptValue) {
    const normalized = normalizeValue(deptValue);
    if (!normalized) return [''];
    if (normalized === 'general' || normalized === 'general_medicine') {
      return ['general', 'general_medicine'];
    }
    return [normalized];
  }

  function filterDoctorsByDepartment(deptValue) {
    if (!doctorSelect) return;
    const deptAliases = getDepartmentAliases(deptValue);
    const options = doctorSelect.querySelectorAll('option');
    options.forEach(option => {
      if (option.value === '') {
        option.style.display = 'block';
        option.hidden = false;
        option.disabled = false;
      } else {
        const optionDept = normalizeValue(option.getAttribute('data-department'));
        const isVisible = deptAliases.includes(optionDept);
        option.style.display = isVisible ? 'block' : 'none';
        option.hidden = !isVisible;
        option.disabled = !isVisible;
      }
    });
  }

  function applyAutoFill() {
    // Auto-fill department if provided
    if (departmentParam && departmentSelect) {
      filterDoctorsByDepartment(departmentParam);
      departmentSelect.value = departmentParam;
      triggerDepartmentSelectChange();
      setHiddenField('department', departmentParam);
      departmentSelect.disabled = true; // Prevent manual change
      departmentSelect.style.backgroundColor = '#e9ecef'; // Visual feedback
      departmentSelect.style.cursor = 'not-allowed';

      if (typeof window.updateDoctorOptions === 'function') {
        window.updateDoctorOptions();
      }
    }

    // Auto-fill doctor if provided
    if (doctorParam && doctorSelect) {
      if (!urlDepartment) {
        const doctorOption = doctorSelect.querySelector(`option[value="${doctorParam}"]`);
        if (doctorOption && doctorOption.getAttribute('data-department')) {
          departmentParam = departmentParam || doctorOption.getAttribute('data-department');
        }
      }

      if (departmentParam) {
        filterDoctorsByDepartment(departmentParam);
        departmentSelect.value = departmentParam;
        triggerDepartmentSelectChange();
        setHiddenField('department', departmentParam);
        departmentSelect.disabled = true;
        departmentSelect.style.backgroundColor = '#e9ecef';
        departmentSelect.style.cursor = 'not-allowed';

        if (typeof window.updateDoctorOptions === 'function') {
          window.updateDoctorOptions();
        }
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

        // Tell the inline page script to refresh doctor options now that autofill completed.
        document.dispatchEvent(new CustomEvent('departmentAutoFilled'));
      }, 100);
    }
  }

  setTimeout(applyAutoFill, 0);

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
