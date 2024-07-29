<script>
  import { onMount } from 'svelte';
  import Header from './components/Header.svelte';
  import ProductEntryForm from './components/ProductEntryForm.svelte';
  import OrderDetails from './components/OrderDetails.svelte';

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
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      event.preventDefault();
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
