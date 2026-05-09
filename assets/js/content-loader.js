// Dynamic Content Loader for Departments and Services

class ContentLoader {
  constructor() {
    this.currentDepartment = null;
    this.currentService = null;
  }

  // Get department from URL or data
  getDepartment(deptId) {
    return departmentsData[deptId] || null;
  }

  // Get service from URL or data
  getService(serviceId) {
    return servicesData[serviceId] || null;
  }

  // Get doctor details
  getDoctor(doctorName) {
    return doctorDetails[doctorName] || null;
  }

  // Load department details page
  loadDepartmentDetails(deptId) {
    const dept = this.getDepartment(deptId);
    if (!dept) return false;

    this.currentDepartment = dept;

    // Update page title
    document.title = `${dept.title} - Hospital`;

    // Update hero section
    const heroSection = document.querySelector('.department-hero');
    if (heroSection) {
      heroSection.innerHTML = `
        <div class="badge-wrap">
          <span class="specialty-badge">${dept.name}</span>
        </div>
        <h1 class="department-title">${dept.title}</h1>
        <p class="department-intro">${dept.longDescription}</p>

        <div class="key-highlights">
          <div class="highlight-item">
            <span class="highlight-number">24/7</span>
            <span class="highlight-text">Emergency Services</span>
          </div>
          <div class="highlight-item">
            <span class="highlight-number">${dept.doctors.length}</span>
            <span class="highlight-text">Specialist Doctors</span>
          </div>
          <div class="highlight-item">
            <span class="highlight-number">95%</span>
            <span class="highlight-text">Patient Satisfaction</span>
          </div>
        </div>

        <div class="action-group">
          <a href="appointment.html" class="btn-primary">Schedule Consultation</a>
          <a href="services.html" class="btn-secondary">
            <span>View All Services</span>
            <i class="bi bi-arrow-right"></i>
          </a>
        </div>
      `;
    }

    // Update department image
    const deptImage = document.querySelector('.department-visual img.primary-image');
    if (deptImage) {
      deptImage.src = dept.image;
      deptImage.alt = dept.title;
    }

    // Update services grid
    this.loadDepartmentServices(dept);

    // Update expert section
    this.loadExpertSection(dept);

    // Load recommended doctors
    this.loadRecommendedDoctors(dept);

    return true;
  }

  // Load department services
  loadDepartmentServices(dept) {
    const servicesGrid = document.querySelector('.services-grid');
    if (!servicesGrid) return;

    servicesGrid.innerHTML = dept.services.map((service, index) => `
      <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="${500 + index * 50}">
        <div class="service-item">
          <div class="service-icon">
            <i class="bi bi-${this.getIconClass(service.name)}"></i>
          </div>
          <h4>${service.name}</h4>
          <p>${service.description}</p>
        </div>
      </div>
    `).join('');
  }

  // Load expert section with features
  loadExpertSection(dept) {
    const expertSection = document.querySelector('.expert-content');
    if (!expertSection) return;

    expertSection.innerHTML = `
      <h3>About ${dept.name}</h3>
      <p class="lead">${dept.longDescription}</p>

      <div class="expertise-list">
        ${dept.features.map(feature => `
          <div class="expertise-item">
            <i class="bi ${feature.icon}"></i>
            <span>${feature.text}</span>
          </div>
        `).join('')}
      </div>

      <div class="contact-info">
        <div class="contact-item">
          <i class="bi bi-telephone"></i>
          <div>
            <span class="contact-label">Emergency ${dept.name}</span>
            <span class="contact-value">+1 (555) 234-5678</span>
          </div>
        </div>
        <div class="contact-item">
          <i class="bi bi-calendar-check"></i>
          <div>
            <span class="contact-label">Appointments</span>
            <span class="contact-value">Mon - Fri, 8:00 AM - 6:00 PM</span>
          </div>
        </div>
      </div>
    `;
  }

  // Load recommended doctors section
  loadRecommendedDoctors(dept) {
    const container = document.querySelector('.recommended-doctors-section');
    if (!container) {
      // Create the section if it doesn't exist
      const mainContent = document.querySelector('.department-details .container');
      if (mainContent) {
        const section = document.createElement('div');
        section.className = 'recommended-doctors-section mt-5';
        mainContent.appendChild(section);
        this.renderDoctors(dept, section);
      }
    } else {
      this.renderDoctors(dept, container);
    }
  }

  // Render doctors HTML
  renderDoctors(dept, container) {
    const doctorsHTML = `
      <div class="doctors-section-wrapper" data-aos="fade-up" data-aos-delay="900">
        <div class="section-header text-center mb-5">
          <h3 class="section-title">Recommended Doctors</h3>
          <p class="section-subtitle">Expert physicians specializing in ${dept.name}</p>
        </div>

        <div class="row gy-4 doctors-grid">
          ${dept.doctors.map((doctorName, index) => {
            const doctor = this.getDoctor(doctorName);
            return doctor ? `
              <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="${${index * 50}}">
                <div class="doctor-card">
                  <div class="doctor-image">
                    <img src="${doctor.image}" alt="${doctor.name}" class="img-fluid">
                    <div class="doctor-overlay">
                      <div class="social-links">
                        <a href="tel:${doctor.phone}" title="Call"><i class="bi bi-telephone"></i></a>
                        <a href="mailto:${doctor.email}" title="Email"><i class="bi bi-envelope"></i></a>
                        <a href="appointment.html" title="Book Appointment"><i class="bi bi-calendar-check"></i></a>
                      </div>
                    </div>
                  </div>
                  <div class="doctor-content">
                    <h4>${doctor.name}</h4>
                    <span class="specialty">${doctor.specialty}</span>
                    <p class="doctor-bio">${doctor.description}</p>
                    <div class="doctor-meta">
                      <div class="experience">
                        <i class="bi bi-award"></i>
                        <span>${doctor.experience}</span>
                      </div>
                      <div class="qualification">
                        <i class="bi bi-book"></i>
                        <span>${doctor.qualification}</span>
                      </div>
                    </div>
                    <div class="doctor-availability">
                      <i class="bi bi-clock"></i>
                      <span>${doctor.availability}</span>
                    </div>
                    <a href="appointment.html" class="btn-appointment btn-sm w-100 mt-3">Book Appointment</a>
                  </div>
                </div>
              </div>
            ` : '';
          }).join('')}
        </div>
      </div>
    `;

    container.innerHTML = doctorsHTML;

    // Reinitialize AOS for new elements
    if (typeof AOS !== 'undefined') {
      AOS.refresh();
    }
  }

  // Load service details
  loadServiceDetails(serviceId) {
    const service = this.getService(serviceId);
    if (!service) return false;

    this.currentService = service;

    // Update page title
    document.title = `${service.title} - Hospital`;

    // Update service header
    const serviceHeader = document.querySelector('.service-header');
    if (serviceHeader) {
      serviceHeader.innerHTML = `
        <div class="service-category">
          <span>${service.name}</span>
        </div>
        <h2>${service.title}</h2>
        <p class="lead">${service.longDescription}</p>
      `;
    }

    // Update service image
    const serviceImage = document.querySelector('.service-visual img');
    if (serviceImage) {
      serviceImage.src = service.image;
      serviceImage.alt = service.title;
    }

    // Update service details items
    const detailsSection = document.querySelector('.service-details');
    if (detailsSection) {
      detailsSection.innerHTML = service.details.map(detail => `
        <div class="detail-item">
          <div class="icon-wrapper">
            <i class="bi ${detail.icon}"></i>
          </div>
          <div class="content">
            <h4>${detail.title}</h4>
            <p>${detail.description}</p>
          </div>
        </div>
      `).join('');
    }

    // Update treatment areas
    this.loadServiceOverview(service);

    return true;
  }

  // Load service overview
  loadServiceOverview(service) {
    const overviewSection = document.querySelector('.treatment-areas');
    if (!overviewSection) return;

    const conditionsList = Array.isArray(service.conditions) ? 
      service.conditions : 
      (service.conditions ? [service.conditions] : []);

    overviewSection.innerHTML = `
      <h4>${service.name} Conditions Treated</h4>
      <div class="condition-tags">
        ${conditionsList.map(condition => `
          <span class="tag">${condition}</span>
        `).join('')}
      </div>
    `;
  }

  // Get icon class for service
  getIconClass(serviceName) {
    const iconMap = {
      'ECG Testing': 'activity',
      'Heart Surgery': 'heart-pulse',
      'Angiography': 'diagram-2',
      'Cardiac Rehabilitation': 'heart',
      'MRI Scans': 'search',
      'Stroke Care': 'hospital',
      'EEG Testing': 'wave-square',
      'Neurological Examination': 'stethoscope',
      'Joint Replacement': 'stethoscope',
      'Sports Medicine': 'person-walking',
      'Arthroscopy': 'tools',
      'Fracture Management': 'shield-plus',
      'Well-Child Visits': 'heart-pulse',
      'Immunizations': 'shield-check',
      'Pediatric Surgery': 'tools',
      'Neonatal Care': 'heart',
      'Skin Cancer Screening': 'eye',
      'Acne Treatment': 'droplet',
      'Cosmetic Procedures': 'brightness-high',
      'Hair Loss Treatment': 'person',
      'Chemotherapy': 'pill',
      'Radiation Therapy': 'radiation',
      'Tumor Surgery': 'tools',
      'Palliative Care': 'heart-hands',
      'Hearing Assessment': 'ear',
      'Sinus Surgery': 'tools',
      'Throat Surgery': 'stethoscope',
      'Hearing Aids': 'volume-up',
      'Endoscopy': 'search',
      'Colonoscopy': 'diagram-2',
      'Ulcer Treatment': 'pill',
      'IBD Management': 'heart-pulse'
    };
    return iconMap[serviceName] || 'check-circle';
  }

  // Initialize from URL parameters
  initFromURL() {
    const params = new URLSearchParams(window.location.search);
    const dept = params.get('dept');
    const service = params.get('service');

    if (dept) {
      this.loadDepartmentDetails(dept);
    } else if (service) {
      this.loadServiceDetails(service);
    }
  }

  // Navigate to department details
  navigateToDepartment(deptId) {
    window.location.href = `department-details.html?dept=${deptId}`;
  }

  // Navigate to service details
  navigateToService(serviceId) {
    window.location.href = `service-details.html?service=${serviceId}`;
  }
}

// Initialize on page load
let contentLoader = new ContentLoader();

document.addEventListener('DOMContentLoaded', function() {
  contentLoader.initFromURL();

  // Reinitialize AOS
  if (typeof AOS !== 'undefined') {
    AOS.init();
  }

  // Initialize tooltips if using Bootstrap
  if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
});
