// dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const res = await fetch('/api/dashboard');
        const data = await res.json();
        
        document.getElementById('dash-sales').innerText = `₹${(data.today_sales || 0).toFixed(2)}`;
        document.getElementById('dash-bills').innerText = data.today_bills;
        document.getElementById('dash-products').innerText = data.total_products;
        document.getElementById('dash-lowstock').innerText = data.low_stock_products;
    } catch(e) {}
});
