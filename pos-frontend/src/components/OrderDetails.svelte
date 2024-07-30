<script>
  import { createEventDispatcher } from 'svelte';
  export let orderItems = [];
  export let selectedOrderIndex = -1;
  const dispatch = createEventDispatcher();

  function handleRowClick(index) {
    selectedOrderIndex = index;
    dispatch('select', index);
  }
</script>

<div class="overflow-x-auto">
  <table class="min-w-full divide-y divide-gray-200 bg-white shadow rounded-lg">
    <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product Code</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product Name</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each orderItems as orderItem, index}
        <tr class="hover:bg-gray-100 cursor-pointer {index === selectedOrderIndex ? 'bg-gray-200' : ''}" on:click={() => handleRowClick(index)}>
          <td class="px-6 py-4 whitespace-nowrap">{orderItem.product_code}</td>
          <td class="px-6 py-4 whitespace-nowrap">{orderItem.product_name}</td>
          <td class="px-6 py-4 whitespace-nowrap">{orderItem.qty}</td>
          <td class="px-6 py-4 whitespace-nowrap">{orderItem.price}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  .selected {
    background-color: #f0f0f0;
  }
</style>
