document.addEventListener('DOMContentLoaded', function () {
  const servicesContainer = document.getElementById('services-list');
  if (!servicesContainer || typeof departmentsData === 'undefined') {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const deptId = params.get('dept');
  const selectedDept = deptId && departmentsData[deptId] ? departmentsData[deptId] : null;

  let cardsHtml = '';

  if (selectedDept) {
    const pageHeadingTitle = document.querySelector('.page-title .heading-title');
    const pageHeadingDescription = document.querySelector('.page-title .mb-0');
    const breadcrumbCurrent = document.querySelector('.breadcrumbs li.current');

    if (pageHeadingTitle) {
      pageHeadingTitle.textContent = `${selectedDept.name} Services`;
    }
    if (pageHeadingDescription) {
      pageHeadingDescription.textContent = `Explore services available in our ${selectedDept.name} department, tailored for your care needs.`;
    }
    if (breadcrumbCurrent) {
      breadcrumbCurrent.textContent = `${selectedDept.name} Services`;
    }
    document.title = `${selectedDept.name} Services - Hospital`;

    cardsHtml = selectedDept.services
      .map((service, index) => {
        return `
          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="${200 + index * 100}">
            <div class="service-item">
              <div class="service-image">
                <img src="${selectedDept.image}" alt="${service.name}" class="img-fluid">
                <div class="service-overlay">
                  <i class="fas fa-heartbeat"></i>
                </div>
              </div>
              <div class="service-content">
                <h3>${service.name}</h3>
                <p>${service.description}</p>
                <div class="service-features">
                  <span class="feature-item"><i class="fas fa-check"></i>Experienced Team</span>
                  <span class="feature-item"><i class="fas fa-check"></i>Personalized Care</span>
                </div>
                <a href="appointment.html?dept=${selectedDept.id}" class="service-btn">
                  <span>Book Appointment</span>
                  <i class="fas fa-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
        `;
      })
      .join('');
  } else {
    const departmentIds = Object.keys(departmentsData).sort((a, b) => {
      return departmentsData[a].name.localeCompare(departmentsData[b].name);
    });

    cardsHtml = departmentIds
      .map((deptId, index) => {
        const dept = departmentsData[deptId];
        return `
          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="${200 + index * 100}">
            <div class="service-item">
              <div class="service-image">
                <img src="${dept.image}" alt="${dept.name} Services" class="img-fluid">
                <div class="service-overlay">
                  <i class="fas fa-building"></i>
                </div>
              </div>
              <div class="service-content">
                <h3>${dept.name} Services</h3>
                <p>${dept.shortDescription}</p>
                <div class="service-features">
                  <span class="feature-item"><i class="fas fa-check"></i>Specialized Care</span>
                  <span class="feature-item"><i class="fas fa-check"></i>Departmental Services</span>
                </div>
                <a href="services.html?dept=${dept.id}" class="service-btn">
                  <span>View ${dept.name}</span>
                  <i class="fas fa-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
        `;
      })
      .join('');
  }

  servicesContainer.innerHTML = cardsHtml;

  if (typeof AOS !== 'undefined') {
    AOS.refresh();
  }
});
