const api_key = 'api_key=putYourApiKeyHereAlso';
const base_url = 'https://api.themoviedb.org/3';
const LANGUAGE = 'language=hr'; 
const api_url = base_url + '/trending/tv/week?' + LANGUAGE + '&' + api_key;
const img_url = 'https://image.tmdb.org/t/p/w500';
const searchurl = base_url + '/search/tv?' + api_key+ '&'+LANGUAGE;
const main = document.getElementById('main');
const currentPageLabel = document.querySelector('.current-page');
const previousButton = document.querySelector('.left-btn');
const nextButton = document.querySelector('.right-btn');
let currentPage = 1;
let totalPages = 0;
let currentCategory = null;

getSeries(api_url);

function getSeries(url, selectedCategoryID = null) {
  if (selectedCategoryID) {
    url = url.replace('trending/tv/week', 'discover/tv?with_genres=' + selectedCategoryID);
    currentCategory = selectedCategoryID;
  } else {
    currentCategory = null;
  }
  fetch(url)
    .then(res => res.json())
    .then(data => {
      console.log(data);
      currentPage = data.page;
      totalPages = data.total_pages;
      showSeries(data.results, currentPage, totalPages);
      showPagination();
    });
}

function showSeries(data, currentPage, totalPages) {
  main.innerHTML = '';
  data.forEach(serie => {
    const { name, vote_average, poster_path, overview, id } = serie;
    const serieEl = document.createElement('div');
    serieEl.classList.add('movie');
    serieEl.innerHTML = `
      <a href="#"><img src="${img_url + poster_path}"></a>
      <div class="detalji">
        <h6 class="naslovFilma">${name}</h6>
        <span class="rejting">Ocena: ${vote_average}</span>
        <span><i class="fa-solid fa-heart fa-sm wishlist" data-movie-id="${id}"></i></span>
      </div>
    `;

    serieEl.addEventListener('click', () => {
      window.location.href = '/serije/' + id + '?title=' + encodeURIComponent(name) + '&overview=' + encodeURIComponent(overview);
    });

    main.appendChild(serieEl);
  });
}

// KATEGORISANJE SERIJA
const categoryButtonsSeries = document.querySelectorAll('.series-btn');
const naslovElement = document.querySelector('.naslov');

categoryButtonsSeries.forEach(button => {
  button.addEventListener('click', () => {
    const categoryID = button.dataset.categoryId;
    const categoryName = button.textContent;
    naslovElement.textContent = categoryName;
    const url = `${api_url}&with_genres=${categoryID}`;
    getSeries(url, categoryID);
    setHeartColors();
  });
});

// PAGINACIJA
function previousPage() {
  if (currentPage > 1) {
    const newPage = currentPage - 1;
    const url = currentCategory ? api_url + '&page=' + newPage + '&with_genres=' + currentCategory : api_url + '&page=' + newPage;
    getSeries(url, currentCategory);
    scrollToTop();
  }
}

function nextPage() {
  if (currentPage < totalPages) {
    const newPage = currentPage + 1;
    const url = currentCategory ? api_url + '&page=' + newPage + '&with_genres=' + currentCategory : api_url + '&page=' + newPage;
    getSeries(url, currentCategory);
    scrollToTop();
  }
}

previousButton.addEventListener('click', previousPage);
nextButton.addEventListener('click', nextPage);

function showPagination() {
  currentPageLabel.textContent = `${currentPage} od ${totalPages}`;
  previousButton.disabled = currentPage === 1;
  nextButton.disabled = currentPage === totalPages;
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// PRETRAGA
const form = document.getElementById('form');
const search = document.getElementById('search');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const searchTerm = search.value;
  if (searchTerm) {
    getSeries(searchurl + '&query=' + searchTerm);
  } else {
    getSeries(api_url);
  }
});

function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}
