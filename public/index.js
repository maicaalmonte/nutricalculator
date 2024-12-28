// Function to fetch data from the Flask server
function fetchData() {
    const page = document.getElementById('page').value;
    const limit = document.getElementById('limit').value;
    const language = document.getElementById('language') ? document.getElementById('language').value : 'en';  // Ensure language is passed

    const status = document.getElementById('status');
    const dataTable = document.getElementById('data-table').getElementsByTagName('tbody')[0];

    // Show loading status
    status.textContent = 'Loading...';

    // Make AJAX request to Flask server
    const formData = new FormData();
    formData.append('page', page);
    formData.append('limit', limit);
    formData.append('language', language);

    fetch('/fetch_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const products = data.data;
            updateTable(products);
            status.textContent = '';
        } else {
            status.textContent = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        status.textContent = 'An error occurred while fetching the data.';
    });
}

// Function to update the data table
function updateTable(products) {
    const dataTable = document.getElementById('data-table').getElementsByTagName('tbody')[0];
    dataTable.innerHTML = '';  // Clear existing data in the table

    products.forEach(product => {
        const row = dataTable.insertRow();

        const productNameCell = row.insertCell(0);
        const brandCell = row.insertCell(1);
        const ingredientsCell = row.insertCell(2);
        const quantityCell = row.insertCell(3);
        const codeCell = row.insertCell(4);
        const energyCell = row.insertCell(5);
        const fatCell = row.insertCell(6);
        const carbsCell = row.insertCell(7);
        const sugarsCell = row.insertCell(8);
        const proteinsCell = row.insertCell(9);
        const saltCell = row.insertCell(10);
        const fiberCell = row.insertCell(11);
        const vitACell = row.insertCell(12);
        const vitCCell = row.insertCell(13);
        const calciumCell = row.insertCell(14);
        const ironCell = row.insertCell(15);
        const magnesiumCell = row.insertCell(16);
        const potassiumCell = row.insertCell(17);

        // Fill in the row with data
        productNameCell.textContent = product.product_name;
        brandCell.textContent = product.brands;
        ingredientsCell.textContent = product.ingredients_text;
        quantityCell.textContent = product.quantity;
        codeCell.textContent = product.code;
        energyCell.textContent = product['energy-kcal_100g'];
        fatCell.textContent = product['fat_100g'];
        carbsCell.textContent = product['carbohydrates_100g'];
        sugarsCell.textContent = product['sugars_100g'];
        proteinsCell.textContent = product['proteins_100g'];
        saltCell.textContent = product['salt_100g'];
        fiberCell.textContent = product['fiber_100g'];
        vitACell.textContent = product['vitamin-a_100g'];
        vitCCell.textContent = product['vitamin-c_100g'];
        calciumCell.textContent = product['calcium_100g'];
        ironCell.textContent = product['iron_100g'];
        magnesiumCell.textContent = product['magnesium_100g'];
        potassiumCell.textContent = product['potassium_100g'];
    });
}

// Function to fetch news articles from the Flask server
function fetchNews() {
    const newsArticlesDiv = document.getElementById('news-articles');

    newsArticlesDiv.innerHTML = '<p>Loading news...</p>';  // Show loading text

    fetch('/fetch_news')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const articles = data.articles;
            updateNews(articles);
        } else {
            newsArticlesDiv.innerHTML = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        newsArticlesDiv.innerHTML = 'An error occurred while fetching news.';
    });
}

// Function to update the news section
function updateNews(articles) {
    const newsArticlesDiv = document.getElementById('news-articles');
    newsArticlesDiv.innerHTML = '';  // Clear existing news

    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.classList.add('news-article');

        const title = document.createElement('h3');
        title.textContent = article.title;
        articleDiv.appendChild(title);

        const description = document.createElement('p');
        description.textContent = article.description || 'No description available.';
        articleDiv.appendChild(description);

        newsArticlesDiv.appendChild(articleDiv);
    });
}

// Call fetchNews() once to load initial news
fetchNews();
