document.addEventListener('DOMContentLoaded', function () {
  const departmentsContainer = document.getElementById('departments-list');
  if (!departmentsContainer || typeof departmentsData === 'undefined') {
    return;
  }

  const departmentIds = Object.keys(departmentsData).sort((a, b) => {
    return departmentsData[a].name.localeCompare(departmentsData[b].name);
  });

  departmentsContainer.innerHTML = departmentIds
    .map((deptId, index) => {
      const dept = departmentsData[deptId];
      return `
        <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="${100 + index * 100}">
          <div class="department-card">
            <div class="department-icon">
              <i class="${dept.icon}"></i>
            </div>
            <div class="department-image">
              <img src="${dept.image}" alt="${dept.name} Department" class="img-fluid">
            </div>
            <div class="department-content">
              <h3>${dept.name}</h3>
              <p>${dept.shortDescription}</p>
              <a href="department-details.html?dept=${dept.id}" class="learn-more">
                <span>Learn More</span>
                <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>
        </div>
      `;
    })
    .join('');

  if (typeof AOS !== 'undefined') {
    AOS.refresh();
  }
});
