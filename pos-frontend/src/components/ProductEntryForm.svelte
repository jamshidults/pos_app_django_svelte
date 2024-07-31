<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import axios from 'axios';
 
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




  async function populateForm(item) {
    productCode = item.product_code;
    const response = await axios.get(`http://localhost:8000/api/products/?product_code=${productCode}`);
    product = response.data[0];
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
    } else if (event.key === 'ArrowUp' ) {
      console.log("arrow up and arrow down from productForm");
       productCodeInput.focus();
    }
  }
</script>

<div role="form" aria-label="Product Entry Form" on:keydown={handleKeydown} class="space-y-4 p-4 bg-white shadow rounded-lg">
  <input
    type="text"
    placeholder="Enter Product Code"
    bind:value={productCode}
    bind:this={productCodeInput}
    on:blur={findProduct}
    aria-label="Product Code"
    class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
  />
  <input
    type="text"
    placeholder="Product Name"
    value={product ? product.product_name : ''}
    readonly
    aria-label="Product Name"
    class="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
  />
  <input
    type="number"
    placeholder="Qty"
    bind:value={qty}
    bind:this={qtyInput}
    aria-label="Quantity"
    class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
  />
  <input
    type="number"
    placeholder="Price"
    bind:value={price}
    readonly
    aria-label="Price"
    class="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
  />
  <button
    type="button"
    on:click={addProduct}
    class="w-full p-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors duration-200"
  >
    {editItem ? 'Update' : 'Add'} to Order
  </button>
</div>

<style>
  /* Add any additional styles if needed */
</style>
