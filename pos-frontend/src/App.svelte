<script>
  import { onMount } from 'svelte';
  import Header from './components/Header.svelte';
  import ProductEntryForm from './components/ProductEntryForm.svelte';
  import OrderDetails from './components/OrderDetails.svelte';
  import OrderFooter from './components/OrderFooter.svelte';
  import axios from 'axios';


  let orderItems = [];
  let editItem = null;
  let selectedOrderIndex = -1;
  let nextId = 1;
  let paymentMethod = '';
  let productFocus = false
 
  let salesman = '';

  $: orderTotal = orderItems.reduce((sum, item) => sum + (item.qty * item.price), 0);

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
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'PageDown') {
      event.preventDefault();
      if (event.key === 'PageDown' && orderItems.length >0) {
      
        saveOrder();
      }
      if (event.key === 'ArrowUp') {
        console.log("arrow up and from App svelte");
        selectedOrderIndex = Math.max(0, selectedOrderIndex - 1);
      } else if (event.key === 'ArrowDown') {
        console.log("arrow down and from App svelte");
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
        order_details: orderItems,
        payment_method: paymentMethod,
        order_total: orderTotal,
        salesman: salesman
      });
      printReceipt(response.data);
      resetOrderLines();
    } catch (error) {
      console.error('Error saving order:', error);
    }
  }

 

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
        <p>Payment Method: ${order.payment_method}</p>
        <p>Order Total: ${order.order_total}</p>
        <p>Salesman: ${order.salesman}</p>
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
    orderTotal = 0;
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
<main tabindex="0" role="application" aria-label="POS Application" class="container mx-auto p-4">
<div>
    <OrderFooter bind:paymentMethod bind:orderTotal bind:salesman />
  <div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <ProductEntryForm {editItem} on:addItem={addOrderItem}  />
    <OrderDetails {orderItems} {selectedOrderIndex} on:select={event => selectedOrderIndex = event.detail} />
  </div>

</main>

<style>
  main {
    outline: none;
  }
</style>
