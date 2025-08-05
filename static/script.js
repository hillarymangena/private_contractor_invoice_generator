let items = [];
let email = '';
let title = '';

function updateTitle() {
    title = document.getElementById('type').value;
    document.getElementById('selectedTitle').textContent = title;
}

function addItem() {
    const item = document.getElementById('item').value;
    const price = parseFloat(document.getElementById('price').value);
    if (item && !isNaN(price)) {
        items.push({ description: item, price: price });
        addToTable(item, price, items.length - 1);
        document.getElementById('item').value = '';
        document.getElementById('price').value = '';
    }
    document.getElementById('doneBtn').style.display = 'inline';
}

function addToTable(item, price, index) {
    const table = document.getElementById('itemsTable');
    table.style.display = 'table';
    const row = table.insertRow();
    row.insertCell(0).innerText = item;
    row.insertCell(1).innerText = `R${price.toFixed(2)}`;
    
    const editBtn = document.createElement("button");
    editBtn.innerText = "Edit";
    editBtn.onclick = () => openEditForm(index);
    row.insertCell(2).appendChild(editBtn);

    const deleteBtn = document.createElement("button");
    deleteBtn.innerText = "Delete";
    deleteBtn.onclick = () => deleteItem(index);
    row.insertCell(3).appendChild(deleteBtn);
}

function deleteItem(index) {
    items.splice(index, 1);
    refreshTable();
    showConfirmation(); // Refresh summary after delete
}

function finishItems() {
    email = document.getElementById('email').value;
    if (email && items.length > 0) {
        document.getElementById('itemsForm').style.display = 'none';
        showConfirmation();
    } else {
        alert('Please enter email and at least one item.');
    }
}

function showConfirmation() {
    const details = document.getElementById('details');
    let total = items.reduce((sum, item) => sum + item.price, 0);
    let vat = total * 0.15;
    let finalTotal = total + vat;

    let itemListHTML = '<ul>';
    items.forEach(item => {
        itemListHTML += `<li>${item.description} – R${item.price.toFixed(2)}</li>`;
    });
    itemListHTML += '</ul>';

    details.innerHTML = `
        <p><strong>${title}</strong> for <strong>${email}</strong></p>
        <p><strong>Items:</strong> ${itemListHTML}</p>
        <p>Total: R${total.toFixed(2)}</p>
        <p>VAT (15%): R${vat.toFixed(2)}</p>
        <p><strong>Final Total: R${finalTotal.toFixed(2)}</strong></p>
    `;
    document.getElementById('confirmation').style.display = 'block';
}

function confirmDetails(answer) {
    const sendBtn = document.getElementById('sendBtn');
    if (answer === 'no') {
        document.getElementById('confirmation').style.display = 'none';
        document.getElementById('itemsForm').style.display = 'block';
    } else {
        sendBtn.disabled = true;
        sendBtn.textContent = "Sending...";
        generatePDF().finally(() => {
            sendBtn.disabled = false;
            sendBtn.textContent = "Send";
        });
    }
}

function openEditForm(index) {
    document.getElementById('editItem').value = items[index].description;
    document.getElementById('editPrice').value = items[index].price;
    document.getElementById('editIndex').value = index;
    document.getElementById('editForm').style.display = 'block';
    document.getElementById('confirmation').style.display = 'none';
}

function saveEdit() {
    const index = parseInt(document.getElementById('editIndex').value);
    const newItem = document.getElementById('editItem').value;
    const newPrice = parseFloat(document.getElementById('editPrice').value);
    if (newItem && !isNaN(newPrice)) {
        items[index] = { description: newItem, price: newPrice };
        refreshTable();
        document.getElementById('editForm').style.display = 'none';
        showConfirmation();
    }
}

function refreshTable() {
    const table = document.getElementById('itemsTable');
    table.innerHTML = '<tr><th>Item</th><th>Price</th><th>Edit</th><th>Delete</th></tr>';
    items.forEach((item, index) => {
        addToTable(item.description, item.price, index);
    });
}

function generatePDF() {
    return fetch('http://localhost:8080/generate-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, email, items })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => alert(data.message))
    .catch(error => {
        console.error('Fetch error:', error);
        alert('Failed to send PDF: ' + error.message);
    });
}
