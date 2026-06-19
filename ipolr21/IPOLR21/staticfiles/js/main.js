// ========== УТИЛИТЫ ==========

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, isError = false) {
    const toastEl = document.getElementById('cart-toast');
    const toastMsg = document.getElementById('toast-message');
    if (!toastEl || !toastMsg) return;
    toastMsg.textContent = message;
    toastEl.style.borderLeftColor = isError ? '#C62828' : '#8B6E4E';
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
}

function renderProductCard(product) {
    const imgHtml = product.fotto
        ? `<img src="${product.fotto}" alt="${product.name}" class="img-fluid w-100 h-100" style="object-fit:cover;">`
        : `<div class="product-img-placeholder">✦</div>`;

    const inStock = product.quantity_in_stock > 0;
    const actionBtn = inStock
        ? `<a href="/catalog/${product.id}/" class="btn btn-card-action">Подробнее</a>`
        : `<span class="badge bg-secondary">Нет в наличии</span>`;

    return `
        <div class="col-sm-6 col-md-4 col-lg-4">
            <div class="product-card h-100">
                <a href="/catalog/${product.id}/" class="text-decoration-none">
                    <div class="product-card-img">${imgHtml}</div>
                    <div class="product-card-body">
                        <p class="product-category">${product.category_name || ''}</p>
                        <h6 class="product-name">${product.name}</h6>
                        <p class="product-manufacturer text-muted small">${product.manufacturer_name || ''}</p>
                    </div>
                </a>
                <div class="product-card-footer">
                    <span class="product-price">${product.price} BYN</span>
                    ${actionBtn}
                </div>
            </div>
        </div>`;
}

// ========== ЗАДАНИЕ 6: Загрузка товаров из API ==========

function loadPopularProducts() {
    const container = document.getElementById('popular-products');
    const spinner = document.getElementById('products-spinner');
    const errorEl = document.getElementById('products-error');

    if (!container) return;

    // Показываем спиннер
    if (spinner) spinner.style.display = 'block';
    container.style.display = 'none';
    if (errorEl) errorEl.classList.add('d-none');

    fetch('/api/products/', {
        headers: {
            'Accept': 'application/json',
        },
        credentials: 'same-origin',
    })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сети: ' + response.status);
            return response.json();
        })
        .then(data => {
            const products = Array.isArray(data) ? data : (data.results || []);
            const popular = products.slice(0, 6);

            if (spinner) spinner.style.display = 'none';
            container.style.display = 'flex';

            if (popular.length === 0) {
                container.innerHTML = '<div class="col-12 text-center text-muted py-4">Товары не найдены</div>';
                return;
            }

            container.innerHTML = popular.map(renderProductCard).join('');
        })
        .catch(error => {
            console.error('Ошибка загрузки товаров:', error);
            if (spinner) spinner.style.display = 'none';
            if (errorEl) errorEl.classList.remove('d-none');
        });
}

// ========== ЗАДАНИЕ 6: Добавление в корзину через API ==========

function addToCart(productId) {
    const csrfToken = getCookie('csrftoken');

    fetch(`/cart/add/${productId}/`, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
        .then(response => {
            if (response.redirected || response.ok) {
                showToast('✦ Товар добавлен в корзину!');
            } else {
                throw new Error('Ошибка');
            }
        })
        .catch(() => {
            showToast('Не удалось добавить товар. Войдите в аккаунт.', true);
        });
}

// ========== ИНИЦИАЛИЗАЦИЯ ==========

document.addEventListener('DOMContentLoaded', function () {
    // Подсветка активного пункта навигации
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});