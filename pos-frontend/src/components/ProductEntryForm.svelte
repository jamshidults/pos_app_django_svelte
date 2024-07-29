<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import axios from 'axios';
  export let items = [];
  export let editItem = null;
  let productCode = '';
  let product = null;
  let qty = '';
  let price = 0;
  const dispatch = createEventDispatcher();

  let productCodeInput;
  let qtyInput;

  onMount(() => {
    productCodeInput.focus();
    if (editItem) {
      populateForm(editItem);
    }
  });

  $: if (editItem) {
    populateForm(editItem);
  }

  function populateForm(item) {
    productCode = item.product_code;
    product = items.find(p => p.product_code === +productCode);
    if (product) {
      price = item.price;
      qty = item.qty;
    }
    qtyInput.focus();
  }


  async function findProduct() {
    const response = await axios.get(`http://localhost:8000/api/products/?product_code=${productCode}`);
    console.log(response.data);
    product = response.data[0];
    if (product) {
      price = product.price;
    }
    qtyInput.focus();
  }



  function addProduct() {
    if (product && qty > 0) {
      const newItem = { ...product, qty: Number(qty), price };
      dispatch('addItem', newItem);
      resetForm();
    }
  }

  function resetForm() {
    productCode = '';
    product = null;
    qty = '';
    price = 0;
    editItem = null;
    productCodeInput.focus();
  }

  function handleKeydown(event) {
    if (event.key === 'Enter') {
      if (document.activeElement === productCodeInput) {
        findProduct();
      } else if (document.activeElement === qtyInput) {
        addProduct();
      }
    } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      productCodeInput.blur();
    }
  }
</script>

<div role="form" aria-label="Product Entry Form" on:keydown={handleKeydown}>
  <input
    type="text"
    placeholder="Enter Product Code"
    bind:value={productCode}
    bind:this={productCodeInput}
    on:blur={findProduct}
    aria-label="Product Code"
  />
  <input type="text" placeholder="Product Name" value={product ? product.product_name : ''} readonly aria-label="Product Name" />
  <input
    type="number"
    placeholder="Qty"
    bind:value={qty}
    bind:this={qtyInput}
    aria-label="Quantity"
  />
  <input
    type="number"
    placeholder="Price"
    bind:value={price}
    readonly
    aria-label="Price"
  />
  <button type="button" on:click={addProduct}>{editItem ? 'Update' : 'Add'} to Order</button>
</div>

<style>
  div {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    margin-bottom: 1em;
  }

  input, button {
    padding: 0.5em;
    font-size: 1em;
  }

  button {
    align-self: flex-start;
    cursor: pointer;
  }
</style>
