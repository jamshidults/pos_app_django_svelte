<script>
  import { createEventDispatcher, onMount,onDestroy } from 'svelte';
  import axios from 'axios';
 
  export let editItem = null;

  let productCode = '';
  let product = null;
  let products = [];
  let qty = '';
  let price = 0;
  const dispatch = createEventDispatcher();

  let productCodeInput;
  let qtyInput;
  $: product = products.find(p => p.product_code == productCode) || '';

   async function fetchProducts() {
    try {
      const response = await axios.get('http://localhost:8000/api/products/');
      products = response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  }

  function getProduct() {
    product = products.find(p => p.product_code == productCode) || '';
  }



  onMount(() => {
    fetchProducts();
    productCodeInput.focus();
    if (editItem) {
      populateForm(editItem);
    }
  });

  $: if (editItem) {
    populateForm(editItem);
  }


    onDestroy(() => {
    document.removeEventListener('keydown', handleKeydown);
  });





  function populateForm(item) {
    productCode = item.product_code;
    getProduct();

    if (product) {
      price = item.price;
      qty = item.qty;
    }
    qtyInput.focus();
  }

  function findProduct() {

    if (product) {
      price = product.price;
    }
    qtyInput.focus();
  }

  function addProduct() {
      if (product && product.qty_in_ltr *Number(qty) > 3) {
      alert("Total quantity in liters for this item exceeds 3 liters.");
      return;
    }

    if (product && qty > 0) {

      const newItem = { ...product, qty: Number(qty), price,qty_in_ltr:product.qty_in_ltr * Number(qty) };
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
