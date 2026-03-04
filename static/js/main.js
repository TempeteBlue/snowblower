/**
 * Main site scripts
 */

// Mobile menu
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.querySelector('.nav-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function() {
      const isExpanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !isExpanded);
      mainNav.classList.toggle('active');
    });
  }
  
  // Search
  initSearch();
});

// Search function
function initSearch() {
  const searchInput = document.getElementById('site-search');
  const searchBtn = document.getElementById('search-btn');
  
  if (!searchInput) return;
  
  // Load search index
  const searchIndexPath = '/search-index.json';
  
  fetch(searchIndexPath)
    .then(response => {
      if (!response.ok) {
        throw new Error('Index not found');
      }
      return response.json();
    })
    .then(data => {
      window.searchIndex = data;
      console.log('Search index loaded:', data.length, 'pages');
    })
    .catch(err => {
      console.log('Search index not available:', err);
      window.searchIndex = [];
    });
  
  // Search handling
  function performSearch(query) {
    if (!query) return;
    
    if (!window.searchIndex) {
      alert('Search index is loading, please wait a few seconds and try again.');
      return;
    }
    
    query = query.toLowerCase();
    const results = window.searchIndex.filter(item => {
      return item.title.toLowerCase().includes(query) ||
             item.description.toLowerCase().includes(query) ||
             (item.content && item.content.toLowerCase().includes(query));
    }).slice(0, 10);
    
    displaySearchResults(results);
  }
  
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      performSearch(this.value);
    }
  });
  
  if (searchBtn) {
    searchBtn.addEventListener('click', function() {
      performSearch(searchInput.value);
    });
  }
}

// Display search results
function displaySearchResults(results) {
  // Remove previous results
  const existingResults = document.querySelector('.search-results');
  if (existingResults) {
    existingResults.remove();
  }
  
  if (results.length === 0) {
    alert('No results found');
    return;
  }
  
  // Create results container
  const resultsDiv = document.createElement('div');
  resultsDiv.className = 'search-results';
  resultsDiv.innerHTML = `
    <div class="search-results-overlay" onclick="this.parentElement.remove()"></div>
    <div class="search-results-content">
      <button class="search-close" onclick="this.closest('.search-results').remove()">×</button>
      <h2>${results.length} result(s)</h2>
      <ul>
        ${results.map(r => `
          <li>
            <a href="${r.url}">
              <strong>${r.title}</strong>
              <p>${r.description || ''}</p>
            </a>
          </li>
        `).join('')}
      </ul>
    </div>
  `;
  
  document.body.appendChild(resultsDiv);
}

// Carousel functionality
window.currentSlide = 0;
window.slideCount = 0;
window.carouselTrack = null;

function initCarousel() {
  console.log('Initializing carousel...');
  const track = document.getElementById('carouselTrack');
  if (!track) {
    console.log('No carousel track found');
    return;
  }
  
  const count = track.children.length;
  console.log('Carousel found with', count, 'slides');
  
  if (count <= 1) {
    console.log('Not enough slides for carousel');
    return;
  }
  
  window.carouselTrack = track;
  window.currentSlide = 0;
  window.slideCount = count;
  console.log('Carousel initialized successfully');
}

function moveCarousel(direction) {
  console.log('Moving carousel', direction);
  const track = window.carouselTrack;
  if (!track) {
    console.log('No carousel track available');
    return;
  }
  
  window.currentSlide += direction;
  
  if (window.currentSlide < 0) {
    window.currentSlide = window.slideCount - 1;
  } else if (window.currentSlide >= window.slideCount) {
    window.currentSlide = 0;
  }
  
  track.style.transform = `translateX(-${window.currentSlide * 100}%)`;
  updateDots();
}

function goToSlide(index) {
  console.log('Going to slide', index);
  const track = window.carouselTrack;
  if (!track) {
    console.log('No carousel track available');
    return;
  }
  
  window.currentSlide = index;
  track.style.transform = `translateX(-${window.currentSlide * 100}%)`;
  updateDots();
}

function moveCarousel(direction) {
  const track = window.carouselTrack;
  if (!track) return;
  
  window.currentSlide += direction;
  
  if (window.currentSlide < 0) {
    window.currentSlide = window.slideCount - 1;
  } else if (window.currentSlide >= window.slideCount) {
    window.currentSlide = 0;
  }
  
  track.style.transform = `translateX(-${window.currentSlide * 100}%)`;
  updateDots();
}

function goToSlide(index) {
  const track = window.carouselTrack;
  if (!track) return;
  
  window.currentSlide = index;
  track.style.transform = `translateX(-${window.currentSlide * 100}%)`;
  updateDots();
}

function updateDots() {
  const dots = document.querySelectorAll('.carousel-dot');
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === window.currentSlide);
  });
}

// Make functions globally available for onclick handlers
window.moveCarousel = moveCarousel;
window.goToSlide = goToSlide;

// Initialize carousel on page load
document.addEventListener('DOMContentLoaded', initCarousel);
