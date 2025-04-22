/**
 * index.js
 *  - Handles login form, task CRUD operations, and UI updates.
 *  - Talks to the backend REST API at /tasks.
 */
(() => {
    // Base URL for all API calls
    const apiBase = `${location.origin}/tasks`;
    let authHeader = ''; // will hold "Basic XYZ==" after login
  
    // Grab references to key DOM elements
    const loginDiv   = document.getElementById('login');
    const appDiv     = document.getElementById('app');
    const loginBtn   = document.getElementById('loginBtn');
    const userInput  = document.getElementById('username');
    const passInput  = document.getElementById('password');
    const refreshBtn = document.getElementById('refreshBtn');
    const createForm = document.getElementById('createForm');
    const tasksBody  = document.getElementById('tasksBody');
  
    // --- EVENT LISTENERS ---
  
    // Click or Enter in login fields triggers login
    loginBtn.addEventListener('click', doLogin);
    [userInput, passInput].forEach(input =>
      input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          e.preventDefault();
          doLogin();
        }
      })
    );
  
    // Refresh button reloads the tasks list
    refreshBtn.addEventListener('click', loadTasks);
  
    // Submitting the create form will POST a new task
    createForm.addEventListener('submit', createTask);
  
    // --- LOGIN HANDLER ---
  
    /** 
     * Attempts to log in by reading username/password,
     * builds a Basic Auth header, then shows the app UI.
     */
    async function doLogin() {
      const u = userInput.value.trim();
      const p = passInput.value.trim();
      if (!u || !p) {
        alert('Enter both username and password');
        return;
      }
  
      // Build the header once, reuse for all API calls
      authHeader = 'Basic ' + btoa(`${u}:${p}`);
  
      // Hide login card, show main app
      loginDiv.style.display = 'none';
      appDiv.style.display   = '';
  
      // Load tasks now that we’re authenticated
      await loadTasks();
    }
  
    // --- TASK LIST & CRUD OPERATIONS ---
  
    /**
     * Fetches all tasks from the backend and re-renders the table.
     */
    async function loadTasks() {
      try {
        const res = await fetch(apiBase, {
          headers: { 'Authorization': authHeader }
        });
        if (!res.ok) throw new Error(res.status);
  
        const tasks = await res.json();
  
        // Build table rows
        tasksBody.innerHTML = tasks.map(task => `
          <tr>
            <td>${task.id}</td>
            <td>${task.title}</td>
            <td>${task.description || ''}</td>
            <td>
              <span class="badge ${task.status.replace(' ', '-')}">
                ${task.status}
              </span>
            </td>
            <td>${task.due || ''}</td>
            <td class="actions">
              <select data-id="${task.id}" class="statusSelect">
                <option ${task.status==='pending'     ? 'selected':''}>pending</option>
                <option ${task.status==='in progress' ? 'selected':''}>in progress</option>
                <option ${task.status==='done'        ? 'selected':''}>done</option>
              </select>
              <button data-id="${task.id}" class="delBtn btn">Delete</button>
            </td>
          </tr>
        `).join('');
  
        // Wire up change/delete handlers on each row
        document.querySelectorAll('.statusSelect')
          .forEach(sel => sel.addEventListener('change', () =>
            updateStatus(sel.dataset.id, sel.value)
          ));
        document.querySelectorAll('.delBtn')
          .forEach(btn => btn.addEventListener('click', () =>
            deleteTask(btn.dataset.id)
          ));
  
      } catch (err) {
        alert('Error loading tasks: ' + err.message);
      }
    }
  
    /**
     * Creates a new task via POST, then reloads the list.
     */
    async function createTask(evt) {
      evt.preventDefault();
      const payload = {
        title:       document.getElementById('newTitle').value.trim(),
        description: document.getElementById('newDesc').value.trim(),
        status:      document.getElementById('newStatus').value,
        due:         document.getElementById('newDue').value
      };
  
      try {
        const res = await fetch(apiBase, {
          method:  'POST',
          headers: {
            'Authorization': authHeader,
            'Content-Type':  'application/json'
          },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(res.status);
  
        createForm.reset();    // clear form
        await loadTasks();      // refresh list
      } catch (err) {
        alert('Create failed: ' + err.message);
      }
    }
  
    /**
     * Updates only the `status` of a task.
     */
    async function updateStatus(id, status) {
      try {
        const res = await fetch(`${apiBase}/${id}/status`, {
          method:  'PATCH',
          headers: {
            'Authorization': authHeader,
            'Content-Type':  'application/json'
          },
          body: JSON.stringify({ status })
        });
        if (!res.ok) throw new Error(res.status);
  
        await loadTasks();
      } catch (err) {
        alert('Update failed: ' + err.message);
      }
    }
  
    /**
     * Deletes a task and reloads the list.
     */
    async function deleteTask(id) {
      if (!confirm(`Delete task #${id}?`)) return;
  
      try {
        const res = await fetch(`${apiBase}/${id}`, {
          method: 'DELETE',
          headers: { 'Authorization': authHeader }
        });
        if (res.status !== 204) throw new Error(res.status);
  
        await loadTasks();
      } catch (err) {
        alert('Delete failed: ' + err.message);
      }
    }
  })();
  