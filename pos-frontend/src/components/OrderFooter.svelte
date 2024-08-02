<script>
  export let orderTotal;
  export let totalQtyInLtr;
  export let counters = [];
  export let paymentMethods = [];
  export let selectedCounterId;
  export let selectedPaymentMethodId;

  // Function to update the selected payment method based on the selected counter
  function handleCounterChange() {
    const selectedCounter = counters.find(counter => counter.id === selectedCounterId);
    if (selectedCounter) {
      selectedPaymentMethodId = selectedCounter.payment_method;
      console.log("payment mehtod id>>>>>>>>>>>>>>",selectedPaymentMethodId)
    }
  }

  // Watch for changes in selectedCounterId to update the payment method
  $: if (selectedCounterId) {
    handleCounterChange();
  }
</script>

<footer class="bg-gray-200 text-gray-800 p-2 fixed bottom-0 w-full flex justify-between items-center border-t border-gray-300">

  <div class="flex items-center space-x-4">
    <div>
      <label for="counter" class="block text-sm font-medium text-gray-700">Counter</label>
      <select
        id="counter"
        bind:value={selectedCounterId}
        class="mt-1 block w-full pl-2 pr-8 py-1 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      >
        {#each counters as counter}
          <option value={counter.id}>{counter.name}</option>
        {/each}
      </select>
    </div>
    <div>
      <label for="paymentMethod" class="block text-sm font-medium text-gray-700">Payment Method</label>
      <select
        id="paymentMethod"
        bind:value={selectedPaymentMethodId}
        class="mt-1 block w-full pl-2 pr-8 py-1 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      >
        {#each paymentMethods as method}
          <option value={method.id}>{method.name}</option>
        {/each}
      </select>
    </div>
  </div>
  <div class="text-lg font-bold text-green-600">
    Total Qty Ltr: {totalQtyInLtr.toFixed(2)}
  </div>
  <div class="text-lg font-bold text-green-600">
    Order Total: {orderTotal.toFixed(2)}
  </div>

</footer>

<style>
  footer {
    background-color: #e5e7eb; /* Tailwind's bg-gray-200 */
    color: #1f2937; /* Tailwind's text-gray-800 */
  }

  select {
    background-color: #f9fafb; /* Tailwind's bg-gray-50 */
    color: #1f2937; /* Tailwind's text-gray-800 */
  }
</style>
