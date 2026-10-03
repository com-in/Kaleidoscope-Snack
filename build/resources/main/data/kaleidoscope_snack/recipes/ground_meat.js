ServerEvents.recipes(event => {

    // 生五花肉 → 肉馅
    event.recipes.kaleidoscope_cookery.chopping_board(
        '3x kaleidoscope_snack:ground_meat',
        'kaleidoscope_cookery:raw_pork_belly',
        'kaleidoscope_cookery:raw_pork_belly',
        4
    );

    // 生牛杂 → 肉馅
    event.recipes.kaleidoscope_cookery.chopping_board(
        '3x kaleidoscope_snack:ground_meat',
        'kaleidoscope_cookery:raw_cow_offal',
        'kaleidoscope_cookery:raw_cow_offal',
        4
    );

});