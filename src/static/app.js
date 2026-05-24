const status = document.getElementById('status');
const resultsContainer = document.getElementById('results');
const filesContainer = document.getElementById('files');
const filePreview = document.getElementById('filePreview');
const searchButton = document.getElementById('searchButton');
const queryInput = document.getElementById('query');

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Server returned ${response.status}`);
  }
  return response.json();
}

function renderSearchResults(data) {
  if (!data.results || data.results.length === 0) {
    resultsContainer.innerHTML = '<p class="empty">No results found for this query.</p>';
    return;
  }

  resultsContainer.innerHTML = data.results
    .map(
      (item) => `
      <article class="result-card">
        <header>
          <strong>#${item.rank}</strong>
          <span>${item.filename}</span>
          <small>score: ${item.score}</small>
        </header>
        <p>${item.preview.replace(/\n/g, '<br>')}...</p>
        <footer>Matched Keywords: ${item.keywords_matched.join(', ') || 'None'}</footer>
      </article>
    `
    )
    .join('');
}

function renderFileList(files) {
  if (!files || files.length === 0) {
    filesContainer.innerHTML = '<p class="empty">No files available.</p>';
    return;
  }

  filesContainer.innerHTML = files
    .map(
      (file) => `
      <button class="file-button" data-filename="${encodeURIComponent(file.filename)}">
        ${file.filename}
      </button>
    `
    )
    .join('');

  document.querySelectorAll('.file-button').forEach((button) => {
    button.addEventListener('click', () => {
      const filename = decodeURIComponent(button.dataset.filename);
      loadFile(filename);
    });
  });
}

function renderFilePreview(document) {
  filePreview.innerHTML = `
    <h3>${document.filename}</h3>
    <p><strong>Keywords:</strong> ${document.unique_keywords.slice(0, 20).join(', ')}</p>
    <pre>${document.original_text}</pre>
  `;
}

async function loadFile(filename) {
  try {
    status.textContent = `Loading ${filename}...`;
    const data = await fetchJson(`/api/file/${encodeURIComponent(filename)}`);
    renderFilePreview(data);
    status.textContent = `Showing ${filename}`;
  } catch (error) {
    status.textContent = 'Unable to load file details.';
    console.error(error);
  }
}

async function searchQuery() {
  const query = queryInput.value.trim();
  if (!query) {
    status.textContent = 'Please enter a search query.';
    return;
  }

  status.textContent = `Searching for: ${query}`;
  try {
    const data = await fetchJson(`/api/search?query=${encodeURIComponent(query)}`);
    renderSearchResults(data);
    status.textContent = `Search complete: ${data.results.length} results.`;
  } catch (error) {
    status.textContent = 'Search failed. Check backend logs.';
    console.error(error);
  }
}

async function loadFiles() {
  try {
    const data = await fetchJson('/api/files');
    renderFileList(data.files);
  } catch (error) {
    filesContainer.innerHTML = '<p class="empty">Unable to load files list.</p>';
    console.error(error);
  }
}

searchButton.addEventListener('click', searchQuery);
queryInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    searchQuery();
  }
});

loadFiles();
