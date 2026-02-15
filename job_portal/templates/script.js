// =============================================
// Fake database using localStorage
// =============================================

const USERS_KEY = 'jobportal_users';
const JOBS_KEY   = 'jobportal_jobs';
const APPLICATIONS_KEY = 'jobportal_applications';

// Initialize if not exists
if (!localStorage.getItem(USERS_KEY)) {
  localStorage.setItem(USERS_KEY, JSON.stringify([]));
}
if (!localStorage.getItem(JOBS_KEY)) {
  localStorage.setItem(JOBS_KEY, JSON.stringify([
    {
      id: 1,
      company: "Google",
      title: "Frontend Developer",
      category: "Core Software Development Roles",
      skills: "HTML, CSS, JavaScript, React",
      description: "Build beautiful and responsive user interfaces."
    },
    {
      id: 2,
      company: "Microsoft",
      title: "Backend Developer",
      category: "Core Software Development Roles",
      skills: "Node.js, Python, SQL",
      description: "Develop scalable backend systems and APIs."
    },
    {
      id: 3,
      company: "Amazon",
      title: "Machine Learning Engineer",
      category: "Data & AI Related Roles",
      skills: "Python, TensorFlow, PyTorch",
      description: "Build and deploy ML models at scale."
    },
    {
      id: 4,
      company: "Cloudflare",
      title: "Cloud Security Engineer",
      category: "Security & Networking Roles",
      skills: "Cloud security, firewalls, penetration testing",
      description: "Protect cloud infrastructure from threats."
    }
  ]));
}
if (!localStorage.getItem(APPLICATIONS_KEY)) {
  localStorage.setItem(APPLICATIONS_KEY, JSON.stringify([]));
}

// Helper functions
function getUsers()          { return JSON.parse(localStorage.getItem(USERS_KEY) || '[]'); }
function saveUsers(users)    { localStorage.setItem(USERS_KEY, JSON.stringify(users)); }
function getJobs()           { return JSON.parse(localStorage.getItem(JOBS_KEY) || '[]'); }
function saveJobs(jobs)      { localStorage.setItem(JOBS_KEY, JSON.stringify(jobs)); }
function getApplications()   { return JSON.parse(localStorage.getItem(APPLICATIONS_KEY) || '[]'); }
function saveApplications(apps) { localStorage.setItem(APPLICATIONS_KEY, JSON.stringify(apps)); }

function getCurrentUser() {
  const email = localStorage.getItem('currentUser');
  if (!email) return null;
  const users = getUsers();
  return users.find(u => u.email === email) || null;
}

function isLoggedIn() {
  return !!localStorage.getItem('currentUser');
}

function isRecruiter() {
  const user = getCurrentUser();
  return user && user.role === 'recruiter';
}

// Register
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', e => {
    e.preventDefault();
    const name  = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const pass  = document.getElementById('regPassword').value;
    const role  = document.getElementById('regRole').value;

    if (!name || !email || !pass || !role) {
      alert("Please fill all fields");
      return;
    }

    const users = getUsers();
    if (users.some(u => u.email === email)) {
      alert("Email already registered!");
      return;
    }

    users.push({ name, email, password: pass, role });
    saveUsers(users);
    alert("Registration successful! Please login.");
    window.location.href = "login.html";
  });
}

// Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', e => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const pass  = document.getElementById('loginPassword').value;

    const users = getUsers();
    const user = users.find(u => u.email === email && u.password === pass);

    if (!user) {
      alert("Invalid email or password");
      return;
    }

    localStorage.setItem('currentUser', email);
    alert("Login successful!");

    if (user.role === 'jobseeker') {
      window.location.href = "jobseeker-dashboard.html";
    } else {
      window.location.href = "recruiter-dashboard.html";
    }
  });
}

// Logout function (add to buttons where needed)
function logout() {
  localStorage.removeItem('currentUser');
  window.location.href = "index.html";
}

// Protect recruiter pages
if (window.location.pathname.includes('recruiter') ||
    window.location.pathname.includes('post-job') ||
    window.location.pathname.includes('applicants')) {
  if (!isLoggedIn() || !isRecruiter()) {
    alert("Please login as Recruiter to access this page");
    window.location.href = "login.html";
  }
}

// Protect apply page
if (window.location.pathname.includes('application-form.html')) {
  if (!isLoggedIn()) {
    alert("Please login to apply for jobs");
    localStorage.setItem('redirectAfterLogin', window.location.href);
    window.location.href = "login.html";
  }
}

// Job list – search + filter
const jobListContainer = document.getElementById('jobListContainer');
if (jobListContainer) {
  const jobs = getJobs();

  function renderJobs(jobsToShow) {
    jobListContainer.innerHTML = '';
    if (jobsToShow.length === 0) {
      jobListContainer.innerHTML = '<p>No jobs found.</p>';
      return;
    }

    jobsToShow.forEach(job => {
      const div = document.createElement('div');
      div.className = 'job-card';
      div.innerHTML = `
        <h3>${job.title}</h3>
        <p><b>Company:</b> ${job.company}</p>
        <p><b>Category:</b> ${job.category}</p>
        <a href="job-details.html?id=${job.id}" class="btn">View Details</a>
      `;
      jobListContainer.appendChild(div);
    });
  }

  renderJobs(jobs);

  // Search
  document.getElementById('searchInput')?.addEventListener('input', e => {
    const term = e.target.value.toLowerCase().trim();
    const filtered = jobs.filter(j =>
      j.company.toLowerCase().includes(term) ||
      j.title.toLowerCase().includes(term) ||
      j.category.toLowerCase().includes(term)
    );
    renderJobs(filtered);
  });
}

// Job details
const jobDetailContainer = document.getElementById('jobDetailContainer');
if (jobDetailContainer) {
  const urlParams = new URLSearchParams(window.location.search);
  const id = parseInt(urlParams.get('id'));
  const jobs = getJobs();
  const job = jobs.find(j => j.id === id);

  if (!job) {
    jobDetailContainer.innerHTML = "<h2>Job not found</h2>";
  } else {
    jobDetailContainer.innerHTML = `
      <h2>${job.title}</h2>
      <p><b>Company:</b> ${job.company}</p>
      <p><b>Category:</b> ${job.category}</p>
      <p><b>Required Skills:</b> ${job.skills}</p>
      <p><b>Description:</b><br>${job.description}</p>
      <a href="application-form.html?id=${job.id}" class="btn big">Apply Now</a>
    `;
  }
}

// Application form
const applyForm = document.getElementById('applyForm');
if (applyForm) {
  applyForm.addEventListener('submit', e => {
    e.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const jobId = parseInt(urlParams.get('id'));

    if (!jobId) {
      alert("Invalid job");
      return;
    }

    // You can collect more data here if needed
    const apps = getApplications();
    apps.push({
      jobId,
      applicantEmail: getCurrentUser().email,
      name: getCurrentUser().name,
      appliedAt: new Date().toISOString()
      // resume, etc. – not really stored
    });
    saveApplications(apps);

    window.location.href = "application-success.html";
  });
}

// Applicants list (for recruiter)
const applicantsListContainer = document.getElementById('applicantsList');
if (applicantsListContainer) {
  const apps = getApplications();
  const jobs = getJobs();

  if (apps.length === 0) {
    applicantsListContainer.innerHTML = "<p>No applications yet.</p>";
  } else {
    const grouped = {};

    apps.forEach(app => {
      if (!grouped[app.jobId]) grouped[app.jobId] = [];
      grouped[app.jobId].push(app);
    });

    for (const jobId in grouped) {
      const job = jobs.find(j => j.id == jobId);
      if (!job) continue;

      const h3 = document.createElement('h3');
      h3.textContent = `${job.title} @ ${job.company} (${grouped[jobId].length} applicants)`;
      applicantsListContainer.appendChild(h3);

      grouped[jobId].forEach(app => {
        const p = document.createElement('p');
        p.innerHTML = `
          ${app.name} (${app.applicantEmail})
          <button onclick="alert('Resume download simulation for ${app.name}')">Download Resume</button>
          <br><small>Applied: ${new Date(app.appliedAt).toLocaleString()}</small>
        `;
        applicantsListContainer.appendChild(p);
      });
    }
  }
}

// Post job (recruiter)
const postJobForm = document.getElementById('postJobForm');
if (postJobForm) {
  postJobForm.addEventListener('submit', e => {
    e.preventDefault();

    const title       = document.getElementById('jobTitle').value.trim();
    const company     = document.getElementById('companyName').value.trim();
    const category    = document.getElementById('jobCategory').value;
    const skills      = document.getElementById('skills').value.trim();
    const description = document.getElementById('description').value.trim();

    if (!title || !company || !category || !skills || !description) {
      alert("Please fill all fields");
      return;
    }

    const jobs = getJobs();
    const newId = jobs.length ? Math.max(...jobs.map(j => j.id)) + 1 : 1;

    jobs.push({
      id: newId,
      company,
      title,
      category,
      skills,
      description
    });

    saveJobs(jobs);
    window.location.href = "post-job-success.html";
  });
}