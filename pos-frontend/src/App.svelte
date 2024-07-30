<script>
  import { onMount } from 'svelte';
  import Header from './components/Header.svelte';
  import ProductEntryForm from './components/ProductEntryForm.svelte';
  import OrderDetails from './components/OrderDetails.svelte';
  import axios from 'axios';

  let items = [
    { product_code: 2125, product_id: 2, product_name: "bra 750 ml", unit_qty: 1, qty_in_ltr: 0.750, price: 300 }
  ];
  let orderItems = [];
  let editItem = null;
  let selectedOrderIndex = -1;
  let nextId = 1;

  function addOrderItem(event) {
    const newItem = event.detail;

    if (editItem) {
      const index = orderItems.findIndex(item => item.id === editItem.id);
      if (index !== -1) {
        orderItems[index] = { ...newItem, id: editItem.id };
      }
      editItem = null;
    } else {
      orderItems = [...orderItems, { ...newItem, id: nextId++ }];
    }
    selectedOrderIndex = -1;
  }

  function handleKeydown(event) {

    if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key=== 'PageDown') {
      event.preventDefault();
      if (event.key === 'PageDown') {
        saveOrder()
      }
      if (event.key === 'ArrowUp') {
        selectedOrderIndex = Math.max(0, selectedOrderIndex - 1);
      } else if (event.key === 'ArrowDown') {
        selectedOrderIndex = Math.min(orderItems.length - 1, selectedOrderIndex + 1);
      }
    } else if ((event.key === 'Delete' || event.key === 'd' || event.key === 'D') && selectedOrderIndex !== -1) {
      deleteOrderLine(selectedOrderIndex);
    } else if ((event.key === 'e' || event.key === 'E') && selectedOrderIndex !== -1) {
      editOrderLine(selectedOrderIndex);
      event.preventDefault();
    }
  }

  async function saveOrder() {
    try {
      const response = await axios.post('http://localhost:8000/api/orders/', {
        order_details: orderItems
      });
      printReceipt(response.data);
      resetOrderLines();
     
    } catch (error) {
      console.error('Error saving order:', error);
    }
  }

  


  // function printReceipt(order) {
  //   let receipt = `Order ID: ${order.id}\nOrder Date: ${order.order_date}\n\nItems:\n`;
  //   order.order_details.forEach(detail => {
  //     receipt += `${detail.product_name} - ${detail.qty} x ${detail.price}\n`;
  //   });
  //   const blob = new Blob([receipt], { type: 'text/plain' });
  //   const url = URL.createObjectURL(blob);
  //   const a = document.createElement('a');
  //   a.href = url;
  //   a.download = `receipt-${order.id}.txt`;
  //   a.click();
  //   URL.revokeObjectURL(url);
  // }

  function printReceipt(order) {
    // Generate receipt content
    let receiptContent = `
      <div>
        <h2>Order ID: ${order.id}</h2>
        <p>Order Date: ${order.order_date}</p>
        <h3>Items:</h3>
        <ul>
          ${order.order_details.map(detail => `
            <li>${detail.product_name} - ${detail.qty} x ${detail.price}</li>
          `).join('')}
        </ul>
      </div>
    `;

    // Open a new window for printing
    let printWindow = window.open('', '', 'width=600,height=400');
    printWindow.document.write('<html><head><title>Print Receipt</title>');
    printWindow.document.write('</head><body>');
    printWindow.document.write(receiptContent);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    
    // Wait for the document to be fully loaded and then print
    printWindow.onload = function() {
        printWindow.focus();
        printWindow.print();
        setTimeout(function() {
            printWindow.close();
        }, 100);  // Close the print window after 100 milliseconds
    };
}






  function resetOrderLines() {
    orderItems = [];
  }

  function deleteOrderLine(index) {
    orderItems = orderItems.filter((_, i) => i !== index);
    selectedOrderIndex = -1;
  }

  function editOrderLine(index) {
    const orderItem = orderItems[index];
    editItem = orderItem;
  }

  onMount(() => {
    document.addEventListener('keydown', handleKeydown);
  });
</script>

<Header />
<main tabindex="0" role="application" aria-label="POS Application">
  <ProductEntryForm {items} on:addItem={addOrderItem} {editItem} />
  <OrderDetails {orderItems} {selectedOrderIndex} on:select={event => selectedOrderIndex = event.detail} />
</main>

<style>
  main {
    padding: 1em;
    outline: none;
  }
</style>
