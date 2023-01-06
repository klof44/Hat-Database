<script lang='ts'>
    import ErrorPage from '/src/ErrorPage.svelte';
    import data from '/src/hats.json?raw';
    import { page } from '$app/stores';
    import fs from 'fs';

    const json: Array<Hat> = JSON.parse(data);
    let error = false;
    let cape = false;
    let rock = false;
    const hat = json.find((hatInQuestion) => hatInQuestion.id == $page.url.searchParams.get('id'))!;
    if (hat != undefined) {
        cape = fs.existsSync(`/capes/${hat.id}`);
        rock = fs.existsSync(`/rocks/${hat.id}`);
    } else {
        error = true;
    }
</script>
{#if error}
    <ErrorPage/>
{:else}
    <div class="header">
        <h1>{hat.name}</h1>
    </div>
    <div class="hat-info">
        <div class="hat-img">
            <img class="duck" src="/thumbs-large/{hat.id}.png" alt="{hat.name}" width="500">
            <img class="quacking duck" src="/quack-thumbs-large/{hat.id}.png" alt="{hat.name} quack" width="500">
            <div class="extras">
            {#if cape}
                <img id='cape' src='/capes/{hat.id}.png' alt='{hat.name} Cape' width='200'>
            {/if}
            {#if rock}
                <img id='rock' src='/rocks/{hat.id}.png' alt='{hat.name} Rock' width='200'>
            {/if}
        </div>
      </div>
    </div>
    <div class="info-box">
      {#if hat.mod != null}
        <p>Workshop ID: {hat.mod}</p>
      {/if}
      <p class="first-button"><a href="/hats/{hat.id}.png" download target="_blank" rel="noreferrer"><button>Download</button></a></p>
      {#if hat.mod != null}
        <p><a href="https://steamcommunity.com/sharedfiles/filedetails/?id={hat.mod}" target="_blank" rel="noreferrer"><button>Workshop Page</button></a></p>
      {/if}
    </div>
{/if}
<style>
    .info-box {
        margin: 10px;
        border: 5px solid black;
        border-radius: 5px;
        background-color: rgb(100, 100, 100);
        display: flex;
        align-items: center;
    }
    .info-box p {
        padding: 10px;
    }
    .info-box button {
        padding: 10px;
        border: 2px solid black;
        border-radius: 5px;
        background-color: rgb(70, 70, 70);
        color: white;
        transition-duration: 0.3s;
    }
    .info-box button:hover {
        background-color: rgb(150, 150, 150);
    }
    .first-button {
        margin-left: auto;
    }
    .hat-img {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    .extras {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>