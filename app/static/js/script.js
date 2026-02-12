async function loadMovies() {
  try {
    const resp = await fetch('/api/movies');
    if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
    const movies = await resp.json();
    const list = document.getElementById('movie-list');
    if (!list) return;
    list.innerHTML = '';
    if (!movies || movies.length === 0) {
      list.innerHTML = '<li>No movies found.</li>';
      return;
    }
    movies.forEach(movie => {
      const li = document.createElement('li');
      li.className = 'movie-card';
      li.innerHTML = `
        <img src="${movie.poster || 'https://via.placeholder.com/150x220?text=No+Image'}" alt="${movie.title || ''}" class="poster"/>
        <div class="info">
          <h3>${movie.title || 'Untitled'}</h3>
          <p><strong>Year:</strong> ${movie.year || 'N/A'}</p>
          <p><strong>Duration:</strong> ${movie.duration || 'N/A'} min</p>
          <p>${movie.description || ''}</p>
          <div class="actions">
            <button onclick="deleteMovie(${movie.id})">Delete</button>
          </div>
        </div>
      `;
      list.appendChild(li);
    });
  } catch (e) {
    console.error('Error loading movies:', e);
    alert('Failed to load movies.');
  }
}

async function deleteMovie(id) {
  if (!confirm('Are you sure you want to delete this movie?')) return;
  try {
    const resp = await fetch(`/api/movies/${id}`, { method: 'DELETE' });
    if (resp.ok) {
      alert('Deleted');
      loadMovies();
    } else {
      const data = await resp.json();
      alert(data.error || 'Error deleting movie.');
    }
  } catch (e) {
    console.error('Error deleting:', e);
    alert('Connection error while deleting.');
  }
}

function setupRegisterForm() {
  const form = document.getElementById('register-form');
  if (!form) return;
  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const formData = new FormData(form);
    const payload = {
      title: formData.get('title'),
      year: formData.get('year') ? parseInt(formData.get('year')) : null,
      duration: formData.get('duration') ? parseInt(formData.get('duration')) : null,
      poster: formData.get('poster'),
      description: formData.get('description')
    };
    try {
      const resp = await fetch('/api/movies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (resp.ok) {
        window.location.href = '/success';
      } else {
        alert(data.error || 'Failed to add movie.');
      }
    } catch (e) {
      console.error('Error adding movie:', e);
      alert('Connection error while adding movie.');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('movie-list')) loadMovies();
  setupRegisterForm();
});