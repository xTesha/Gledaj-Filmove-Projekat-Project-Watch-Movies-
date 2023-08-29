// Ostatak vašeg postojećeg koda
const API_KEY = 'api_key=hereYouPlaceYourApiKey';
const BASE_URL = 'https://api.themoviedb.org/3';
const LANGUAGE = 'language=hr';
const API_URL = BASE_URL + '/discover/movie?sort_by=popularity.desc&' + LANGUAGE + '&' + API_KEY;
const IMG_URL = 'https://image.tmdb.org/t/p/w500';
const searchURL = BASE_URL + '/search/movie?' + API_KEY + '&' + LANGUAGE;
const main = document.getElementById('main');
const currentPageLabel = document.querySelector('.current-page');
const previousButton = document.querySelector('.left-btn');
const nextButton = document.querySelector('.right-btn');
let currentPage = 1;
let totalPages = 0;
let currentCategory = null;
selectedCategoryID = null;
getMovies(API_URL);

function getMovies(url) {
  if (selectedCategoryID) {
    url = url.replace('discover/movie', 'discover/movie?with_genres=' + selectedCategoryID);
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
      showMovies(data.results, currentPage, totalPages);
      showPagination();
      dodajEventListenereNaIkoneSrca(); // Dodajte ovu liniju ovdje
    });
}

function showMovies(data) {
  main.innerHTML = '';
  data.forEach(movie => {
    const { title, vote_average, poster_path, overview, id } = movie;
    const movieEl = document.createElement('div');
    movieEl.classList.add('movie');
    movieEl.innerHTML = `
      <a href="#"><img src="${IMG_URL + poster_path}"></a>
      <div class="detalji">
        <h6 class="naslovfilma">${title}</h6>
        <span class="rejting">Ocena: ${vote_average}</span>
        <span><i class="fa-solid fa-heart fa-sm wishlist" data-movie-id="${id}" data-opis="${overview}" 
        data-movie-posterpath="${poster_path}"></i></span>
      </div>`;

      
    // Event za odlazak na gledanje filma
    movieEl.addEventListener('click', (event) => {
      if (event.target.tagName.toLowerCase() !== 'i') {
        window.location.href = '/movie/' + id + '?title=' + encodeURIComponent(title) +
          '&overview=' + encodeURIComponent(overview);
      }
    });
    main.appendChild(movieEl);
  });
}

// KATEGORISANJE FILMOVA
const categoryButtons = document.querySelectorAll('.category-btn');
const naslovElement = document.querySelector('.naslov');

categoryButtons.forEach(button => {
  button.addEventListener('click', () => {
    const categoryID = button.dataset.categoryId;
    const categoryName = button.textContent;
    naslovElement.textContent = categoryName;
    const url = `${API_URL}&with_genres=${categoryID}`;
    getMovies(url, categoryID);
  });
});

// PAGINACIJA
function previousPage() {
  if (currentPage > 1) {
    const newPage = currentPage - 1;
    const url = currentCategory ? API_URL + '&page=' + newPage + '&with_genres=' + currentCategory : API_URL + '&page=' + newPage;
    getMovies(url, currentCategory);
	  scrollToTop();
  }
}

function nextPage() {
  if (currentPage < totalPages) {
    const newPage = currentPage + 1;
    const url = currentCategory ? API_URL + '&page=' + newPage + '&with_genres=' + currentCategory : API_URL + '&page=' + newPage;
    getMovies(url, currentCategory);
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

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const searchTerm = search.value;
  if (searchTerm) {
    getMovies(searchURL+'&query='+searchTerm);
  } else {
    getMovies(API_URL);
  }
});

/* Toggle between showing and hiding the navigation menu links when the user clicks on the hamburger menu / bar icon */
function myFunction() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}

function dodajFilmUWatchlist(filmId, naslovFilma, opis, posterpath) {
  const data = {
    filmId: filmId,
    naslovFilma: naslovFilma,
    opis: opis,
    posterpath: posterpath
  };

  fetch('/addToWatchlist', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      // Uspješno dodavanje filma u watchlist
      prikaziPopup('Bravo!', 'Uspesno ste dodali sadrzaj u listu gledanja!.');
    } else {
      // Neuspješno dodavanje filma u watchlist
      console.error('Greška prilikom dodavanja filma u watchlist:', result.message);
    }
  })
  .catch(error => {
    console.error('Greška prilikom slanja zahtjeva:', error);
  });
}

// Funkcija za dodavanje event listenere na ikone srca
function dodajEventListenereNaIkoneSrca() {
  // Dodavanje event listenera na ikone srca
  const wishlistIcons = document.querySelectorAll('.wishlist');

  wishlistIcons.forEach(icon => {
    icon.addEventListener('click', () => {
      const filmId = icon.dataset.movieId;
      const naslovFilma = icon.parentNode.parentNode.querySelector('.naslovfilma').textContent;
      const opis = icon.dataset.opis;
      const posterpath = icon.dataset.moviePosterpath;

      dodajFilmUWatchlist(filmId, naslovFilma, opis, posterpath);
      prikaziPopup('Bravo!', 'Uspješno ste dodali sadržaj u listu gledanja!.');
    });
  });
}



function prikaziPopup(naslov, poruka) {
  const container = document.querySelector('.container.mt-5');
  const popup = document.createElement('div');
  popup.classList.add('alert');
  popup.innerHTML = `
    <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
    <strong class="font__weight-semibold">${naslov}</strong> ${poruka}
  `;

  // Dodavanje popup-a na stranicu
  container.appendChild(popup);
}
