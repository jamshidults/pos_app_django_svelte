<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let paymentMethod = "cash";
  export let salesman = "";

  function handlePaymentMethodChange(event) {
    paymentMethod = event.target.value;
    dispatch('paymentMethodChange', paymentMethod);
  }

  function handleSalesmanChange(event) {
    salesman = event.target.value;
    dispatch('salesmanChange', salesman);
  }
</script>

<div class="payment-method border p-4 rounded-lg shadow-md bg-white">
  <h3 class="text-xl font-semibold mb-4">Payment Method</h3>
  <select bind:value={paymentMethod} on:change={handlePaymentMethodChange} class="border rounded p-2 w-full mb-4">
    <option value="cash">Cash</option>
    <option value="card">Card</option>
    <option value="upi">UPI</option>
  </select>
  <h3 class="text-xl font-semibold mb-4">Salesman</h3>
  <input type="text" bind:value={salesman} on:change={handleSalesmanChange} class="border rounded p-2 w-full mb-4">
</div>

<style>
  .payment-method {
    max-width: 400px;
    margin: auto;
  }
</style>
