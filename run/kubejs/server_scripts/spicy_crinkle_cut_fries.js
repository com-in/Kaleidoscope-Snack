ServerEvents.recipes(event => {

    event.custom({
        type: 'kaleidoscope_cookery:pot',

        carrier: {
            item: 'minecraft:bowl'
        },

        ingredients: [
            {
                item: 'kaleidoscope_snack:potato_chunks'
            },
            {
                item: 'kaleidoscope_snack:potato_chunks'
            },
            {
                item: 'kaleidoscope_snack:potato_chunks'
            },
            {
                item: 'kaleidoscope_cookery:red_chili'
            },
            {
                item: 'kaleidoscope_cookery:red_chili'
            }
        ],

        result: {
            count: 1,
            id: 'kaleidoscope_snack:spicy_crinkle_cut_fries'
        }
    });

});