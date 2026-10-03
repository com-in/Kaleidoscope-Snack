ServerEvents.recipes(event => {

    const offal = 'kaleidoscope_cookery:raw_cow_offal';
    const casing = 'kaleidoscope_snack:sausage_casing';

    // 1 个牛杂 → 2 个肠衣
    event.recipes.kaleidoscope_cookery.stockpot(
        Item.of(casing, 2),
        [offal],
        'minecraft:water'
    );

    // 2 个牛杂 → 4 个肠衣
    event.recipes.kaleidoscope_cookery.stockpot(
        Item.of(casing, 4),
        [offal, offal],
        'minecraft:water'
    );

    // 3 个牛杂 → 6 个肠衣
    event.recipes.kaleidoscope_cookery.stockpot(
        Item.of(casing, 6),
        [offal, offal, offal],
        'minecraft:water'
    );

    // 4 个牛杂 → 8 个肠衣
    event.recipes.kaleidoscope_cookery.stockpot(
        Item.of(casing, 8),
        [offal, offal, offal, offal],
        'minecraft:water'
    );

});
// 盛出汤锅内容时返还碗-刷碗的来

// BlockEvents.rightClicked('kaleidoscope_cookery:stockpot', event => {

//    const player = event.player;

    // 必须手持碗
//    if (player.mainHandItem.id !== 'minecraft:bowl') return;

    // 等森罗物语完成盛出动作
//    event.server.scheduleInTicks(1, () => {
//        player.give('minecraft:bowl');
//    });

//});
