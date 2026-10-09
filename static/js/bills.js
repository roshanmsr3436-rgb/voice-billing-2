let allBills = [];

document.addEventListener('DOMContentLoaded', loadBills);

async function loadBills() {
    const res = await fetch('/api/bills');
    allBills = await res.json();
    renderBillsTable(allBills);
}

function renderBillsTable(bills) {
    const tbody = document.getElementById('bills-table-body');
    if(!tbody) return;
    tbody.innerHTML = '';
    
    bills.forEach(b => {
        tbody.innerHTML += `
            <tr>
                <td>${b.bill_number}</td>
                <td>${b.created_at}</td>
                <td>₹${b.grand_total.toFixed(2)}</td>
                <td>${b.payment_method}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="reprintBill(${b.id})">Reprint</button>
                </td>
            </tr>
        `;
    });
}

function filterBillsTable() {
    const q = document.getElementById('search-bills').value.toLowerCase();
    const filtered = allBills.filter(b => b.bill_number.toLowerCase().includes(q));
    renderBillsTable(filtered);
}

function reprintBill(id) {
    window.open(`/bill/${id}/view`, '_blank');
}
