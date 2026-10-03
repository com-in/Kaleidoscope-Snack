ServerEvents.recipes(event => {

    // 生香肠 → 烤肠
    event.recipes.minecraft.campfire_cooking(
        'kaleidoscope_snack:cooked_sausage',
        'kaleidoscope_snack:sausage',
        0.35,
        200
    );

});