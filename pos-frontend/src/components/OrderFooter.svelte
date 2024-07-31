<script>
  export let paymentMethod = 'cash';
  export let orderTotal = 0;
  export let salesman = 'jamshid';
</script>

<div class="bg-gray-100 p-4 mt-4 rounded-lg shadow-lg">
  <div class="flex justify-between items-center mb-4">
    <div class="w-1/3">
      <label for="paymentMethod" class="block text-sm font-medium text-gray-700">Payment Method</label>
      <select id="paymentMethod" bind:value={paymentMethod} class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <option value="">Select Payment Method</option>
        <option value="cash">Cash</option>
        <option value="card">Card</option>
        <option value="upi">UPI</option>
      </select>
    </div>
    <div class="w-1/3">
      <label for="salesman" class="block text-sm font-medium text-gray-700">Salesman</label>
      <input type="text" id="salesman" bind:value={salesman} class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
    <div class="w-1/3 text-right">
      <label for="orderTotal" class="block text-sm font-medium text-gray-700">Order Total</label>
      <div id="orderTotal" class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-green-600">
        ${orderTotal.toFixed(2)}
      </div>
    </div>
  </div>
</div>
