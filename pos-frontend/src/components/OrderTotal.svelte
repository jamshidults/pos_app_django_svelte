<script>
  export let orderItems = [];
  $: total = orderItems.reduce((sum, item) => sum + (item.qty * item.price), 0);
</script>

<div class="order-total border p-4 rounded-lg shadow-md bg-white">
  <h3 class="text-xl font-semibold mb-4">Order Total</h3>
  <p class="text-lg">${total.toFixed(2)}</p>
</div>

<style>
  .order-total {
    max-width: 400px;
    margin: auto;
  }
</style>
