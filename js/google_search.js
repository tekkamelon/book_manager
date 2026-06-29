const params = new URLSearchParams(window.location.search);
const isbn = params.get('isbn') || '';

document.getElementById('isbn_display').textContent = isbn || '不明';

if (isbn) {
	const encoded = encodeURIComponent(isbn);
	document.getElementById('google_search_link').href =
		'https://www.google.com/search?q=' + encoded;
}
