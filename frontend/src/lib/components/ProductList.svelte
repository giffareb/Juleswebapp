<script>
    import { onMount, createEventDispatcher } from 'svelte';
    import { getProducts } from '$lib/api';

    let products = [];
    let isLoading = true;
    let error = null;

    const dispatch = createEventDispatcher();

    onMount(async () => {
        try {
            // Let's create some mock products for now, as the DB will be empty on first run
            products = [
                { id: 1, name: 'Latte', price: 50, description: 'Coffee with milk' },
                { id: 2, name: 'Espresso', price: 40, description: 'Strong coffee shot' },
                { id: 3, name: 'Croissant', price: 35, description: 'Buttery pastry' },
            ];
            // You can uncomment this to fetch from the actual API
            // products = await getProducts();
        } catch (e) {
            error = e.message;
        } finally {
            isLoading = false;
        }
    });

    function addToCart(product) {
        dispatch('addToCart', product);
    }
</script>

<div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4">Products</h2>
    {#if isLoading}
        <p>Loading products...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each products as product (product.id)}
                <div class="border p-4 rounded-lg shadow-sm">
                    <h3 class="text-lg font-semibold">{product.name}</h3>
                    <p class="text-gray-600">{product.description || ''}</p>
                    <p class="text-xl font-bold my-2">฿{product.price.toFixed(2)}</p>
                    <button
                        on:click={() => addToCart(product)}
                        class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors"
                    >
                        Add to Cart
                    </button>
                </div>
            {/each}
        </div>
    {/if}
</div>
