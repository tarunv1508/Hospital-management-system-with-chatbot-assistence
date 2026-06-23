document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("admin-login-form");
  const loginAlert = document.getElementById("admin-login-alert");
  const loginCard = document.getElementById("admin-login-card");
  const dashboard = document.getElementById("admin-dashboard");
  const logoutButton = document.getElementById("admin-logout-button");
  const departmentList = document.getElementById("department-list");
  const totalAppointments = document.getElementById("total-appointments");
  const totalDepartments = document.getElementById("total-departments");
  const totalDoctors = document.getElementById("total-doctors");
  const doctorAppointmentsCard = document.getElementById("doctor-appointments-card");
  const doctorAppointmentsTitle = document.getElementById("doctor-appointments-title");
  const doctorAppointmentsMeta = document.getElementById("doctor-appointments-meta");
  const doctorAppointmentsBody = document.getElementById("doctor-appointments-body");
  const doctorAppointmentsClose = document.getElementById("doctor-appointments-close");

  async function showError(message) {
    loginAlert.textContent = message;
    loginAlert.classList.remove("d-none");
  }

  function hideError() {
    loginAlert.classList.add("d-none");
  }

  function renderDepartments(departments) {
    departmentList.innerHTML = departments
      .map((department) => {
        return `
          <div class="col-md-6 col-lg-4">
            <div class="card department-card h-100 shadow-sm">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">${department.name}</h5>
                <p class="card-text mb-4">Doctors: ${department.doctor_count}</p>
                <button class="btn btn-primary mt-auto department-view-btn" data-department="${department.id}">View Doctors</button>
              </div>
            </div>
          </div>
        `;
      })
      .join("");

    departmentList.querySelectorAll(".department-view-btn").forEach((button) => {
      button.addEventListener("click", async (event) => {
        const departmentId = event.target.dataset.department;
        const departmentInfo = departments.find((item) => item.id == departmentId);
        if (!departmentInfo) {
          showError("Unable to find department data.");
          return;
        }
        await showDoctorSelection(departmentInfo);
      });
    });
  }

  async function showDoctorSelection(departmentInfo) {
    try {
      const response = await fetch(`/api/departments/${departmentInfo.id}/doctors`, { credentials: "same-origin" });
      const data = await response.json();
      if (!response.ok || data.status !== "OK") {
        showError(data.message || "Unable to load doctors for this department.");
        return;
      }

      const doctors = data.doctors || [];
      if (!doctors.length) {
        showError("No doctors are registered for this department.");
        return;
      }

      const selectionModal = document.createElement("div");
      selectionModal.className = "modal fade";
      selectionModal.tabIndex = -1;
      selectionModal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Select doctor in ${departmentInfo.name}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="list-group" id="doctor-selection-list">
                ${doctors
                  .map(
                    (doctor) =>
                      `<button type="button" class="list-group-item list-group-item-action doctor-select-btn" data-doctor-id="${doctor.id}" data-doctor-name="${doctor.name}">${doctor.name}${doctor.appointment_count ? ` <span class="badge bg-secondary ms-2">${doctor.appointment_count} appts</span>` : ''}</button>`
                  )
                  .join("")}
              </div>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(selectionModal);
      const modal = new bootstrap.Modal(selectionModal, { backdrop: "static" });
      modal.show();

      selectionModal.querySelectorAll(".doctor-select-btn").forEach((button) => {
        button.addEventListener("click", async (event) => {
          const doctorId = event.target.dataset.doctorId;
          const doctorName = event.target.dataset.doctorName;
          modal.hide();
          selectionModal.remove();
          await loadDoctorAppointments(departmentInfo.name, doctorId, doctorName);
        });
      });

      selectionModal.addEventListener("hidden.bs.modal", () => {
        selectionModal.remove();
      });
    } catch (error) {
      showError("Network error while loading doctors.");
    }
  }

  async function loadDoctorAppointments(departmentName, doctorId, doctorName) {
    try {
      const response = await fetch(`/api/doctors/${doctorId}/appointments`, { credentials: "same-origin" });
      const data = await response.json();
      if (!response.ok || data.status !== "OK") {
        showError(data.message || "Unable to load appointments.");
        return;
      }

      doctorAppointmentsTitle.textContent = `${doctorName} — Appointments`;
      doctorAppointmentsMeta.textContent = `${departmentName}`;

      if (!data.appointments || !data.appointments.length) {
        doctorAppointmentsBody.innerHTML = `
          <tr>
            <td colspan="8" class="text-center text-muted">No scheduled appointments found for ${doctorName}.</td>
          </tr>
        `;
      } else {
        doctorAppointmentsBody.innerHTML = data.appointments
          .map((appointment) => {
            return `
              <tr>
                <td>${appointment.id || "-"}</td>
                <td>${appointment.patientName || appointment.name || "-"}</td>
                <td>${appointment.email || "-"}</td>
                <td>${appointment.department || departmentName || "-"}</td>
                <td>${appointment.doctor || doctorName || "-"}</td>
                <td>${appointment.appointment_date || appointment.date || "-"}</td>
                <td>${appointment.appointment_time || appointment.time || "-"}</td>
                <td>${appointment.notes || "-"}</td>
              </tr>
            `;
          })
          .join("");
      }

      doctorAppointmentsCard.classList.remove("d-none");

      doctorAppointmentsCard.classList.remove("d-none");
    } catch (error) {
      showError("Network error while loading appointments.");
    }
  }

  function showLoginView() {
    hideError();
    loginCard.classList.remove("d-none");
    dashboard.classList.add("d-none");
    doctorAppointmentsCard.classList.add("d-none");
  }

  function showDashboardView() {
    loginCard.classList.add("d-none");
    dashboard.classList.remove("d-none");
    doctorAppointmentsCard.classList.add("d-none");
  }

  async function initializeAdminView() {
    showLoginView();
    try {
      const response = await fetch("/api/admin/summary", { credentials: "same-origin" });
      const data = await response.json();
      if (response.ok && data.status === "OK") {
        totalAppointments.textContent = data.summary.total_appointments;
        totalDepartments.textContent = data.summary.total_departments;
        totalDoctors.textContent = data.summary.total_doctors;
        renderDepartments(data.summary.departments);
        showDashboardView();
      }
    } catch (error) {
      // Keep the login view visible if session is not active or request fails.
    }
  }

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideError();

    const username = document.getElementById("admin-username").value.trim();
    const password = document.getElementById("admin-password").value.trim();

    if (!username || !password) {
      showError("Username and password are required.");
      return;
    }

    try {
      const response = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (!response.ok || data.status !== "OK") {
        showError(data.message || "Invalid credentials.");
        return;
      }

      await loadAdminSummary();
      loginCard.classList.add("d-none");
      dashboard.classList.remove("d-none");
    } catch (error) {
      showError("Unable to reach the server. Please try again.");
    }
  });

  logoutButton.addEventListener("click", async () => {
    await fetch("/api/admin/logout", { method: "POST", credentials: "same-origin" });
    loginCard.classList.remove("d-none");
    dashboard.classList.add("d-none");
    doctorAppointmentsCard.classList.add("d-none");
  });

  doctorAppointmentsClose.addEventListener("click", () => {
    doctorAppointmentsCard.classList.add("d-none");
  });

  async function loadAdminSummary() {
    try {
      const response = await fetch("/api/admin/summary", { credentials: "same-origin" });
      const data = await response.json();
      if (!response.ok || data.status !== "OK") {
        showError(data.message || "Unable to load admin data.");
        return;
      }

      totalAppointments.textContent = data.summary.total_appointments;
      totalDepartments.textContent = data.summary.total_departments;
      totalDoctors.textContent = data.summary.total_doctors;
      renderDepartments(data.summary.departments);
    } catch (error) {
      showError("Unable to load admin data.");
    }
  }

  initializeAdminView();
});
