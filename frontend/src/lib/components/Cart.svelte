<script>
    import { createEventDispatcher } from 'svelte';
    import QRCode from 'qrcode';
    import { getPromptPayPayload } from '$lib/api';

    export let items = []; // Receives cart items as a prop

    let showQRModal = false;
    let qrCodeCanvas; // bind:this to the canvas element
    let qrPayload = '';
    let isGenerating = false;
    let error = null;

    const dispatch = createEventDispatcher();

    $: total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    function increment(item) {
        dispatch('updateQuantity', { ...item, quantity: item.quantity + 1 });
    }

    function decrement(item) {
        if (item.quantity > 1) {
            dispatch('updateQuantity', { ...item, quantity: item.quantity - 1 });
        } else {
            dispatch('removeItem', item);
        }
    }

    async function handlePromptPayCheckout() {
        if (total <= 0) return;

        isGenerating = true;
        error = null;

        try {
            const response = await getPromptPayPayload(total);
            qrPayload = response.payload;
            showQRModal = true;

            // Use a timeout to ensure the canvas is in the DOM before drawing
            setTimeout(() => {
                if (qrCodeCanvas) {
                    QRCode.toCanvas(qrCodeCanvas, qrPayload, { width: 256, errorCorrectionLevel: 'H' }, (err) => {
                        if (err) console.error(err);
                    });
                }
            }, 100);

        } catch (e) {
            error = e.message;
        } finally {
            isGenerating = false;
        }
    }

    function closeModal() {
        showQRModal = false;
        // Optionally, clear the cart after payment modal is closed
        dispatch('clearCart');
    }
</script>

<div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4">Cart</h2>
    {#if items.length === 0}
        <p class="text-gray-500">Your cart is empty.</p>
    {:else}
        <div class="space-y-2 mb-4">
            {#each items as item (item.id)}
                <div class="flex justify-between items-center border-b pb-2">
                    <div>
                        <p class="font-semibold">{item.name}</p>
                        <p class="text-sm text-gray-600">฿{item.price.toFixed(2)}</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button on:click={() => decrement(item)} class="px-2 border rounded">-</button>
                        <span>{item.quantity}</span>
                        <button on:click={() => increment(item)} class="px-2 border rounded">+</button>
                    </div>
                </div>
            {/each}
        </div>
        <div class="text-right font-bold text-xl mb-4">
            Total: ฿{total.toFixed(2)}
        </div>
        <button
            on:click={handlePromptPayCheckout}
            disabled={isGenerating}
            class="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors disabled:bg-gray-400"
        >
            {isGenerating ? 'Generating...' : 'Pay with PromptPay QR'}
        </button>
        {#if error}
            <p class="text-red-500 mt-2">{error}</p>
        {/if}
    {/if}
</div>

<!-- QR Code Modal -->
{#if showQRModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" on:click={closeModal}>
        <div class="bg-white p-8 rounded-lg shadow-xl text-center" on:click|stopPropagation>
            <h3 class="text-2xl font-bold mb-2">Scan to Pay</h3>
            <p class="text-lg mb-4">Total Amount: <span class="font-bold">฿{total.toFixed(2)}</span></p>
            <canvas bind:this={qrCodeCanvas} class="mx-auto"></canvas>
            <p class="text-xs text-gray-500 mt-4">Closes automatically after scanning or by clicking away.</p>
            <button on:click={closeModal} class="mt-4 bg-gray-300 px-4 py-2 rounded">Close</button>
        </div>
    </div>
{/if}
