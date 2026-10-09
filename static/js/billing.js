// billing.js

let cart = [];
let allProducts = [];
let settings = {};

document.addEventListener('DOMContentLoaded', async () => {
    // Load products
    const res = await fetch('/api/products');
    allProducts = await res.json();
    renderProducts(allProducts);

    // Load settings for GST calculation
    const sRes = await fetch('/api/settings');
    settings = await sRes.json();
});

function renderProducts(products) {
    const grid = document.getElementById('products-grid');
    if(!grid) return;
    grid.innerHTML = '';
    
    products.forEach(p => {
        const div = document.createElement('div');
        div.className = 'product-card';
        div.innerHTML = `
            <div class="product-name">${p.name}</div>
            <div class="product-price">₹${p.price} / ${p.unit}</div>
        `;
        div.onclick = () => {
            addToCart({
                product_id: p.id,
                name: p.name,
                price: p.price,
                quantity: 1,
                unit: p.unit
            });
        };
        grid.appendChild(div);
    });
}

document.getElementById('product-search')?.addEventListener('keyup', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = allProducts.filter(p => p.name.toLowerCase().includes(query) || (p.aliases && p.aliases.some(a => a.toLowerCase().includes(query))));
    renderProducts(filtered);
});

function addToCart(item) {
    const existing = cart.find(c => c.product_id === item.product_id);
    if(existing) {
        existing.quantity += item.quantity;
        existing.total = existing.quantity * existing.price;
    } else {
        item.total = item.quantity * item.price;
        cart.push(item);
    }
    renderCart();
    
    // Play sound
    document.getElementById('success-sound').play().catch(()=>{});
}

function removeFromCart(index) {
    cart.splice(index, 1);
    renderCart();
}

function updateQty(index, delta) {
    cart[index].quantity += delta;
    if(cart[index].quantity <= 0) {
        removeFromCart(index);
    } else {
        cart[index].total = cart[index].quantity * cart[index].price;
        renderCart();
    }
}

function renderCart() {
    const tbody = document.getElementById('cart-body');
    if(!tbody) return;
    tbody.innerHTML = '';
    
    let subtotal = 0;
    cart.forEach((item, index) => {
        subtotal += item.total;
        tbody.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" style="padding: 2px 6px;" onclick="updateQty(${index}, -1)">-</button>
                    ${item.quantity} ${item.unit}
                    <button class="btn btn-secondary btn-sm" style="padding: 2px 6px;" onclick="updateQty(${index}, 1)">+</button>
                </td>
                <td>₹${item.price}</td>
                <td>₹${item.total.toFixed(2)}</td>
                <td><button class="btn btn-danger" style="padding: 4px 8px;" onclick="removeFromCart(${index})">X</button></td>
            </tr>
        `;
    });
    
    // GST Calculate (simplified 5% average for example, or based on products)
    // Actually, we should get GST from each product, but for simplicity we calculate a flat or get it from products.
    // Let's get GST from original products
    let gstTotal = 0;
    cart.forEach(item => {
        const p = allProducts.find(x => x.id === item.product_id);
        const gstPct = p ? p.gst_percentage : 0;
        gstTotal += (item.total * gstPct) / 100;
    });
    
    const grandTotal = subtotal + gstTotal;
    
    document.getElementById('subtotal').innerText = `₹${subtotal.toFixed(2)}`;
    document.getElementById('gst-total').innerText = `₹${gstTotal.toFixed(2)}`;
    document.getElementById('grand-total').innerText = `₹${grandTotal.toFixed(2)}`;
}

function clearCart() {
    cart = [];
    renderCart();
}

function confirmBill() {
    if(cart.length === 0) {
        showToast("Cart is empty");
        return;
    }
    document.getElementById('confirm-modal').classList.add('show');
}

function closeModal() {
    document.getElementById('confirm-modal').classList.remove('show');
}

async function generateAndPrintBill() {
    closeModal();
    
    let subtotal = 0;
    let gstTotal = 0;
    cart.forEach(item => {
        subtotal += item.total;
        const p = allProducts.find(x => x.id === item.product_id);
        const gstPct = p ? p.gst_percentage : 0;
        gstTotal += (item.total * gstPct) / 100;
    });
    const grandTotal = subtotal + gstTotal;
    
    const payload = {
        subtotal: subtotal,
        gst: gstTotal,
        discount: 0,
        grand_total: grandTotal,
        payment_method: 'CASH',
        items: cart
    };
    
    try {
        const res = await fetch('/api/bills', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        if(!res.ok) {
            showToast("Error saving bill on server");
            return;
        }
        
        const data = await res.json();
        if(data.status === 'success') {
            showToast("Bill Generated: " + data.bill_number);
            // Print
            window.open(`/bill/${data.bill_id}/view`, '_blank');
            clearCart();
        }
    } catch(err) {
        showToast("Network Error: Could not reach server");
        console.error(err);
    }
}
