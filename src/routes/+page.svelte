<script lang="ts">
    import { page } from '$app/stores';
    import data from '/src/hats.json?raw';

    const json: Array<Hat> = JSON.parse(data);

    let pageNum: number = 1;
    if ($page.url.searchParams.has('page')) {
        pageNum = parseInt($page.url.searchParams.get('page')!);
        if (pageNum < 1) {
            pageNum = 1;
        }
        if (isNaN(pageNum)) {
            pageNum = 1;
        }
    }
    
    let hats: Array<Hat> = [];
    for (let i = 48 * (pageNum - 1); i < 48 * pageNum; i++) {
        hats.push({
            id: json[i].id,
            name: json[i].name,
            mod: json[i].mod
        });
    }
</script>
<div class="header">
    <h1>Hat Database</h1>
</div>
<div class="hats-list">
    {#each hats as hat}
        <span class='hat'>
            <img src='./thumbs/{hat.id}.png' alt='{hat.name}' width="150">
            <img class="quacking" src='./quack-thumbs/{hat.id}.png' alt='{hat.name} quack' width="150">
            <span class='info'>
                <p><b>{hat.name}</b></p>
                <a href='/hats/{hat.id}.png' download target="_blank" rel="noreferrer"><button>Download</button></a>
                <a href='/info?id={hat.id}'><button>Info</button></a>
            </span>
        </span>
    {/each}
</div>
<div class="pagechanger">
    {#if pageNum > 1}
        <a href='?page={pageNum - 1}'><button>&#60;</button></a>
    {:else}
        <button style="opacity: 0.4;">&#60;</button>
    {/if}
    <p>{pageNum}</p>
    <a href=".?page={pageNum + 1}"><button>&#62;</button></a>
</div>
<footer>
    <p>Site by <a href="https://github.com/klof44"><img class="avatar" src="/avatar.png" alt="klof44's github"><b>klof44</b></a></p>
    <p>Discord: <b>klof44#6612</b></p>
    <p>Email: <b>klof4four@gmail.com</b></p>
    <a class="footer-left-first github" href="https://github.com/klof44/Hat-Database"><img src="/github.svg" width="60" alt="github"></a>
</footer>
<style>
    .hats-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        grid-template-rows: repeat(auto-fill, minmax(200px, 1fr));
        padding: 10px;
        gap: 10px;
    }
    .hat {
        width: 420px;
        height: 145px;
        border: 4px solid black;
        border-radius: 5px;
        padding: 10px;
        background-color: rgb(100, 100, 100);
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .hat img {
        display: block;
        margin: auto;
    }
    .hat button {
        padding: 10px;
        border: 2px solid black;
        border-radius: 5px;
        background-color: var(--button-primary);
        color: white;
        transition-duration: 0.3s;
        width: 80px;
    }
    .hat button:hover {
        background-color: var(--button-hover);
    }

    .info {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .info p {
        max-width: 88px;
        direction: rtl;
    }
    .info a {
        text-decoration: none;
        display: block;
        margin-top: 10px;
        width: fit-content;
    }

    .pagechanger {
        display: flex;
        flex-direction: row;
        justify-content: center;
        padding: 20px;
    }
    .pagechanger p {
        font-size: 20px;
        padding-inline: 10px;
        text-align: center;
        width: 3%;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .pagechanger button {
        width: 50px;
        height: 50px;
        font-size: 25px;
        background-color: var(--background-header);
        border-radius: 5px;
        border: 2px solid black;
    }
    .pagechanger a {
        width: 50px;
        height: 50px;
    }
    .pagechanger button:hover {
        transition-duration: 0.3s;
        background-color: rgb(100, 180, 120);
    }
    footer {
        background-color: var(--footer);
        gap: 20px;
        text-align: left;
        display: flex;
        flex-direction: row;
        align-items: center;
        position:absolute;
        width: 100%;
    }
    footer p {
        padding-top: 30px;
        padding-bottom: 15px;
        padding-inline: 10px;
        height: 30px;
        margin: 0;
        line-height: 30px;
    }
    footer a {
        text-decoration: none;
        color: white;
    }
    .footer-left-first {
        margin-left: auto;
    }
    .avatar {
        vertical-align: middle;
        border-radius: 90px;
        margin: 0;
    }
    .github {
        padding-inline: 10px;
        padding-top: 5px;
    }
</style>