let allStock = [];

document.addEventListener('DOMContentLoaded', loadStock);

async function loadStock() {
    const res = await fetch('/api/stock');
    allStock = await res.json();
    renderStockTable(allStock);
}

function renderStockTable(stock) {
    const tbody = document.getElementById('stock-table-body');
    if(!tbody) return;
    tbody.innerHTML = '';
    
    stock.forEach(s => {
        const isLow = s.stock_quantity <= s.minimum_stock;
        tbody.innerHTML += `
            <tr>
                <td>${s.id}</td>
                <td>${s.name}</td>
                <td>${s.category}</td>
                <td class="${isLow ? 'danger-text' : ''}">${s.stock_quantity} ${s.unit}</td>
                <td>${s.minimum_stock}</td>
                <td>${isLow ? '<span class="danger-text">Low Stock</span>' : 'OK'}</td>
                <td>
                    <div style="display: flex; gap: 8px;">
                        <input type="number" id="stock-update-${s.id}" value="${s.stock_quantity}" style="width: 80px;">
                        <button class="btn btn-primary btn-sm" onclick="updateStock(${s.id})">Update</button>
                    </div>
                </td>
            </tr>
        `;
    });
}

function filterStockTable() {
    const q = document.getElementById('search-stock').value.toLowerCase();
    const filtered = allStock.filter(s => s.name.toLowerCase().includes(q));
    renderStockTable(filtered);
}

async function updateStock(id) {
    const val = document.getElementById(`stock-update-${id}`).value;
    const res = await fetch(`/api/stock/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({stock_quantity: parseFloat(val)})
    });
    
    if(res.ok) {
        showToast("Stock updated!");
        loadStock();
    }
}
