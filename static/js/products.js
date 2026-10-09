let allProducts = [];

document.addEventListener('DOMContentLoaded', loadProducts);

async function loadProducts() {
    const res = await fetch('/api/products');
    allProducts = await res.json();
    renderProductsTable(allProducts);
}

function renderProductsTable(products) {
    const tbody = document.getElementById('products-table-body');
    if(!tbody) return;
    tbody.innerHTML = '';
    
    products.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.category}</td>
                <td>₹${p.price}</td>
                <td>${p.unit}</td>
                <td>${(p.aliases || []).join(', ')}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="deleteProduct(${p.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

function filterProductsTable() {
    const q = document.getElementById('search-products').value.toLowerCase();
    const filtered = allProducts.filter(p => p.name.toLowerCase().includes(q) || (p.aliases && p.aliases.some(a => a.toLowerCase().includes(q))));
    renderProductsTable(filtered);
}

function openAddProductModal() {
    document.getElementById('product-form').reset();
    document.getElementById('prod-id').value = '';
    openModal('product-modal');
}

function closeProductModal() {
    closeModal('product-modal');
}

document.getElementById('product-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('prod-name').value,
        category: document.getElementById('prod-category').value,
        price: parseFloat(document.getElementById('prod-price').value),
        unit: document.getElementById('prod-unit').value,
        gst_percentage: parseFloat(document.getElementById('prod-gst').value || 0),
        stock_quantity: parseFloat(document.getElementById('prod-stock').value || 0)
    };
    
    const id = document.getElementById('prod-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/products/${id}` : '/api/products';
    
    const res = await fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    
    if(res.ok) {
        closeProductModal();
        loadProducts();
        showToast("Product saved!");
    }
});

async function deleteProduct(id) {
    if(confirm("Are you sure?")) {
        await fetch(`/api/products/${id}`, {method: 'DELETE'});
        loadProducts();
    }
}
