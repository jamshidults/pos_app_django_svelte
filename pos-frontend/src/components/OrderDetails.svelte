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

<div>
  <table>
    <thead>
      <tr>
        <th>Product Code</th>
        <th>Product Name</th>
        <th>Quantity</th>
        <th>Price</th>
      </tr>
    </thead>
    <tbody>
      {#each orderItems as orderItem, index}
        <tr class:selected={index === selectedOrderIndex} on:click={() => handleRowClick(index)}>
          <td>{orderItem.product_code}</td>
          <td>{orderItem.product_name}</td>
          <td>{orderItem.qty}</td>
          <td>{orderItem.price}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 0.5em;
    border: 1px solid #ccc;
  }

  .selected {
    background-color: #f0f0f0;
  }
</style>
