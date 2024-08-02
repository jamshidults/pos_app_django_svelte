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


  $: orderTotal = orderItems.reduce((sum, item) => sum + (item.qty * item.price), 0);
  $: totalQtyInLtr = orderItems.reduce((sum, item) => sum + item.qty_in_ltr, 0);
  $: if (totalQtyInLtr > 3) {
     alert("Total quantity in liters cannot exceed 3 liters.");
  }


  let counters = [];
  let paymentMethods = [];
  let selectedCounterId = null;
  let selectedPaymentMethodId = null;

  async function fetchCounters() {
    try {
      const response = await axios.get('http://localhost:8000/api/counters/');
      counters = response.data;
    } catch (error) {
      console.error('Error fetching counters:', error);
    }
  }

  async function fetchPaymentMethods() {
    try {
      const response = await axios.get('http://localhost:8000/api/payment_methods/');
      paymentMethods = response.data;
    } catch (error) {
      console.error('Error fetching payment methods:', error);
    }
  }


  // async function fetchUser() {
  //   try {
  //     const response = await axios.get('http://localhost:8000/api/user/');
  //     user = response.data;
  //   } catch (error) {
  //     console.error('Error fetching user:', error);
  //   }
  // }

  function addOrderItem(event) {
    const newItem = event.detail;

    if (totalQtyInLtr > 3) {
      alert("Total quantity in liters cannot exceed 3 liters.");
      return;
    }

    if (editItem) {

      const index = orderItems.findIndex(item => item.id === editItem.id);
      const old_item  = orderItems.find(item => item.id === editItem.id)
       if (totalQtyInLtr - old_item.qty_in_ltr + newItem.qty_in_ltr > 3) {
            alert("Total quantity in liters cannot exceed 3 liters.");
            return;
      }
      if (index !== -1) {
        orderItems[index] = { ...newItem, id: editItem.id };
      }
      editItem = null;
    } else {
      if (totalQtyInLtr + newItem.qty_in_ltr > 3) {
      alert("Total quantity in liters cannot exceed 3 liters.");
      return;
    }
      orderItems = [...orderItems, { ...newItem, id: nextId++ }];
    }
    selectedOrderIndex = -1;
  }

  function handleKeydown(event) {
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'PageDown') {
      event.preventDefault();
      if (event.key === 'PageDown') {
        saveOrder();
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
    if (totalQtyInLtr > 3) {
      alert("Total quantity in liters cannot exceed 3 liters.");
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/api/orders/', {
        order_details: orderItems,
        order_total: orderTotal,
        counter:selectedCounterId,
        payment_method: selectedPaymentMethodId
      });
      printReceipt(response.data);
      resetOrderLines();
    } catch (error) {
      console.error('Error saving order:', error);
    }
  }

  function printReceipt(order) {
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
        <p>Order Total: ${order.order_total}</p>
        <p>Payment Method: ${order.payment_method}</p>
      </div>
    `;

    let printWindow = window.open('', '', 'width=600,height=400');
    printWindow.document.write('<html><head><title>Print Receipt</title>');
    printWindow.document.write('</head><body>');
    printWindow.document.write(receiptContent);
    printWindow.document.write('</body></html>');
    printWindow.document.close();

    printWindow.onload = function() {
        printWindow.focus();
        printWindow.print();
        setTimeout(function() {
            printWindow.close();
        }, 100);
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
    fetchCounters();
    fetchPaymentMethods();
    document.addEventListener('keydown', handleKeydown);
  
  });
</script>

<Header />
<main tabindex="0" role="application" aria-label="POS Application" class="container mx-auto p-4">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <ProductEntryForm on:addItem={addOrderItem} {editItem} />
    <OrderDetails {orderItems} {selectedOrderIndex} on:select={event => selectedOrderIndex = event.detail} />
  </div>
</main>
 <OrderFooter {orderTotal} {totalQtyInLtr} {counters} {paymentMethods} bind:selectedCounterId bind:selectedPaymentMethodId />
