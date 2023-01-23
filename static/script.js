const API_KEY = 'api_key=c5632362513441998856f721496efc81'
const BASE_URL = 'https://api.themoviedb.org/3'
const API_URL = BASE_URL + '/discover/movie?sort_by=popularity.desc&' + API_KEY;
const IMG_URL = 'https://image.tmdb.org/t/p/w500'
const searchURL = BASE_URL + '/search/movie?'+ API_KEY;
const form = document.getElementById('form')
const search = document.getElementById('search')
const main = document.getElementById('main')


getMovies(API_URL);

function getMovies(url) {

	fetch(url).then(res => res.json()).then(data => {
		
		showMovies(data.results);
		console.log(data)
	})
}

function showMovies(data){
main.innerHTML = '';
	data.forEach(movie => {
		const {title, vote_average, poster_path, overview, id} = movie
		const movieEl = document.createElement('div')
		movieEl.classList.add('movie')
		movieEl.innerHTML = `
			
				<a href="#"><img src="${IMG_URL + poster_path}"></a>
				<div class="detalji">
				<h6 class="naslov">${title}</h6>
				<span class="rejting">Ocena: ${vote_average}</span>
				</div>
		`

movieEl.addEventListener('click', () => {
    window.location.href = '/movie/' + id + '?title=' + title + '&overview=' + overview;

    
});


     main.appendChild(movieEl);

	})
}

form.addEventListener('submit', (e) => {
	e.preventDefault();

	const searchTerm = search.value;

	if(searchTerm){
		getMovies(searchURL+'&query='+searchTerm)
	}else{
		getMovies(API_URL);
	}
})

/*Korisnik je ulogovan i menja se dugme*/



function onLogin() {
                        document.querySelector('#user-nav-logged-in').show();
                    }
